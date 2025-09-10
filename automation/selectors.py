"""CSS selectors for web automation."""
from __future__ import annotations

# Crimpress login page selectors
CRIMPRESS_EMAIL_INPUT = "input[id='1-email']"
CRIMPRESS_PASSWORD_INPUT = "input[name='password']"
CRIMPRESS_SUBMIT_BUTTON = "button.auth0-lock-submit"

# POM (Cimpress) login page selectors
POM_USERNAME_INPUT = "input[name='username']"
POM_PASSWORD_INPUT = "input[name='password']"
POM_LOGIN_BUTTON = "button[type='submit']"
POM_TOTP_INPUT = "input[name='code']"
POM_TOTP_SUBMIT = "button[type='submit']"

# POM orders page selectors
POM_ORDER_ROW = "div.order-row"
POM_ORDER_ID = ".order-id"
POM_ART_FILE_LINK = "a.art-download"
POM_NEXT_BUTTON = "button[aria-label='Next page']"
