# Smart HVAC Using QNX RTOS

A software prototype for intelligent HVAC decision support using recorded environmental/occupancy data, Python analysis, a Streamlit dashboard, and QNX Neutrino message-passing IPC.

## Workflow
1. Analyse recorded occupancy and environmental readings using Python and Pandas.
2. Replay recorded readings in a Streamlit monitoring dashboard.
3. Send sample temperature, CO2 and occupancy values from a QNX client to a QNX server.
4. The QNX server applies threshold-based rules and replies with an HVAC recommendation.

## Decision algorithm
The QNX server applies these rules in order:
- If temperature > 30°C **or** CO2 > 1000 ppm: recommend cooling and ventilation.
- Else if occupancy is 0: recommend energy-saving mode.
- Else: recommend normal operation.

The Streamlit dashboard has its own display logic: CO2 > 1000 ppm, then unoccupied room, then temperature > 30°C, then temperature > 26°C, otherwise normal. The dashboard's rules are not identical to the QNX server's rules.

## Repository structure
```text
Smart-HVAC-Using-QNX-RTOS/
├── Datasets/
│   └── Occupancy_Estimation.csv
├── python/
│   ├── data_analysis.py
│   └── occupancy_graph.png       # generated when analysis runs
├── qnx_ipc/
│   ├── ipc.c
│   ├── client.c
│   └── Makefile
├── dashboard/
│   └── app.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── TEST_RESULTS.md
├── requirements.txt
└── .gitignore
```

## Setup: Python analysis and dashboard
Place the dataset at `Datasets/Occupancy_Estimation.csv`. Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Run analysis:
```bash
python python/data_analysis.py
```

Run dashboard:
```bash
streamlit run dashboard/app.py
```

The dashboard replays recorded CSV rows every two seconds. It is not a live sensor feed.

## QNX build and run
Build `qnx_ipc/ipc.c` and `qnx_ipc/client.c` with the QNX Momentics/QCC toolchain configured for your target. Start the server first, then run the client in a separate QNX terminal. The Makefile is a starting point; verify the QCC target variant for your installed QNX SDP.

The server and client both use the service name `smart_hvac_test`.

## Verified QNX scenarios
| Temperature | CO2 | Occupancy | Expected QNX response |
|---:|---:|---:|---|
| 35°C | 1200 ppm | 5 | High HVAC load warning |
| 24°C | 500 ppm | 0 | Energy-saving mode |
| 24°C | 500 ppm | 3 | Normal operation |

See `docs/TEST_RESULTS.md`.

## Important implementation boundaries
- The Python dashboard and QNX IPC programs are currently separate; no dashboard-to-QNX bridge is implemented.
- The QNX client currently sends hardcoded sample values, not physical sensor readings.
- The QNX server returns a software recommendation; it does not control a physical air conditioner.
- AC inlet/outlet temperature and humidity are unavailable in the supplied dataset.
- QNX thread priorities have not been explicitly configured in this prototype.

## Future work
Integrate the dashboard with QNX through a communication bridge, add live sensor input, and develop a properly isolated and safety-validated hardware control interface.

## Team information
Add your team name, member names, institution and hackathon details here.

## Dataset and licensing
Confirm that the dataset's licence permits public redistribution before committing it. Add an appropriate repository licence only after confirming that your team has the rights to publish all included code and data.
