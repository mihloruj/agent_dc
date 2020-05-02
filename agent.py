import json, sys, time, datetime as dt
from threading import Thread
import msm, mrm, uts 
from collections import defaultdict

# log = open("agent.log", "a")
# sys.stdout = log

# AGENT - текущий основной скрипт 
# MSM (message sending module) - модуль ответственный за отправку сообщений
# MRM (message receiving module) - модуль ответственный за прием сообщений
# UTS (unit testing system) - модуль ответственный за юнит-тестирование

UNITTEST = False
SELFID = 'IADC'
STATUS = 'SLEEP'
    # SLEEP - Ожидание выполнения команд, агент не работает 
    # WORK - Агент работает, может получать команды
TIMING_STATUS = 25
TIMING_CHECK_WC = 10
SCHEDULE = ''
LISTWC = ''
NOPARAMS = 'NO PARAMETERS'
TRUST_LEVEL = 2
    # 0 - агент не может сам принимать решения
    # 1 - агент может принимать некоторые решения
    # 2 - агент полностью принимает решения
DISPATCHPROC = defaultdict(list)
QUEUEPROCS = defaultdict(list)

# Коды агентов в системе
# IACM - коммуникатор
# IACN - контролер
# IAPL - планировщик
# IADC - диспетчер
# IAWC - рабочий центр

#   Обработка неопознанных сообщений 
def unrecognizedCommand(id):
    msm.SendMessage(SELFID, 'IACM', 'system', 'NONETYPEMSG FROM '+id, NOPARAMS)
    print('WARNING: Не удалось распознать команду', id)

#   Изменение статуса агента
def changeStatus(status):
    global STATUS 
    STATUS = status
    if STATUS == 'WORK':
        msm.SendMessage(SELFID, 'IACM', 'system', 'IADC '+status, NOPARAMS)
    print('SYSTEM: Агент переведен в режим:', STATUS)

#   Отображение статуса
def sendStatus():
    while True:
        msm.SendMessage(SELFID, 'IACM', 'system', 'STATUS '+ STATUS, NOPARAMS)
        print('INFO: Статус агента', STATUS)
        time.sleep(TIMING_STATUS)

#   Запрос расписания
def requestSchedule():
    msm.SendMessage(SELFID, 'IAPL', 'manage', 'MAKE SCHEDULE', dt.datetime.date)
    print('INFO: Запрос расписания')

#   Получение расписания
def loadSchedule(schedule):
    global SCHEDULE
    SCHEDULE = schedule
    print('INFO: Расписание получено', SCHEDULE, len(SCHEDULE))
    if len(SCHEDULE) != 0:
        startProcThread = Thread(target=startWorkProc)
        startProcThread.start()
    else:
        print('WARNING: В расписании не обнаружены задачи')

#   Запрос списка обслуживаемых РЦ
def requestListWC():
    msm.SendMessage(SELFID, 'IAPL', 'manage', 'GET LIST WC', dt.datetime.date)
    print('INFO: Запрос списка обслуживаемых РЦ')

#   Получение списка обслуживаемых РЦ
def loadListWC(listwc):
    global LISTWC
    LISTWC = listwc
    print('INFO: Список обслуживаемых РЦ получен', LISTWC)

#   Выдача команды для РЦ
def sendCommandToWC(idWC, procname, command):
    msm.SendMessage(SELFID, 'IAWC', 'control', command, 'IDWC '+str(idWC)+' PROCNAME '+procname)
    print('MANAGEWC: Выдача команды',command, procname,'для РЦ', idWC)

#   Запуск работы процессов
def startWorkProc():
    global DISPATCHPROC
    global QUEUEPROCS
    if len(LISTWC) > 0:
        while True:
            for task in SCHEDULE:
                for wc in LISTWC:
                    if task['IAWCID'] == wc['id']:
                        if len(DISPATCHPROC[task['IAWCID']]) < 1:
                            sendCommandToWC(task['IAWCID'], task['procname'], 'START')
                            DISPATCHPROC[task['IAWCID']].append(task['procname'])
                            print('MANAGEWC: Процесс', task['procname'], 'добавлен в список отслеживаемых процессов')
                        else:
                            if not task['procname'] in QUEUEPROCS[task['IAWCID']] and not task['procname'] in DISPATCHPROC[task['IAWCID']]:
                                QUEUEPROCS[task['IAWCID']].append(task['procname'])
                                print('MANAGEWC: Процесс', task['procname'], 'поставлен в очередь')
            time.sleep(TIMING_CHECK_WC)
    else:
        print('WARNING: Список обслуживаемых РЦ не загружен')

#   Реакция на корректное завершение работы процесса
def finishWorkProc(msg, params):
    infostr = str(params['idWC'])+' '+str(params['procname'])
    if DISPATCHPROC.get(params['idWC']) != None:
        del DISPATCHPROC[params['idWC']]
        for task in SCHEDULE:
            if task['IAWCID'] == params['idWC'] and task['procname'] == params['procname']:
                SCHEDULE.remove(task)
                print('MANAGEWC: Процесс',infostr,'успешно завершился за', params['time'])
        print('MANAGEWC: Процесс',infostr, 'удален из списка отслеживаемых процессов')
    else:
        print('ERROR: Процесс',infostr,'не удален из списка отслеживаемых процессов')

#   Реакция на внештатную работу процесса
def manageWc(msg, params):
    infostr = str(params['idWC'])+' '+str(params['procname'])
    if msg == 'WARNING' and TRUST_LEVEL >= 0:
        print('MANAGEWC: Процесс', infostr,'не стабилен')
    elif msg == 'EXCESS' and TRUST_LEVEL < 2:
        print('MANAGEWC: Процесс', infostr,'вышел за рамки')
    elif msg == 'EXCESS' and TRUST_LEVEL == 2:
        try:
            sendCommandToWC(params['idWC'], params['procname'], 'STOP')
            print('MANAGEWC: Процесс',infostr,'вышел за рамки и был остановлен')
            if DISPATCHPROC.get(params['idWC']) != None:
                del DISPATCHPROC[params['idWC']]
                for task in SCHEDULE:
                    if task['IAWCID'] == params['idWC'] and task['procname'] == params['procname']:
                        SCHEDULE.remove(task)
                print('MANAGEWC: Процесс',infostr, 'удален из списка отслеживаемых процессов')
            else:
                print('ERROR: Процесс',infostr,'не удален из списка отслеживаемых процессов')
        except Exception as e:
            print('ERROR: Ошибка при остановке процесса',infostr, e)

#   Запуск тестирования
def testSystem():
    uts.startTest()
    print('INFO: Производится тестирование работы агента')

#   Старт агента
def startAgent():
    print('SYSTEM: Агент запускается...')
    try:
        if UNITTEST:
            testSystem()
        else:
            print('SYSTEM: Юнит-тестирование отключено!')
        statusThread = Thread(target=sendStatus)
        time.sleep(2)
        print('SYSTEM: Агент успешно запустился!')
        statusThread.start()
    except:
        print('ERROR: Агенту не удалось запуститься!')