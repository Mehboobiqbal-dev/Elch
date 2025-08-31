"""
Intelligent request parser for user queries about web services.
Parses natural language requests and extracts service, action, and parameters.
"""

import re
from typing import Dict, Any, Optional
from gemini import generate_text


class RequestParser:
    """Parses user requests for web service actions."""

    def __init__(self):
        self.service_patterns = {
            "gmail": ["gmail", "email", "mail", "google mail"],
            "skype": ["skype", "call", "video call", "voice call"],
            "outlook": ["outlook", "hotmail", "live mail"],
            "slack": ["slack", "workspace"],
            "discord": ["discord", "server"],
            "whatsapp": ["whatsapp", "text message", "sms"],
            "telegram": ["telegram", "tg"],
            "facebook": ["facebook", "messenger", "fb"],
            "twitter": ["twitter", "tweet", "x"],
            "linkedin": ["linkedin", "professional network"],
            "zoom": ["zoom", "meeting", "conference"],
            "teams": ["teams", "microsoft teams"],
            "meet": ["meet", "google meet"]
        }

        self.action_patterns = {
            "send_email": ["send email", "send mail", "email", "write email", "compose email", "send gmail", "send outlook", "send yahoo"],
            "make_call": ["call", "make call", "start call", "video call", "voice call", "dial", "call on skype", "skype call", "video call on teams"],
            "send_message": ["send message", "text", "message", "chat", "talk", "send whatsapp", "whatsapp message", "text on whatsapp"],
            "schedule_meeting": ["schedule meeting", "book meeting", "set up meeting", "arrange meeting", "schedule slack meeting", "slack meeting"],
            "join_meeting": ["join meeting", "attend meeting", "enter meeting"],
            "post_update": ["post", "share", "update", "status", "post on facebook", "tweet on twitter", "share on linkedin"],
            "send_dm": ["dm", "direct message", "private message"]
        }

    def parse_request(self, request: str) -> Dict[str, Any]:
        """Parse a user request and extract service, action, and parameters."""
        request_lower = request.lower()

        # Extract service
        service = self._extract_service(request_lower)
        if not service:
            return {"error": "Could not identify the service you want to use"}

        # Extract action
        action = self._extract_action(request_lower, service)
        if not action:
            return {"error": f"Could not identify the action you want to perform on {service}"}

        # Extract parameters based on action
        params = self._extract_parameters(request, service, action)

        return {
            "service": service,
            "action": action,
            "params": params,
            "original_request": request
        }

    def _extract_service(self, request: str) -> Optional[str]:
        """Extract the service from the request."""
        request_lower = request.lower()

        # First, try exact pattern matching
        for service, patterns in self.service_patterns.items():
            for pattern in patterns:
                if pattern in request_lower:
                    return service

        # Special handling for ambiguous cases
        # Handle "teams" vs "zoom" vs "meet" more intelligently
        if "teams" in request_lower and ("meeting" in request_lower or "call" in request_lower):
            return "teams"
        elif "meet" in request_lower and "meeting" in request_lower:
            return "meet"
        elif "zoom" in request_lower:
            return "zoom"

        # Handle cases where service comes after action
        # e.g., "send gmail" -> gmail service
        service_indicators = {
            "gmail": ["gmail"],
            "skype": ["skype"],
            "outlook": ["outlook", "hotmail"],
            "slack": ["slack"],
            "discord": ["discord"],
            "whatsapp": ["whatsapp"],
            "telegram": ["telegram"],
            "facebook": ["facebook"],
            "twitter": ["twitter", "tweet"],
            "linkedin": ["linkedin"],
            "zoom": ["zoom"],
            "teams": ["teams", "microsoft teams"],
            "meet": ["meet", "google meet"]
        }

        for service, indicators in service_indicators.items():
            for indicator in indicators:
                if indicator in request_lower:
                    return service

        return None

    def _extract_action(self, request: str, service: str) -> Optional[str]:
        """Extract the action from the request."""
        # First, try exact pattern matching
        for action, patterns in self.action_patterns.items():
            for pattern in patterns:
                if pattern in request:
                    # Validate if action is appropriate for service
                    if self._is_valid_action_for_service(action, service):
                        return action

        # If no exact match, try to infer action from service context
        # Handle cases like "send gmail" where service name is used as action
        request_lower = request.lower()

        # Check for email services with send action
        if service in ["gmail", "outlook", "yahoo", "hotmail"]:
            if any(word in request_lower for word in ["send", "write", "compose", "email", "mail"]):
                return "send_email"

        # Check for communication services with call action
        if service in ["skype", "teams", "whatsapp", "discord"]:
            if any(word in request_lower for word in ["call", "video", "voice", "dial", "start"]):
                return "make_call"
            elif any(word in request_lower for word in ["send", "message", "text", "chat", "talk"]):
                return "send_message"

        # Check for social media with post action
        if service in ["facebook", "twitter", "linkedin"]:
            if any(word in request_lower for word in ["post", "share", "tweet", "update", "status"]):
                return "post_update"
            elif any(word in request_lower for word in ["dm", "direct", "private"]):
                return "send_dm"

        # Check for meeting services
        if service in ["zoom", "meet", "teams"]:
            if any(word in request_lower for word in ["schedule", "book", "set up", "arrange"]):
                return "schedule_meeting"
            elif any(word in request_lower for word in ["join", "attend", "enter"]):
                return "join_meeting"
            elif any(word in request_lower for word in ["meeting", "call"]):
                return "schedule_meeting"  # Default to scheduling for meeting services

        # If we have a service but no specific action, infer the default action
        default_actions = {
            "gmail": "send_email",
            "outlook": "send_email",
            "skype": "send_message",  # Default to messaging for communication
            "slack": "send_message",
            "discord": "send_message",
            "whatsapp": "send_message",
            "telegram": "send_message",
            "facebook": "post_update",
            "twitter": "post_update",
            "linkedin": "post_update",
            "teams": "send_message",
            "zoom": "schedule_meeting",
            "meet": "schedule_meeting"
        }

        # Check if the request contains action-like words
        action_words = ["send", "make", "start", "call", "text", "message", "email", "mail", "post", "share", "tweet", "schedule", "join"]
        has_action_word = any(word in request_lower for word in action_words)

        if not has_action_word and service in default_actions:
            return default_actions[service]

        return None

    def _is_valid_action_for_service(self, action: str, service: str) -> bool:
        """Check if an action is valid for a given service."""
        valid_actions = {
            "gmail": ["send_email"],
            "skype": ["make_call", "send_message"],
            "outlook": ["send_email"],
            "slack": ["send_message", "schedule_meeting"],
            "discord": ["send_message", "make_call", "join_meeting"],
            "whatsapp": ["send_message", "make_call"],
            "telegram": ["send_message"],
            "facebook": ["send_message", "post_update"],
            "twitter": ["post_update", "send_dm"],
            "linkedin": ["send_message", "post_update"],
            "zoom": ["schedule_meeting", "join_meeting"],
            "teams": ["send_message", "schedule_meeting", "join_meeting", "make_call"],
            "meet": ["schedule_meeting", "join_meeting"]
        }

        return action in valid_actions.get(service, [])

    def _extract_parameters(self, request: str, service: str, action: str) -> Dict[str, Any]:
        """Extract parameters from the request based on service and action."""
        params = {}

        if action == "send_email":
            params.update(self._extract_email_params(request))
        elif action in ["make_call", "send_message"]:
            params.update(self._extract_communication_params(request))
        elif action in ["schedule_meeting", "join_meeting"]:
            params.update(self._extract_meeting_params(request))
        elif action == "post_update":
            params.update(self._extract_post_params(request))

        return params

    def _extract_email_params(self, request: str) -> Dict[str, Any]:
        """Extract email-specific parameters."""
        params = {}

        # Extract recipient email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, request)
        if emails:
            params["to"] = emails[0]

        # Extract subject (look for "about" or "regarding" or "subject:")
        subject_patterns = [
            r'subject:\s*["\']([^"\']+)["\']',
            r'subject:\s*([^\n\r]+)',
            r'about\s+["\']([^"\']+)["\']',
            r'regarding\s+["\']([^"\']+)["\']'
        ]

        for pattern in subject_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                params["subject"] = match.group(1).strip()
                break

        # Extract message body (everything after "saying" or "that says")
        body_patterns = [
            r'saying\s*["\']([^"\']+)["\']',
            r'that says\s*["\']([^"\']+)["\']',
            r'message:\s*["\']([^"\']+)["\']',
            r'body:\s*["\']([^"\']+)["\']'
        ]

        for pattern in body_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                params["body"] = match.group(1).strip()
                break

        # Extract CC and BCC
        cc_match = re.search(r'cc:\s*([^\s,]+)', request, re.IGNORECASE)
        if cc_match:
            params["cc"] = cc_match.group(1).strip()

        bcc_match = re.search(r'bcc:\s*([^\s,]+)', request, re.IGNORECASE)
        if bcc_match:
            params["bcc"] = bcc_match.group(1).strip()

        return params

    def _extract_communication_params(self, request: str) -> Dict[str, Any]:
        """Extract communication-specific parameters (call/message)."""
        params = {}

        # Extract contact/name
        contact_patterns = [
            r'(?:call|message|text|contact)\s+([A-Za-z\s]+?)(?:\s+(?:and|about|that)|$)',
            r'to\s+([A-Za-z\s]+?)(?:\s+(?:and|about|that)|$)',
            r'with\s+([A-Za-z\s]+?)(?:\s+(?:and|about|that)|$)'
        ]

        for pattern in contact_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                contact = match.group(1).strip()
                # Remove common words
                contact = re.sub(r'\b(the|a|an|my|friend|contact)\b', '', contact, flags=re.IGNORECASE).strip()
                if contact:
                    params["contact"] = contact
                    break

        # Extract message content for messaging actions
        if "send_message" in request or "message" in request:
            message_patterns = [
                r'saying\s*["\']([^"\']+)["\']',
                r'that says\s*["\']([^"\']+)["\']',
                r'message:\s*["\']([^"\']+)["\']',
                r'["\']([^"\']+)["\']'
            ]

            for pattern in message_patterns:
                match = re.search(pattern, request, re.IGNORECASE)
                if match:
                    params["message"] = match.group(1).strip()
                    break

        return params

    def _extract_meeting_params(self, request: str) -> Dict[str, Any]:
        """Extract meeting-specific parameters."""
        params = {}

        # Extract meeting title/topic
        title_patterns = [
            r'(?:meeting|call)\s+(?:about|on|for)\s+["\']([^"\']+)["\']',
            r'titled\s*["\']([^"\']+)["\']',
            r'["\']([^"\']+)["\'](?:\s+meeting|\s+call)'
        ]

        for pattern in title_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                params["title"] = match.group(1).strip()
                break

        # Extract participants
        participant_patterns = [
            r'with\s+([A-Za-z\s,]+?)(?:\s+(?:at|on|today|tomorrow)|\s*$)',
            r'invite\s+([A-Za-z\s,]+?)(?:\s+(?:at|on|today|tomorrow)|\s*$)'
        ]

        for pattern in participant_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                participants = [p.strip() for p in match.group(1).split(',') if p.strip()]
                if participants:
                    params["participants"] = participants
                    break

        # Extract date/time (basic patterns)
        time_patterns = [
            r'at\s+(\d+(?::\d+)?(?:\s*(?:am|pm))?)',
            r'on\s+([A-Za-z]+\s+\d+(?:st|nd|rd|th)?)',
            r'today',
            r'tomorrow'
        ]

        for pattern in time_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                params["time"] = match.group(1) if match.groups() else match.group(0)
                break

        return params

    def _extract_post_params(self, request: str) -> Dict[str, Any]:
        """Extract post/update specific parameters."""
        params = {}

        # Extract post content
        content_patterns = [
            r'(?:post|share|update)\s*["\']([^"\']+)["\']',
            r'saying\s*["\']([^"\']+)["\']',
            r'["\']([^"\']+)["\']'
        ]

        for pattern in content_patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                params["content"] = match.group(1).strip()
                break

        return params

    def generate_plan(self, parsed_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an execution plan based on the parsed request."""
        if "error" in parsed_request:
            return {"error": parsed_request["error"]}

        service = parsed_request["service"]
        action = parsed_request["action"]
        params = parsed_request["params"]

        plan = {
            "service": service,
            "action": action,
            "steps": [],
            "params": params
        }

        # Create steps based on service and action
        if service in ["gmail", "outlook"]:
            plan["steps"] = self._create_email_steps(service, params)
        elif service == "skype":
            plan["steps"] = self._create_skype_steps(action, params)
        elif service in ["slack", "discord", "whatsapp", "telegram"]:
            plan["steps"] = self._create_messaging_steps(service, action, params)
        else:
            plan["steps"] = self._create_generic_steps(service, action, params)

        return plan

    def _create_email_steps(self, service: str, params: Dict[str, Any]) -> list:
        """Create steps for email sending."""
        steps = [
            {
                "action": "create_persistent_browser",
                "params": {"profile_name": f"{service}_profile"}
            },
            {
                "action": "navigate_to_service",
                "params": {"service": service}
            },
            {
                "action": "check_login_status",
                "params": {"service": service}
            }
        ]

        if params.get("to"):
            steps.append({
                "action": "send_email",
                "params": {
                    "service": service,
                    "to": params["to"],
                    "subject": params.get("subject", ""),
                    "body": params.get("body", ""),
                    "cc": params.get("cc"),
                    "bcc": params.get("bcc")
                }
            })

        return steps

    def _create_skype_steps(self, action: str, params: Dict[str, Any]) -> list:
        """Create steps for Skype actions."""
        steps = [
            {
                "action": "create_persistent_browser",
                "params": {"profile_name": "skype_profile"}
            },
            {
                "action": "navigate_to_service",
                "params": {"service": "skype"}
            },
            {
                "action": "check_login_status",
                "params": {"service": "skype"}
            }
        ]

        if action == "make_call" and params.get("contact"):
            steps.append({
                "action": "start_call",
                "params": {
                    "service": "skype",
                    "contact": params["contact"]
                }
            })
        elif action == "send_message" and params.get("contact") and params.get("message"):
            steps.append({
                "action": "send_message",
                "params": {
                    "service": "skype",
                    "contact": params["contact"],
                    "message": params["message"]
                }
            })

        return steps

    def _create_messaging_steps(self, service: str, action: str, params: Dict[str, Any]) -> list:
        """Create steps for messaging services."""
        steps = [
            {
                "action": "create_persistent_browser",
                "params": {"profile_name": f"{service}_profile"}
            },
            {
                "action": "navigate_to_service",
                "params": {"service": service}
            },
            {
                "action": "check_login_status",
                "params": {"service": service}
            }
        ]

        if action == "send_message" and params.get("contact") and params.get("message"):
            steps.append({
                "action": "send_message",
                "params": {
                    "service": service,
                    "contact": params["contact"],
                    "message": params["message"]
                }
            })

        return steps

    def _create_generic_steps(self, service: str, action: str, params: Dict[str, Any]) -> list:
        """Create generic steps for unsupported services."""
        return [
            {
                "action": "create_persistent_browser",
                "params": {"profile_name": f"{service}_profile"}
            },
            {
                "action": "navigate_to_service",
                "params": {"service": service}
            },
            {
                "action": "check_login_status",
                "params": {"service": service}
            },
            {
                "action": "perform_action",
                "params": {
                    "service": service,
                    "action": action,
                    **params
                }
            }
        ]


# Global parser instance
request_parser = RequestParser()
