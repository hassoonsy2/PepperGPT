# -*- coding: utf-8 -*-

"""Zmq client interface for the TinyLlama chatbot"""

import zmq
import sys, os, json
from datetime import datetime
from tlresponse import TinyLlamaResponse
import dotenv

dotenv.load_dotenv()

if sys.version_info[0] > 2:
    raw_input = input

class TinyLlamaClient:



    def __init__(self, name='TinyLlamaClient', user=None):
        self.name = name
        self.user = user
        self.context = zmq.Context()

        self.log = None
        if user:
            logdir = os.getenv('LOGDIR')
            if not os.path.isdir(logdir): os.mkdir(logdir)
            log = 'dialogue.%s.%s.log'%(user,datetime.now().strftime("%Y-%m-%d_%H%M%S"))
            self.log = open(os.path.join(logdir,log),'a')

        sys.stdout.write("Connecting to LLAMA chatbot server... ")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(os.getenv('CHATBOT_SERVER_ADDRESS'))
        handshake = self.send({'handshake':self.name})
        print("Done." if handshake.get('handshake') == 'ok' else "Unexpected response '%s'"%handshake)


    def send(self,o):
        o['time'] = datetime.now().isoformat()
        if self.log:
            json.dump({'sending':o},self.log)
            self.log.write(',\n')
        self.socket.send_json(o)
        r = self.socket.recv_json()
        if self.log:
            json.dump({'receiving':r},self.log)
            self.log.write(',\n')
        return r

    def reset(self):
        r = self.send({'reset':True,'user':self.user})
        if r.get('reset') == 'ok':
            print('Dialogue history reset')
        else:
            print('Error resetting dialoge history')


    def respond(self,s):
        return TinyLlamaResponse(self.send({'input':s})).getText()


if __name__ == '__main__':
    client = TinyLlamaClient(('Your name is Pepper.','We are currently at the Hub Lab at HU.','You are a robot.'))
    while True:
        s = raw_input('> ')
        if s:
            print('Response: ' + client.respond(s).getText())
        else:
            break