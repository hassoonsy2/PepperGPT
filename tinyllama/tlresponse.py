# -*- coding: utf-8 -*-

import json

# Assume moderation or flagging is handled by the server, which includes a 'flagged' field in responses
class TinyLlamaResponse:
    def __init__(self, response):
        """Initialize with a JSON response from TinyLlama."""
        self.response = json.loads(response) if isinstance(response, str) else response

    def is_flagged(self):
        """Simulate a check for flagged content based on a response field."""
        # This assumes there's a 'flagged' field in the response dict
        return self.response.get('flagged', False)

    def getText(self):
        """Extract text from the response, checking for flagged content."""
        if self.is_flagged():
            return "This conversation is going nowhere."
        else:
            # Assuming response structure has a 'text' or similar field
            return self.response.get('text', '').strip()

    def flagged_response(self):
        """Provide a standard response if the content is flagged."""
        if self.is_flagged():
            return "This conversation is going nowhere."
