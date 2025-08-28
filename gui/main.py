"""Main application window using CustomTkinter."""
from __future__ import annotations

import customtkinter as ctk

from config.credentials import load_credentials, save_credentials
from config.settings import load_settings, save_settings
from services.crimpress import login as crimpress_login
import sys
import traceback


class TextboxRedirector:
    """Redirects writes to a CTkTextbox."""

    def __init__(self, textbox: ctk.CTkTextbox) -> None:
        self.textbox = textbox

    def write(self, message: str) -> None:
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def flush(self) -> None:
        pass


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Vista Order Automation")
        self.geometry("600x400")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew")

        self.terminal = ctk.CTkTextbox(self, height=120)
        self.terminal.grid(row=1, column=0, sticky="ew")
        self.terminal.configure(state="disabled")

        redirector = TextboxRedirector(self.terminal)
        sys.stdout = redirector
        sys.stderr = redirector
        sys.excepthook = self._exception_hook

        self.tabview.add("Home")
        self.settings_tab = self.tabview.add("Settings")

        self._create_settings_tab()

    # Settings tab construction
    def _create_settings_tab(self) -> None:
        logins_frame = ctk.CTkFrame(self.settings_tab)
        logins_frame.pack(padx=20, pady=20, fill="x")

        ctk.CTkLabel(logins_frame, text="Crimpress Logins", font=("Helvetica", 16)).grid(
            row=0, column=0, columnspan=3, pady=(0, 10)
        )

        ctk.CTkLabel(logins_frame, text="Email:").grid(row=1, column=0, sticky="e", padx=(0, 5))
        self.email_entry = ctk.CTkEntry(logins_frame, width=200)
        self.email_entry.grid(row=1, column=1, sticky="w")

        ctk.CTkLabel(logins_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=(0, 5))
        self.password_entry = ctk.CTkEntry(logins_frame, width=200, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w")

        # status indicator
        self.status_indicator = ctk.CTkLabel(
            logins_frame, text="", width=12, height=12, fg_color="red", corner_radius=6
        )
        self.status_indicator.grid(row=1, column=2, rowspan=2, padx=10)

        test_button = ctk.CTkButton(logins_frame, text="Test", command=self._test_login)
        test_button.grid(row=3, column=0, pady=(10, 0))

        save_button = ctk.CTkButton(logins_frame, text="Save", command=self._save_credentials)
        save_button.grid(row=3, column=1, columnspan=2, pady=(10, 0))

        # Program settings frame
        config_frame = ctk.CTkFrame(self.settings_tab)
        config_frame.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkLabel(config_frame, text="Program Settings", font=("Helvetica", 16)).grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )

        ctk.CTkLabel(config_frame, text="Art Server Path:").grid(
            row=1, column=0, sticky="e", padx=(0, 5)
        )
        self.art_path_entry = ctk.CTkEntry(config_frame, width=300)
        self.art_path_entry.grid(row=1, column=1, sticky="w")

        config_save = ctk.CTkButton(
            config_frame, text="Save", command=self._save_program_settings
        )
        config_save.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Load stored credentials if present
        email, password = load_credentials()
        if email:
            self.email_entry.insert(0, email)
        if password:
            self.password_entry.insert(0, password)

        settings = load_settings()
        art_root = settings.get("art_root", "")
        if art_root:
            self.art_path_entry.insert(0, art_root)

    def _save_credentials(self) -> None:
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            save_credentials(email, password)
            print("Credentials saved")
            self._test_login()
        except Exception as exc:
            self._log_error(exc)

    def _test_login(self) -> None:
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            try:
                success = crimpress_login(email, password)
                print("Login test successful" if success else "Login test failed")
            except Exception as exc:
                success = False
                self._log_error(exc)
            self.status_indicator.configure(fg_color="green" if success else "red")
        else:
            self.status_indicator.configure(fg_color="red")

    def _save_program_settings(self) -> None:
        art_root = self.art_path_entry.get()
        try:
            save_settings(art_root)
            print("Program settings saved")
        except Exception as exc:
            self._log_error(exc)

    def _log_error(self, exc: Exception) -> None:
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()

    def _exception_hook(self, exc_type, exc, tb) -> None:
        self.terminal.configure(state="normal")
        self.terminal.insert("end", "".join(traceback.format_exception(exc_type, exc, tb)))
        self.terminal.see("end")
        self.terminal.configure(state="disabled")


def main() -> None:
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
