import requests, json, os, socketserver
from flask import Flask, jsonify, request, make_response
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
file_path = "src/backend/database.json"     

def jsonValueCheck():
    try:   
        with open(file_path, "r") as file:
            existing_data = json.load(file)
        # print("Уже существующая дата в базе данных", existing_data) 
        return existing_data
    except ValueError as ve:
        # print("Ошибка, джсон пустой")
        existing_data = []
        with open(file_path, 'w') as file: 
            json.dump(existing_data, file)
        return existing_data

# Функция проверки одинаковых почт
def checkEmail(existing_data, data):
    for user in existing_data:
        if desired_key in user:
            if user["email"]==data["email"]: 
                
                return True
            else:  
                print('Keys does not match, continuing process') 
        else:
            print("Desired key has not been found, please ensure that your database is not broken") 
    return False 


def login(existing_data, data): 
    for user in existing_data:
        if "email" in user:
            if user["email"]==data["email"] and user["pass"]==data["pass"]: 
                
                return True
            else:  
                print('Keys does not match, continuing process') 
        else:
            print("Desired key has not been found, please ensure that your database is not broken") 
    return False 


def updateJsonData():
    existing_data = jsonValueCheck()
    data = request.get_json()
    match_value = checkEmail(existing_data, data)  

    # Проверка на одинаковую почту
    print(match_value)

    # Записываем нового юзера в массив users
    if match_value==False:
        existing_data.append(data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=2) 
        
        return True
    # Если пользователь не зарегестрирован - ответ False
    else:       
        return False
    
def userLogin():
    existing_data = jsonValueCheck()
    data = requestGetData()
    match_value = login(existing_data, data)

    print(match_value)

    if match_value==True:
        print('email does match')
        return True
    else: 
        return False

def requestGetData():
    # Получение значения query-параметра "param1"
    email_value = request.args.get('email')

    # Получение значения query-параметра "param2" (если он присутствует, иначе используется значение по умолчанию)
    pass_value = request.args.get('pass') 

    user = {
        "email": email_value,
        "pass": pass_value
    }

    return user


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle POST request data
        response = make_response(jsonify(str(updateJsonData()))) 
       
        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = "application/json"
        return response
    elif request.method == 'GET':
        response = make_response(jsonify(str(userLogin())))

        response.headers['Access-Control-Allow-Origin'] = '*' 
        response.headers['Content-Type'] = "application/json"
        return response
    else:
        print('Method is not supported')


if __name__ == "__main__":
    app.run(debug=True)
# Load data from the JSON file


# response = requests.get("")
# print("Статус код:", response.status_code)
# print("Текст ответа:", response.text)
