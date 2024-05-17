import qi
import sys


def main(app):
    try:
        session = app.session
        tabletService = session.service("ALTabletService")

        # Replace <your-laptop-ip> and <port> with your laptop's IP address and port number
        webpage_url = "http://192.168.1.219 :8000/index.html"

        tabletService.showWebview(webpage_url)

        app.run()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    ip = "192.168.1.140"  # the IP of the robot
    port = 9559

    try:
        connection_url = "tcp://{}:{}".format(ip, port)
        app = qi.Application(url=connection_url)
        app.start()
    except RuntimeError:
        print("Can't connect to Naoqi.")
        sys.exit(1)
    main(app)
