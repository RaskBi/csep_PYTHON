import random
import string

def randomnum(length):
    # choose from all lowercase letter
    numbers = string.digits
    # print(numbers)
    result_str = ''.join(random.choice(numbers) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str

def randomstr(length):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    return random_string

def cbxModel(model, value= False, name= None):
    list = []
    for data in model:
        jdata = {
            "value": data.pk,
            "label": data.label_cbx()
        }
        if value:
            jdata.__setitem__(name, data.valor)
        list.append(jdata)
    return list

def cbxModelObject(model, value= False, name= None):
    if model is None:
        print("None")
        return {
            "value": None,
            "label": ""
        }
    jdata={
        "value": model.pk,
        "label": model.label_cbx()
    }
    if value:
            jdata[name]= model.valor
    return jdata


def cbxtovalue(obj:dict):
    if obj is None:
        return None
    return obj.get("value")


def rgba():
    # Generar valores aleatorios para los componentes RGB
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return f"rgba({red}, {green}, {blue}, 0.7)"