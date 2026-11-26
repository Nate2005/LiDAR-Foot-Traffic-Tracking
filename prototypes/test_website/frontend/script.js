const button = document.getElementById("refresh");
const buttonStatus = document.getElementById("status");
const tbody = document.querySelector("#data tbody");

async function refresh() {
    button.disabled = true;
    buttonStatus.textContent = "Loading...";

    try {
        // Send request to FastAPI endpoint, format data as json.
        const response = await fetch("api/readings", { cache: "no-store"});
        if (!response.ok) throw new Error("HTTP " + response.status);
        const rows = await response.json();

        // Read out json, making new row for each reading.
        tbody.innerHTML = "";
        for (const r of rows) {
            const tableRow = document.createElement("tr");
            for (const key of ["id", "sensor", "value", "time"]) {
                const tableData = document.createElement("td");
                tableData.textContent = r[key];
                tableRow.appendChild(tableData);
            }
            tbody.appendChild(tableRow);
        }

        buttonStatus.textContent = "Updated " + new Date().toUTCString() + " - " + rows.length + " rows";
    } catch (err) {
        buttonStatus.textContent = "Error: " + err.message;
    } finally {
        button.disabled = false;
    }
}