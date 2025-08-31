"""
Service-specific handlers for common web services like Gmail, Skype, etc.
These handlers use browser automation to perform actions while preserving user sessions.
"""

import time
import re
from typing import Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from browsing import browsers, check_login_status, navigate_to_service
from core.config import settings


class GmailHandler:
    """Handler for Gmail operations."""

    def __init__(self, browser_id: str):
        self.browser_id = browser_id

    def check_login(self) -> Dict[str, Any]:
        """Check if user is logged into Gmail."""
        return check_login_status(self.browser_id, "gmail")

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> str:
        """Send an email via Gmail."""
        if self.browser_id not in browsers:
            return f"Browser {self.browser_id} not found"

        driver = browsers[self.browser_id]

        try:
            # Check login status
            login_status = self.check_login()
            if not login_status.get("logged_in", False):
                return "Please log into Gmail first. The browser will navigate to Gmail - please sign in."

            # Click compose button
            compose_selectors = [
                "[data-tooltip*='Compose']",
                "[aria-label*='Compose']",
                ".T-I.T-I-KE.L3",
                "[role='button'][aria-label*='Compose']"
            ]

            compose_button = None
            for selector in compose_selectors:
                try:
                    compose_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not compose_button:
                return "Could not find compose button. Please make sure you're on the Gmail inbox page."

            compose_button.click()
            time.sleep(2)

            # Fill recipient
            to_selectors = [
                "textarea[aria-label*='To']",
                "input[aria-label*='To']",
                "[role='combobox'][aria-label*='To']"
            ]

            to_field = None
            for selector in to_selectors:
                try:
                    to_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if to_field:
                to_field.clear()
                to_field.send_keys(to)
                time.sleep(1)

            # Fill CC if provided
            if cc:
                cc_selectors = [
                    "[aria-label*='Cc']",
                    "input[aria-label*='Cc']"
                ]
                for selector in cc_selectors:
                    try:
                        cc_field = driver.find_element(By.CSS_SELECTOR, selector)
                        cc_field.clear()
                        cc_field.send_keys(cc)
                        break
                    except:
                        continue

            # Fill BCC if provided
            if bcc:
                bcc_selectors = [
                    "[aria-label*='Bcc']",
                    "input[aria-label*='Bcc']"
                ]
                for selector in bcc_selectors:
                    try:
                        bcc_field = driver.find_element(By.CSS_SELECTOR, selector)
                        bcc_field.clear()
                        bcc_field.send_keys(bcc)
                        break
                    except:
                        continue

            # Fill subject
            subject_selectors = [
                "input[aria-label*='Subject']",
                "input[placeholder*='Subject']",
                "[role='textbox'][aria-label*='Subject']"
            ]

            subject_field = None
            for selector in subject_selectors:
                try:
                    subject_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if subject_field:
                subject_field.clear()
                subject_field.send_keys(subject)
                time.sleep(1)

            # Fill body
            body_selectors = [
                "div[aria-label*='Message Body']",
                "div[role='textbox'][aria-label*='Message Body']",
                ".Am",
                "[contenteditable='true']"
            ]

            body_field = None
            for selector in body_selectors:
                try:
                    body_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if body_field:
                body_field.clear()
                body_field.send_keys(body)
                time.sleep(1)

            # Send email
            send_selectors = [
                "[data-tooltip*='Send']",
                "[aria-label*='Send']",
                ".T-I.T-I-KE.L3",
                "[role='button'][aria-label*='Send']"
            ]

            send_button = None
            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if send_button:
                send_button.click()
                time.sleep(3)  # Wait for send confirmation
                return f"Email sent successfully to {to}"
            else:
                return "Could not find send button"

        except Exception as e:
            return f"Failed to send email: {str(e)}"


class SkypeHandler:
    """Handler for Skype operations."""

    def __init__(self, browser_id: str):
        self.browser_id = browser_id

    def check_login(self) -> Dict[str, Any]:
        """Check if user is logged into Skype."""
        return check_login_status(self.browser_id, "skype")

    def start_call(self, contact: str) -> str:
        """Start a call with a Skype contact."""
        if self.browser_id not in browsers:
            return f"Browser {self.browser_id} not found"

        driver = browsers[self.browser_id]

        try:
            # Check login status
            login_status = self.check_login()
            if not login_status.get("logged_in", False):
                return "Please log into Skype first. The browser will navigate to Skype - please sign in."

            # Search for contact
            search_selectors = [
                "[placeholder*='Search']",
                "[aria-label*='Search']",
                "input[type='search']"
            ]

            search_field = None
            for selector in search_selectors:
                try:
                    search_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not search_field:
                return "Could not find search field in Skype"

            search_field.clear()
            search_field.send_keys(contact)
            time.sleep(2)

            # Click on contact
            contact_selectors = [
                f"[aria-label*='{contact}']",
                f"[data-text-as-pseudo-element*='{contact}']",
                ".contact"
            ]

            contact_element = None
            for selector in contact_selectors:
                try:
                    contact_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not contact_element:
                return f"Could not find contact '{contact}' in Skype"

            contact_element.click()
            time.sleep(2)

            # Click call button
            call_selectors = [
                "[data-text-as-pseudo-element='Call']",
                "[aria-label*='Call']",
                "[title*='Call']",
                ".call-button"
            ]

            call_button = None
            for selector in call_selectors:
                try:
                    call_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if call_button:
                call_button.click()
                return f"Call started with {contact}"
            else:
                return "Could not find call button"

        except Exception as e:
            return f"Failed to start call: {str(e)}"

    def send_message(self, contact: str, message: str) -> str:
        """Send a message to a Skype contact."""
        if self.browser_id not in browsers:
            return f"Browser {self.browser_id} not found"

        driver = browsers[self.browser_id]

        try:
            # Check login status
            login_status = self.check_login()
            if not login_status.get("logged_in", False):
                return "Please log into Skype first. The browser will navigate to Skype - please sign in."

            # Search for contact and open chat
            search_selectors = [
                "[placeholder*='Search']",
                "[aria-label*='Search']",
                "input[type='search']"
            ]

            search_field = None
            for selector in search_selectors:
                try:
                    search_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not search_field:
                return "Could not find search field in Skype"

            search_field.clear()
            search_field.send_keys(contact)
            time.sleep(2)

            # Click on contact to open chat
            contact_selectors = [
                f"[aria-label*='{contact}']",
                f"[data-text-as-pseudo-element*='{contact}']",
                ".contact"
            ]

            contact_element = None
            for selector in contact_selectors:
                try:
                    contact_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not contact_element:
                return f"Could not find contact '{contact}' in Skype"

            contact_element.click()
            time.sleep(2)

            # Find message input
            message_selectors = [
                "[contenteditable='true']",
                "[role='textbox']",
                ".message-input",
                "[placeholder*='Type a message']"
            ]

            message_field = None
            for selector in message_selectors:
                try:
                    message_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not message_field:
                return "Could not find message input field"

            message_field.clear()
            message_field.send_keys(message)
            time.sleep(1)

            # Send message
            message_field.send_keys(Keys.RETURN)
            time.sleep(2)

            return f"Message sent to {contact}"

        except Exception as e:
            return f"Failed to send message: {str(e)}"


class OutlookHandler:
    """Handler for Outlook/Hotmail operations."""

    def __init__(self, browser_id: str):
        self.browser_id = browser_id

    def check_login(self) -> Dict[str, Any]:
        """Check if user is logged into Outlook."""
        return check_login_status(self.browser_id, "outlook")

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> str:
        """Send an email via Outlook."""
        if self.browser_id not in browsers:
            return f"Browser {self.browser_id} not found"

        driver = browsers[self.browser_id]

        try:
            # Check login status
            login_status = self.check_login()
            if not login_status.get("logged_in", False):
                return "Please log into Outlook first. The browser will navigate to Outlook - please sign in."

            # Click new email button
            new_email_selectors = [
                "[aria-label*='New mail']",
                "[title*='New message']",
                ".ms-Button--command",
                "[data-automation-id='composeButton']"
            ]

            new_email_button = None
            for selector in new_email_selectors:
                try:
                    new_email_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not new_email_button:
                return "Could not find new email button"

            new_email_button.click()
            time.sleep(3)

            # Fill recipient
            to_selectors = [
                "[aria-label*='To']",
                "input[placeholder*='To']",
                "[role='textbox'][aria-label*='To']"
            ]

            to_field = None
            for selector in to_selectors:
                try:
                    to_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if to_field:
                to_field.clear()
                to_field.send_keys(to)
                time.sleep(1)

            # Fill subject
            subject_selectors = [
                "[aria-label*='Subject']",
                "input[placeholder*='Subject']",
                "[role='textbox'][aria-label*='Subject']"
            ]

            subject_field = None
            for selector in subject_selectors:
                try:
                    subject_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if subject_field:
                subject_field.clear()
                subject_field.send_keys(subject)
                time.sleep(1)

            # Fill body
            body_selectors = [
                "[contenteditable='true']",
                "[role='textbox'][aria-label*='Message body']",
                ".ms-TextField-field"
            ]

            body_field = None
            for selector in body_selectors:
                try:
                    body_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if body_field:
                body_field.clear()
                body_field.send_keys(body)
                time.sleep(1)

            # Send email
            send_selectors = [
                "[aria-label*='Send']",
                "[title*='Send']",
                ".ms-Button--primary"
            ]

            send_button = None
            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if send_button:
                send_button.click()
                time.sleep(3)
                return f"Email sent successfully to {to}"
            else:
                return "Could not find send button"

        except Exception as e:
            return f"Failed to send email: {str(e)}"


# Service handler factory
def get_service_handler(service: str, browser_id: str):
    """Get the appropriate service handler."""
    handlers = {
        "gmail": GmailHandler,
        "skype": SkypeHandler,
        "outlook": OutlookHandler
    }

    handler_class = handlers.get(service.lower())
    if handler_class:
        return handler_class(browser_id)
    else:
        return None
