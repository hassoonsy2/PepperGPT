import time

import zmq
import os
import json
import datetime
from threading import Thread, Event
from tinyllama.models import TinyLlamaModel

class TinyLlamaServer(TinyLlamaModel):
    def __init__(self, user, prompt=None):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)  # REP socket for request-reply pattern
        self.socket.bind('tcp://*:' + os.getenv('CHATBOT_SERVER_ADDRESS').split(':')[-1])
        self.thread = None
        self.shutdown_flag = Event()
        self.model = TinyLlamaModel(user,prompt)  # Initialize the model
        self.history = []


    def start(self):
        print("TinyLlamaServer started and awaiting requests...")
        self.thread = Thread(target=self._run)
        self.thread.start()

    def _run(self):
        print('LLAMA TIny')
        while self.thread:
            response = {}
            i = self.listen()
            print('Input received:', i)
            if 'handshake' in i:
                print('New client connected:', i['handshake'])
                response['handshake'] = 'ok'
            if 'reset' in i and i['reset']:
                print('Resetting history.')
                self.reset(i['user'])
                response['reset'] = 'ok'
            if 'history' in i:
                print('Extending history:')
                for row in i['history']:
                    print('\t' + row.strip())
                    self.history.append(row.strip())
                response['history'] = 'ok'
            if 'input' in i:
                r = self.respond(i['input'])
                print(r.type())
                for k, v in r.json.items():
                    response[k] = v
            response['time'] = datetime.datetime.now().isoformat()
            print('Sending response:', response)
            self.send(response)

    def stop(self):
        self.socket.close()
        self.thread = None
        # self.log.close()

    def send(self,s):
        return self.socket.send_json(s)

    def listen(self):
        #  Wait for next request from client
        return self.socket.recv_json()

if __name__ == '__main__':
    server = TinyLlamaServer(user='Pepper')
    try:
        server.start()
        input("Press Enter to stop the server...\n")
    finally:
        server.stop()