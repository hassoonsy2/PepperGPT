# -*- coding: utf-8 -*-

import json

# Assume moderation or flagging is handled by the server, which includes a 'flagged' field in responses
class TinyLlamaResponse:
    def __init__(self, response):
        """Initialize with a JSON response from TinyLlama."""
        self.json = json.loads(response) if isinstance(response,str) else response
        # self.response = json.loads(response) if isinstance(response, str) else response

    def flagged(self):
        return hasattr(self,'moderation') and self.moderation['results'][0]['flagged']

    def getText(self):
        if self.flagged():
            return "This conversation is going nowhere."
        else:
            print(self.json, 'its json')
            return self.json['message']['content'].strip()

    def flaggedResponse(self):
        #categories = self.json['results'][0]['categories']
        #for key,val in categories.items():
        #  if val:
        #    return self.responses[key]
        if self.flagged():
            return "This conversation is going nowhere."
