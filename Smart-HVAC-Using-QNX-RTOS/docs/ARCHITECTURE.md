# Architecture and workflow

## Implemented components
- Python analysis: reads the recorded occupancy dataset, reports shape/columns/missing values, plots occupancy distribution, and calculates average room temperature and CO2 statistics.
- Streamlit dashboard: independently reads the CSV, replays one record every two seconds, displays sensor metrics and trends, and produces dashboard-side HVAC recommendations.
- QNX IPC: a client sends a `HVAC_Message` to a server using `MsgSend()`. The server receives it with `MsgReceive()`, applies its rules, and returns `HVAC_Reply` with `MsgReply()`.

## QNX decision rules
1. If `temperature > 30` OR `co2 > 1000`, recommend high HVAC load/cooling and ventilation.
2. Else if `occupancy == 0`, recommend energy-saving mode.
3. Else, recommend normal operation.

The order matters: the high-load rule takes priority over the empty-room rule.

## Dashboard decision rules
1. If CO2 > 1000 ppm: high ventilation.
2. Else if occupancy is zero: energy saving.
3. Else if average temperature > 30°C: high cooling.
4. Else if average temperature > 26°C: moderate cooling.
5. Else: normal operation.

The dashboard and QNX server rules are not identical in the current code.

## Scope boundaries
The dashboard does not currently communicate with the QNX server. Dashboard playback and QNX client/server testing are independent demonstrations. There are no live physical sensors or AC actuators in this prototype.
