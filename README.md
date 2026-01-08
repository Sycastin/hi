# Name to Desmos

Type a name, convert it into Bézier curves, and plot it in Desmos.

## What you need

- Python 3.11+ installed
- A terminal (Command Prompt, PowerShell, or macOS/Linux Terminal)
- Internet access (Desmos API loads from `desmos.com`)

## Setup (first time)

```bash
python -m venv .venv
```

Activate the virtual environment:

- **macOS/Linux**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell)**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

You should see output like:

```
Running on http://127.0.0.1:5000
```

Open your browser and go to: <http://127.0.0.1:5000>

## How to use it

1. Type your name in the input.
2. Click **Plot on Desmos**.
3. The graph should draw your name as curves.

## Troubleshooting

- **“Nothing happens” after clicking the link:** Make sure `python app.py` is still running in your terminal. If it stopped, restart it and refresh the page.
- **Blank page or no graph:** Check the terminal for errors. You should see a log line when the page loads. Also make sure you have internet access so the Desmos script can load.
- **Windows won’t activate venv:** Run PowerShell as Administrator or use Command Prompt and run `venv\Scripts\activate.bat`.

## How it works

1. The browser sends the name to `/api/equations`.
2. The server uses `matplotlib.textpath.TextPath` to turn the text into Bézier paths.
3. Those paths are converted into line, quadratic, and cubic parametric equations.
4. The browser plots them in Desmos via the API.
