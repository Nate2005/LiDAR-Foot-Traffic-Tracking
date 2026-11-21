# Backend API

FastAPI app in `src/api/main.py`. See the [main README](../README.md#backend) for how to run it. Interactive docs are at <http://127.0.0.1:8000/docs> when it is running.

## Buildings

A building looks like:

```json
{
  "building_id": 1,
  "building_name": "Scrugham Engineering and Mines",
  "building_code": "SEM",
  "outline": {"type": "Polygon", "coordinates": [[[-119.8163, 39.5399], [-119.8158, 39.5399], [-119.8158, 39.5403], [-119.8163, 39.5403], [-119.8163, 39.5399]]]}
}
```

- `building_name`: full name, unique.
- `building_code`: short code, unique.
- `outline`: optional GeoJSON `Polygon` or `MultiPolygon` (RFC 7946), with positions as `[longitude, latitude]`. Each ring must have at least 4 positions and end where it starts.

| Method | Path | Does | Errors |
|---|---|---|---|
| `GET` | `/buildings` | List all buildings | |
| `GET` | `/buildings?q=sem` | Search by full name or code (case-insensitive, partial match; exact code matches first) | |
| `GET` | `/buildings/{id}` | Get one building | `404` |
| `POST` | `/buildings` | Create a building (`building_name` and `building_code` required) | `409` duplicate name/code, `422` invalid body |
| `PATCH` | `/buildings/{id}` | Change only the fields sent; `"outline": null` clears the outline | `404`, `409`, `422` |
| `DELETE` | `/buildings/{id}` | Delete a building | `404` |

## Pathways

A pathway segment is an edge in the routing graph:

```json
{
  "pathway_id": 1,
  "pathway_name": "Quad north walk",
  "boundary": {"type": "LineString", "coordinates": [[-119.8163, 39.5399], [-119.8158, 39.5403]]},
  "allow_riders": true,
  "allow_vehicles": false,
  "ada_accessible": true
}
```

- `pathway_name`: unique.
- `boundary`: optional GeoJSON `LineString`, `MultiLineString`, `Polygon` or `MultiPolygon`.
- `allow_riders`, `allow_vehicles`, `ada_accessible`: default `false` on create. In a `PATCH`, `null` leaves them as they are.

| Method | Path | Does | Errors |
|---|---|---|---|
| `GET` | `/pathways` | List all pathways. Filter with `?ada_accessible=true`, `?allow_riders=true`, `?allow_vehicles=false` (combinable) | |
| `GET` | `/pathways/{id}` | Get one pathway | `404` |
| `POST` | `/pathways` | Create a pathway (`pathway_name` required) | `409` duplicate name, `422` |
| `PATCH` | `/pathways/{id}` | Change only the fields sent; `"boundary": null` clears it | `404`, `409`, `422` |
| `DELETE` | `/pathways/{id}` | Delete a pathway and its intersection links | `404`, `409` a sensor is attached |

## Intersections

An intersection is a node in the routing graph:

```json
{
  "intersection_id": 1,
  "intersection_name": "quad-north",
  "name": "North end of the Quad",
  "boundary": {"type": "Point", "coordinates": [-119.8163, 39.5399]}
}
```

- `intersection_name`: unique key. `name`: optional display name.
- `boundary`: optional GeoJSON `Point`, `Polygon` or `MultiPolygon`.

| Method | Path | Does | Errors |
|---|---|---|---|
| `GET` | `/intersections` | List all intersections | |
| `GET` | `/intersections/{id}` | Get one intersection | `404` |
| `POST` | `/intersections` | Create an intersection (`intersection_name` required) | `409` duplicate name, `422` |
| `PATCH` | `/intersections/{id}` | Change only the fields sent | `404`, `409`, `422` |
| `DELETE` | `/intersections/{id}` | Delete an intersection, its links **and its TrafficEvent history** | `404`, `409` a sensor is attached |

## Pathway–intersection links

| Method | Path | Does | Errors |
|---|---|---|---|
| `GET` | `/pathways/{id}/intersections` | Intersections at the ends of a pathway | `404` pathway |
| `GET` | `/intersections/{id}/pathways` | Pathways meeting at an intersection | `404` intersection |
| `PUT` | `/pathways/{pid}/intersections/{iid}` | Link them (`204`; linking twice is fine) | `404` either missing |
| `DELETE` | `/pathways/{pid}/intersections/{iid}` | Remove the link | `404` no such link |

Building examples with curl (or use `/docs`):

```bash
curl -X POST http://127.0.0.1:8000/buildings \
  -H 'Content-Type: application/json' \
  -d '{"building_name": "Davidson Mathematics and Science Center", "building_code": "DMSC"}'

curl 'http://127.0.0.1:8000/buildings?q=davidson'

# Use the building_id returned by the POST above (2 if you ran the seed script)
curl -X PATCH http://127.0.0.1:8000/buildings/2 \
  -H 'Content-Type: application/json' \
  -d '{"outline": {"type": "Polygon", "coordinates": [[[-119.8163, 39.5399], [-119.8158, 39.5399], [-119.8158, 39.5403], [-119.8163, 39.5403], [-119.8163, 39.5399]]]}}'

curl -X DELETE http://127.0.0.1:8000/buildings/2
```

From the frontend (served behind nginx):

```js
const buildings = await (await fetch("/api/buildings?q=" + encodeURIComponent(text))).json();
```
