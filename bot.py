import json
import requests
from serverlib.server import Server


class Bob(Server):

    def handle(self, message):
        try:
            print("Got: {}".format(message))
        except Exception as e:
            print("Error: {}".format(e))


if __name__ == "__main__":
    print("Заглушка агента запустилась - имитация коммуникатора")

    getter = Bob("localhost", 8887)
    getter.start_server()
    getter.loop()
    getter.stop_server()
