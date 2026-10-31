# QNX IPC test results

These are the three scenarios reported as successfully tested on the QNX target. The client inputs are sample values, not live sensor readings.

| Test | Temperature | CO2 | Occupancy | Expected response | Reported result |
|---|---:|---:|---:|---|---|
| High HVAC load | 35°C | 1200 ppm | 5 | High HVAC load warning; cooling and ventilation | Passed |
| Empty room | 24°C | 500 ppm | 0 | Switch HVAC to energy-saving mode | Passed |
| Normal operation | 24°C | 500 ppm | 3 | HVAC operating normally | Passed |

## Test procedure
1. Build server and client using the QNX toolchain.
2. Start the server first.
3. Set the sample values in `qnx_ipc/client.c` for the selected scenario and rebuild the client.
4. Run the client and verify the reply.
5. Keep the server running for subsequent tests; do not launch a duplicate server with the same registered name.

## Evidence to attach
Add genuine screenshots of the QNX server, each client test, Python analysis output, and Streamlit dashboard.

These tests validate the QNX message exchange and decision rules. They do not establish real energy savings, physical AC operation, or live sensor accuracy.
