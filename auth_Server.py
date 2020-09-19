import flask
from gevent.pywsgi import WSGIServer
from libraries import database_Manager
from libraries import spotify_Oauth



flask_App = flask.Flask(__name__)



@flask_App.route('/spotify')
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



print("Auth-Server launched!")



http_server = WSGIServer(("0.0.0.0", 8000), flask_App)
http_server.serve_forever()