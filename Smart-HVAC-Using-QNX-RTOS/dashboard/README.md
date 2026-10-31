# Streamlit dashboard

Copy your tested Streamlit application (`app.py`) into this folder.

Run from the repository root:

```bash
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

The current dashboard replays recorded CSV data. It is not connected to the QNX IPC server and does not receive live physical sensor data.
