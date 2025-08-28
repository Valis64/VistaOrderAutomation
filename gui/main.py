"""Main application window using CustomTkinter."""
from __future__ import annotations

import customtkinter as ctk

from config.credentials import load_credentials, save_credentials


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Vista Order Automation")
        self.geometry("600x400")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both")

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
        self.status_indicator = ctk.CTkLabel(logins_frame, text="", width=12, height=12, fg_color="red", corner_radius=6)
        self.status_indicator.grid(row=1, column=2, rowspan=2, padx=10)

        save_button = ctk.CTkButton(logins_frame, text="Save", command=self._save_credentials)
        save_button.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        # Load stored credentials if present
        email, password = load_credentials()
        if email:
            self.email_entry.insert(0, email)
        if password:
            self.password_entry.insert(0, password)

    def _save_credentials(self) -> None:
        email = self.email_entry.get()
        password = self.password_entry.get()
        save_credentials(email, password)
        if email and password:
            self.status_indicator.configure(fg_color="green")
        else:
            self.status_indicator.configure(fg_color="red")


def main() -> None:
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
