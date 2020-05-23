import json
import requests
from serverlib.server import Server
import agent


class UTS(Server):

    def handle(self, message):
        try:
            print("Got: {}".format(message))
        except Exception as e:
            print("Error: {}".format(e))


def testing(test, uts):
    print(test['NameTest'])
    for command in test['Commands']:
        pass

def loadScenario():
    try:
        with open('scenario.json') as f:
            scenario = json.load(f)
            print('Сценарий успешно загружен')
            return scenario
    except Exception as e:
        print("Error: {}".format(e))
        return None


if __name__ == "__main__":
    print("Система юнит-тестирования")
    scenario = loadScenario()
    if scenario != None:
        for test in scenario:
            testing(test, uts)
    uts = UTS("localhost", 8887)
    uts.start_server()
    uts.loop()
    uts.stop_server()
