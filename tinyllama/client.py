# -*- coding: utf-8 -*-

"""Zmq client interface for the TinyLlama chatbot"""

import zmq
import sys, os, json
from datetime import datetime
from tlresponse import TinyLlamaResponse

import dotenv
dotenv.load_dotenv()

class TinyLlamaClient:



    def __init__(self, name='TinyLlamaClient', user=None):
        self.name = name
        self.user = user
        self.context = zmq.Context()

        self.log = None
        if user:
            logdir = os.getenv('LOGDIR')
            if not os.path.isdir(logdir): os.mkdir(logdir)
            log = 'dialogue.%s.%s.log' % (user, datetime.now().strftime("%Y-%m-%d_%H%M%S"))
            self.log = open(os.path.join(logdir, log), 'a')

        sys.stdout.write("Connecting to TinyLlama chatbot server... ")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(os.getenv('CHATBOT_SERVER_ADDRESS'))
        handshake = self.send({'handshake': 'TinyLlamaClient'})
        print("Done." if handshake.get('handshake') == 'ok' else "Unexpected response '%s'" % handshake)

    def send(self, o):
        o['time'] = datetime.now().isoformat()
        if self.log:
            json.dump({'sending': o}, self.log)
            self.log.write(',\n')
        self.socket.send_json(o)
        r = self.socket.recv_json()
        if self.log:
            json.dump({'receiving': r}, self.log)
            self.log.write(',\n')
        return r

    def reset(self):
        r = self.send({'reset': True, 'user': self.user})
        if r.get('reset') == 'ok':
            print('Dialogue history reset')
        else:
            print('Error resetting dialoge history')

    def respond(self, s):
        response = self.send({'input': s})
        if response.get('error'):
            print("Error:", response.get('error'))
        else:
            print("Response:", response.get('output'))
        return response  # Optionally return the entire response dictionary

    def close(self):
        """Close the ZMQ socket and context."""
        self.socket.close()
        self.context.term()
        if self.log:
            self.log.close()

if __name__ == '__main__':
    user = 'Pepper'  # Provide the user name here
    client = TinyLlamaClient(user=user)
    while True:
        s = input('> ')
        if s:
            print('Response:', client.respond(s).get('output'))
        else:
            break

