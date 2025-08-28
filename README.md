# Vista Order Automation

Vista Order Automation streamlines order ingestion across partner sites, our web portal and the art server.

## Features
- Graphical interface built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).
- Command line tools powered by [Typer](https://typer.tiangolo.com/).
- Secure credential storage via the system keyring.
- Crimpress login verification with visual green/red status indicator.

## Requirements
- Python 3.10+
- Dependencies from `requirements.txt`
- Crimpress login URL provided via the `CRIMPRESS_LOGIN_URL` environment variable or configured in the Settings tab (default URL is prefilled).

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
3. Adjust the Crimpress login URL if needed and set the art server path.
4. Click **Test** to attempt a real login. The indicator turns green on success or red on failure.
5. Click **Save** to store credentials and program settings.

## CLI Usage
- `python -m cli login` – test Crimpress login using stored credentials.
- `python -m cli gui` – launch the GUI from the command line.

Stored credentials can be cleared using your platform's keyring tools. Program settings are written to `~/.vista_order_settings.json`.
