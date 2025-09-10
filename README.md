# Vista Order Automation

Vista Order Automation streamlines order ingestion across partner sites, our web portal and the art server.

## Features
- Graphical interface built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).
- Command line tools powered by [Typer](https://typer.tiangolo.com/).
- Secure credential storage via the system keyring.
- Crimpress login verification with visual green/red status indicator.

## Requirements
- Python 3.10+
- Dependencies from `requirements.txt` (including `pyotp`)
- Environment variable `CRIMPRESS_LOGIN_URL` pointing to the Crimpress login page.

Install dependencies:
```bash
pip install -r requirements.txt
```

## GUI Usage
Launch the interface:
```bash
python -m cli gui
```
1. Open the **Settings** tab.
2. Enter Crimpress email and password.
3. Click **Test** to attempt a real login. The indicator turns green on success or red on failure.
4. Click **Save** to store credentials in the OS keyring.
5. Set the art server path and save program settings.

## CLI Usage
- `python -m cli login` – test Crimpress login using stored credentials.
- `python -m cli gui` – launch the GUI from the command line.

Stored credentials can be cleared using your platform's keyring tools. Program settings are written to `~/.vista_order_settings.json`.
