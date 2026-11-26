#!/usr/bin/env python3

import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOST = socket.gethostname()
SERVICES = ['nginx', 'capstone', 'capstone-listener', 'cloudflared', 'tailscaled']
URLS = {
    'website (local)': 'http://127.0.0.1/',
    'api (local)': 'http://127.0.0.1/api/health',
    'website (public)': 'https://unrwalkingmap.com/',
    'api (public)': 'https://unrwalkingmap.com/api/health',
}
DB_PATH = '/data/app.db'

def env_num(name, default):
    return float(os.environ.get(name, default))

TEMP_WARN = env_num('TEMP_WARN', 70)
TEMP_CRIT = env_num('TEMP_CRIT', 80)
DISK_WARN = env_num('DISK_WARN', 85)
MEM_MIN_PCT = env_num('MEM_MIN_PCT', 10)
SUMMARY_HOUR = int(env_num('SUMMARY_HOUR', 8))
STATE_FILE = Path(os.environ.get('STATE_DIRECTORY', '/var/lib/pi_monitor')) / 'state.json'

# Checks to run on the Pi
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10)

def check_url(url):
    last = '' 
    for _ in range(2):
        start = time.time()
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pi-monitor/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    return True, f'200 in {time.time() - start:.2f}s'
                last = f'HTTP {r.status}'
        except Exception as e:
            last = str(e)
        time.sleep(3)
    return False, last

def cpu_temp():
    return int(Path('/sys/class/thermal/thermal_zone0/temp').read_text()) / 1000

def throttled_flags():
    try:
        out = run(['vcgencmd', 'get_throttled']).stdout.strip()
        return int(out.split('=')[1], 16)
    except Exception:
        return None

def mem_available_pct():
    info = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key, val = line.split(':', 1)
        info[key] = int(val.split()[0])
    return 100 * info['MemAvailable'] / info['MemTotal']

# Run all the checks
def collect():
    problems, info = {}, []

    # Check if services are currently running
    for name in SERVICES:
        state = run(['systemctl', 'is-active', name]).stdout.strip()
        info.append(f'service {name}: {state}')
        if state != 'active':
            problems[f'svc-{name}'] = f'Service {name} is {state}'

    # Check local and public URLs, checks API also
    for label, url in URLS.items():
        ok, detail = check_url(url)
        info.append(f'{label}: {detail}')
        if not ok:
            problems[f'url-{label}'] = f'{label} unreachable ({detail})'

    # Check CPU temp
    temp = cpu_temp()
    info.append(f'CPU temp: {temp:.1f} C')
    if temp >= TEMP_CRIT:
        problems['temp'] = f'CPU temperature critical: {temp:.1f} C'
    elif temp >= TEMP_WARN:
        problems['temp'] = f'CPU temperature high: {temp:.1f} C'

    # Check Pi flags
    flags = throttled_flags()
    if flags is not None:
        info.append(f'throttle flags: {hex(flags)}')
        if flags & 0xF:
            problems['throttle'] = f'Throttled or under-voltage right now ({hex(flags)})'

    # Check storage
    disk = shutil.disk_usage('/')
    pct = 100 * disk.used / disk.total
    info.append(f'disk: {pct:.0f}% used, {disk.free / 1e9:.1f} GB free')
    if pct >= DISK_WARN:
        problems['disk'] = f'Disk is {pct:.0f}% full'

    # Check RAM
    mem = mem_available_pct()
    info.append(f'memory available: {mem:.0f}%')
    if mem <= MEM_MIN_PCT:
        problems['mem'] = f'Low memory: {mem:.0f}% available'

    # Check CPU load
    load1, load5, load15 = os.getloadavg()
    info.append(f'load: {load1:.2f} {load5:.2f} {load15:.2f}')
    if load5 > (os.cpu_count() or 4):
        problems['load'] = f'High load: {load5:.2f} (5 min avg)'

    uptime_h = float(Path('/proc/uptime').read_text().split()[0]) / 3600
    info.append(f'uptime: {uptime_h:.1f} h')

    return problems, info

# Send notifications through ntfy
def send_ntfy(subject, body, urgent):
    topic = os.environ.get('NTFY_TOPIC')
    if not topic:
        return False
    req = urllib.request.Request(
        f'https://ntfy.sh/{topic}',
        data=body.encode(),
        headers={'Title': subject, 'Priority': 'high' if urgent else 'default'},
        method='POST',
    )
    urllib.request.urlopen(req, timeout=15).close()
    return True

def notify(subject, body, urgent):
    try:
        if send_ntfy(subject, body, urgent):
            return True
    except Exception as e:
        print('ntfy failed: {e}', file=sys.stderr)
    print('No notifications sent.\n' + subject + '\n' + body)
    return False

# State and main
def load_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def main():
    problems, info = collect()
    force = '--summary' in sys.argv
    state = load_state()
    prev = set(state.get('problems', []))
    now = set(problems)
    new, cleared = now - prev, prev - now

    today = datetime.now().strftime('%Y-%m-%d')
    daily = datetime.now().hour >= SUMMARY_HOUR and state.get('last_summary') != today

    if not (now or cleared or daily or force):
        return

    lines = []
    if problems:
        lines.append('PROBLEMS:')
        lines += [f' - {m}' for m in problems.values()]
    if cleared:
        lines.append('RESOLVED:')
        lines += [f' - {k}' for k in sorted(cleared)]
    lines += ['', 'STATUS:'] + [f' {i}' for i in info]

    subject = f'[{HOST}] ' + (f'{len(problems)} problems(s)' if problems else 'all OK')
    if (daily or force) and not (new or cleared):
        subject += ' (summary)'

    if notify(subject, '\n'.join(lines), urgent=bool(new) and not force):
        state['problems'] = sorted(now)
        if daily:
            state['last_summary'] = today
        save_state(state)

if __name__ == '__main__':
    main()