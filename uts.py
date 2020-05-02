import json, msm

#
#   ЮНИТ ТЕСТЫ НЕ ГОТОВЫ! ТУТ БЫЛА ПРОБА
#

def testMRM():
    print('Тестирование MRM (message receiving module)...')
    print('--------------------')
    
def testMSM():
    print('Тестирование MSM (message sending module)...')
    msgList = ['СТАРТ ПРОЦЕСС',
    'СТОП ПРОЦЕСС',
    'ПОЛУЧИТЬ СТАТУС РЦ',
    'СООБЩИТЬ СОСТОЯНИЕ',
    'ПОЛУЧИТЬ РАСПИСАНИЕ',
    'КРИТИЧЕСКАЯ СИТУАЦИЯ']
    testIDIA = 1    
    for msg in msgList:
        try:
            idMSG, pathfile = msm.SendMessage(0, testIDIA, 'TEST MESSAGE', msg, 'NO PARAMETERS')
        except Exception as e:
            print(e)
        testPathfile = 'msg\\test\\msg_test_'+str(testIDIA)+'.json'
        currentFile = open(pathfile, "r", encoding='utf-8')
        testFile = open(testPathfile, "r", encoding='utf-8')
        answer = ''
        currentFileJSON = json.load(currentFile)
        testFileJSON = json.load(testFile)
        if currentFileJSON['message'] == testFileJSON['message'] and currentFileJSON['id_OIA'] == testFileJSON['id_OIA']:
            answer = 'OK'
        else:
            answer = 'ERROR'
        currentFile.close()
        testFile.close()
        testIDIA = testIDIA + 1
        print('Тест команды -', msg, answer, idMSG)
    print('--------------------')

def startTest():
    print('Система юнит-тестирования ИА-диспетчера:')
    try:
        testMRM()
        testMSM()
    except Exception as e:
        print('При проведении юнит-тестирования произошла ошибка!', e)