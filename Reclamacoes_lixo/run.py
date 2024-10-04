from flask import Flask
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
csrf = CSRFProtect(app)


from app.controllers.index import *
from app.controllers.login import *      


if __name__ == '__main__':
    app.run(debug=True)