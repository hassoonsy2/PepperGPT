import ollama
from ollama import Client
import os

from datetime import datetime
from tinyllama.tlresponse import TinyLlamaResponse
import os, sys, codecs, json
import dotenv
dotenv.load_dotenv()

if sys.version_info[0] < 3:
    raise ImportError('LLAMA Chat requires Python 3')


# Todo : fix the straming issue and the logging !
class TinyLlamaModel:
    def __init__(self,user,prompt=None):
        self.log = None
        self.reset(user,prompt)
        self.client = Client(host='http://localhost:11434')


    def reset(self,user,prompt=None):
        self.user = user
        self.history = self.loadPrompt(prompt or os.getenv('LLAMA_PROMPTFILE'))
        self.resetRequestLog()


    def resetRequestLog(self):
        # if (self.log): self.log.close()
        # logdir = os.getenv('LOGDIR')
        # if not os.path.isdir(logdir): os.mkdir(logdir)
        # log = 'requests.%s.%s.log'%(self.user,datetime.now().strftime("%Y-%m-%d_%H%M%S"))
        # self.log = open(os.path.join(logdir,log),'a')
        # print('Logging requests to',log)
        pass

    def loadPrompt(self,promptFile):
        promptFile = promptFile or 'tinyllama.prompt'
        promptPath = promptFile if os.path.isfile(promptFile) else os.path.join(os.path.dirname(__file__),promptFile)
        prompt = [] # [{"role": "system", "content": "You are a helpful robot designed to output JSON."}]
        if not os.path.isfile(promptPath):
            print('WARNING: Unable to locate tinyllama prompt file',promptFile)
        else:
            with codecs.open(promptPath,encoding='utf-8') as f:
                prompt.append({'role':'system','content':f.read()})
        return prompt



    def respond(self, inputText):
        start = datetime.now()
        self.moderation = None
        #moderator = Thread(target=self.getModeration,args=(inputText,))
        #moderator.start()
        self.history.append({'role':'user','content':inputText})
        response = self.client.chat(
        model="tinyllama",
        messages=self.history,
        options = {'num_ctx': 20,'temperature' : 0.9,'num_predict':30},

        )
        print(response['message']['content'])
        print(response)
        r = TinyLlamaResponse(response)

        self.history.append({'role':'assistant','content':r.getText()})
        print('Request delay',datetime.now()-start)
        return r


# Example usage
if __name__ == '__main__':

    chat = TinyLlamaModel(user='TinyLlama')

    while True:
        try:
            s = input('> ')
        except KeyboardInterrupt:
            break
        if s:
            print(chat.history)
            print(chat.respond(s).getText())
        else:
            break
    print('Closing tinyllama Server')