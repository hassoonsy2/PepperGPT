import ollama
import os
import json
from datetime import datetime
from tinyllama.tlresponse import TinyLlamaResponse

class TinyLlamaModel:
    def __init__(self, user, prompt_file=None):
        self.user = user
        self.history = self.loadPrompt(prompt_file or 'tinyllama.prompt')

    def loadPrompt(self, prompt_file):
        """Load initial conversation prompts from a file."""
        prompt_path = prompt_file if os.path.isfile(prompt_file) else os.path.join(os.path.dirname(__file__), prompt_file)
        prompts = []
        if os.path.isfile(prompt_path):
            with open(prompt_path, 'r', encoding='utf-8') as file:
                content = file.read()
                prompts.append({'role': 'system', 'content': content})
        else:
            print(f'WARNING: Unable to locate prompt file {prompt_file}')
        return prompts

    def reset(self, user, prompt=None):
        self.user = user
        self.history = self.loadPrompt(prompt or os.getenv('OPENAI_PROMPTFILE'))
        self.resetRequestLog()

    def resetRequestLog(self):
        # if (self.log): self.log.close()
        # logdir = os.getenv('LOGDIR')
        # if not os.path.isdir(logdir): os.mkdir(logdir)
        # log = 'requests.%s.%s.log'%(self.user,datetime.now().strftime("%Y-%m-%d_%H%M%S"))
        # self.log = open(os.path.join(logdir,log),'a')
        # print('Logging requests to',log)
        pass

    def respond(self, input_text):
        self.history.append({'role': 'user', 'content': input_text})
        response_content = ''

        try:
            stream = ollama.chat(model='tinyllama', messages=self.history, stream=True)
            for chunk in stream:
                response_content += chunk['message']['content']
                if chunk.get('done', False):
                    break
        except Exception as e:
            print(f"Error during model response generation: {str(e)}")
            response_content = "Sorry, I couldn't process that due to an error."

        # Ensure TinyLlamaResponse is returned regardless of path taken
        final_response = TinyLlamaResponse(json.dumps({'text': response_content}))

        self.history.append({'role': 'assistant', 'content': response_content})

        return final_response


# Example usage
if __name__ == '__main__':


    model = TinyLlamaModel(user='Pepper', prompt_file='tinyllama.prompt')
    print("TinyLlamaModel initialized. Type something to chat!")
    while True:
        try:
            input_text = input('> ')
            if input_text.strip():
                response = model.respond(input_text)
                print(response)
            else:
                print("Restarting conversation.")
                model.reset()  # Optionally reset the conversation
        except KeyboardInterrupt:
            print("\nExiting TinyLlamaModel chat.")
            break
