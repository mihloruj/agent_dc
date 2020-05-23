from serverlib.server import Server
from threading import Thread
import time, json, datetime as dt, random 
import mrm, agent

# Настройки адреса агента
HOST = 'localhost'
PORT = 8889

# Настройки адреса коммуникатора
CMHOST = 'localhost'
CMPORT = 8887

AGENT = None

# Класс обработки входящих сообщений, для работы требуется модуль-парсер mrm.py
class Agent(Server):

    def handle(self, message):
        try:
            mrm.receiveMessage(json.loads(str(message, 'ascii')))
        except Exception as e:
            print("Error recmsg: {}".format(e))

# Генерация уникального ID в системе
def generateUniqID():
    date = dt.datetime.now().strftime("%d%m%Y%H%M%S")
    uniqPart = random.randint(100, 999)
    return date+str(uniqPart)

# Отправка сообщения
def SendMessage(id_IIA, id_OIA, type_message, message, parameters):
    try:
        _id = generateUniqID()
        msg = {"id": _id,
        "id_IIA": id_IIA,
        "id_OIA": id_OIA,
        "type_message": type_message,
        "message": message,
        "parameters": parameters}
        AGENT.send(CMHOST, CMPORT, json.dumps(msg))
        print(msg)
    except Exception as e:
        print("Error sendmsg: {}".format(e))

if __name__ == "__main__":
    try:
        app = Agent(HOST, PORT)
        app.start_server()
        agent.startAgent(app)
        app.loop()
        app.stop_server()
    except Exception as e:
        print("Error: {}".format(e))
