
from openaichat import OaiChat

chat = OaiChat(('Your name is Pepper.','We are currently at the HUB Lab in Utrecht Unversity of applied scinece.','You are a robot.'))

while True:
    s = input('> ')
    if s:
        print(chat.history)
        print(chat.respond(s).getText())
    else:
        break

