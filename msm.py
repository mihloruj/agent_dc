import json, datetime as dt, random


# Генерация уникального ID в системе
# СЕЙЧАС ID НАСТРОЕН КАК ТЕКСТОВАЯ ВРЕМЕННАЯ МЕТКА. ПРИ ПРОДЕ ИСПРАВИТЬ НА INT
def generateUniqID():
    date = dt.datetime.now().strftime("%Y%m%d.%H-%M-%S.")
    uniqPart = random.randint(100, 999)
    return date+str(uniqPart)

# Отправка сообщения
def SendMessage(id_IIA, id_OIA, type_message, message, parameters):
    try:
        _id = generateUniqID()
        pathfile = 'msg\\out\\msg_'+str(_id)+'.json'
        with open(pathfile, "w", encoding='utf8') as f:
            json.dump({"id": _id,
            "id_IIA": id_IIA,
            "id_OIA": id_OIA,
            "type_message": type_message,
            "message": message,
            "parameters": parameters},f,ensure_ascii=False)
        return _id, pathfile
    except:
        return _id