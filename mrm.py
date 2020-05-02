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
def receiveMessage(filepath):
    with open(filepath, "r", encoding='utf-8') as jsonfile:
        message = json.load(jsonfile)
    if message['id_OIA'] == 'IADC':
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

if __name__ == "__main__":
    timing = 3
    agent.startAgent()
    # адовая чепуха = аналог юнитов
    # чисто чтобы тестить всю систему
    time.sleep(timing)
    receiveMessage('msg\\in\\msg_start_work.json')
    time.sleep(timing)
    agent.requestListWC()
    receiveMessage('msg\\in\\msg_list_wc.json')
    time.sleep(7)
    receiveMessage('msg\\in\\msg_nonetype.json')
    time.sleep(15)
    agent.requestSchedule()
    receiveMessage('msg\\in\\msg_scheduleNew.json')
    time.sleep(timing)
    receiveMessage('msg\\in\\msg_wc_command_warning.json')
    time.sleep(20)
    receiveMessage('msg\\in\\msg_wc_command_excess.json')
    time.sleep(40)
    receiveMessage('msg\\in\\msg_wc_command_finish.json')
    time.sleep(10)
    receiveMessage('msg\\in\\msg_wc_command_finish1.json')
    time.sleep(20)
    receiveMessage('msg\\in\\msg_wc_command_finish2.json')
    time.sleep(timing)
    receiveMessage('msg\\in\\msg_stop_work.json')
    print('ТЕСТОВЫЙ ВАРИАНТ РАБОТЫ ЗАВЕРШЕН')
    