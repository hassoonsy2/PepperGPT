# -*- coding: utf-8 -*-


from oaichat.oaiserver import OaiServer
from optparse import OptionParser
from tinyllama.tinyllamaserver import TinyLlamaServer

parser = OptionParser()
parser.add_option("--prompt",
    help="Path to propot file.",
    dest="prompt")
parser.add_option("--server",
                  help="Server to use (tinyllama or openai).",
    dest="server")
parser.set_defaults(server='openai')
parser.set_defaults(prompt='pepper')
  
if __name__ == '__main__':
    (opts, args_) = parser.parse_args()
    if opts.server == 'tinyllama':
        server = TinyLlamaServer(user='User 1',prompt=opts.prompt + '.prompt')
    else:
        server = OaiServer(user='User 1',prompt=opts.prompt + '.prompt')

    try:
        server.start()
        while True:
            s = input('> ')
            if s.lower() == 'exit':
                break
            elif s.lower() == 'history':
                for item in server.history:
                    print(f"{item['role']}: {item['content']}")
            else:
                response_object = server.respond(s)
                print(response_object.getText())
    finally:
        server.stop()


    