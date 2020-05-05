import json, datetime, time
import agent

#   Обработка сообщений типа system
def systemMSG(textMSG):
    if textMSG == 'ON':
        agent.changeStatus('WORK')
    elif textMSG == 'OFF':
        agent.changeStatus('SLEEP')

#   Обработка сообщений типа control
def controlMSG(textMSG, paramsMSG):
    if textMSG == 'FINISH WORK':
        agent.finishWorkProc(textMSG, paramsMSG)
    else:
        agent.manageWc(textMSG, paramsMSG)

#   Обработка сообщений типа manage
def manageMSG(textMSG, paramsMSG):
    if textMSG == 'SCHEDULE READY':
        agent.loadSchedule(paramsMSG)
    elif  textMSG == 'LIST WC READY':
        agent.loadListWC(paramsMSG)

#   Обработка неопознанных сообщений
def nontypeMSG(idFrom):
    agent.unrecognizedCommand(idFrom)

#   Обработчик-парсер входящих сообщений
def receiveMessage(message):
    idFromMSG = message['id_IIA']
    typeMSG = message['type_message']
    textMSG = message['message']
    paramsMSG = message['parameters']
    if typeMSG == 'manage':
        manageMSG(textMSG, paramsMSG)
    elif typeMSG == 'control':
        controlMSG(textMSG, paramsMSG)
    elif typeMSG == 'system':
        systemMSG(textMSG)
    else:
        nontypeMSG(idFromMSG)

