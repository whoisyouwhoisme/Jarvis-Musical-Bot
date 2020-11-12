import flask
import json
from gevent.pywsgi import WSGIServer
from libraries import database_Manager
from libraries import spotify_Oauth
from bot_Mothership import proceed_Updates

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

flask_App = flask.Flask(__name__)



@flask_App.route("/")
def index():
    return flask.render_template("index.html")



@flask_App.route("/telegram_Api", methods=["GET", "POST"])
def receive_Updates():
    try:
        secret = flask.request.args["secret"] #Используем секрет для защиты

    except:
        return flask.Response(status=403)

    else:
        if secret == bot_Keys_File["telegram"]["telegram_Key"]:
            if flask.request.headers.get("content-type") == "application/json":
                json_string = flask.request.get_data().decode("utf-8")
                proceed_Updates(json_string)
                return flask.Response(status=200)
            
            else:
                return flask.Response(status=405)
        
        else:
            return flask.Response(status=403)



@flask_App.route("/spotify")
def spotify_Auth():
    try:
        auth_State = flask.request.args["state"]
        auth_Code = flask.request.args["code"]
    except:
        return flask.render_template("auth_Failed.html")
    else:
        if database_Manager.search_In_Database(auth_State, "bot_Users", "user_Unique_ID"): #Если для пользователя подготовлен уникальный ID, то продолжаем авторизацию
            spotify_Oauth.auth_User(auth_Code, auth_State)
            return flask.render_template("auth_Passed.html")

        else:
            return flask.render_template("auth_Failed.html")



if __name__ == "__main__":
    print("Web-Server launched!")
    flask_App.run(host="0.0.0.0")