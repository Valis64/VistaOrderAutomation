"""CSS selectors for web automation."""
from __future__ import annotations

# Crimpress login page selectors
CRIMPRESS_EMAIL_INPUT = "input[id='1-email']"
CRIMPRESS_PASSWORD_INPUT = "input[name='password']"
CRIMPRESS_SUBMIT_BUTTON = "button.auth0-lock-submit"

# POM (Cimpress) login page selectors
POM_USERNAME_INPUT = "input[name='username']"  # Username field
POM_EMAIL_INPUT = "input[name='email']"  # Fallback email field
POM_PASSWORD_INPUT = "input[name='password']"  # Password field
POM_SUBMIT_BUTTON = "button[type='submit']"  # Login submit button
POM_TOTP_INPUT = "input[name='code']"
POM_TOTP_SUBMIT = "button[type='submit']"

# POM orders page selectors
POM_ORDER_ROW = "div.order-row"  # Order row in list view
POM_ORDER_ROW_ID_LABEL = ".order-row .order-id"  # Order ID label within a row
POM_ORDER_CARD = "div.order-card"  # Order card in grid view
POM_ORDER_CARD_ID_LABEL = ".order-card .order-id"  # Order ID label within a card
POM_ART_DOWNLOAD_LINK = "a.art-download"  # Link to download art assets
POM_ART_DOWNLOAD_BUTTON = "button.art-download"  # Button to download art assets
POM_NEXT_PAGE_BUTTON = "button[aria-label='Next page']"  # Pagination next
POM_PREV_PAGE_BUTTON = "button[aria-label='Previous page']"  # Pagination previous
