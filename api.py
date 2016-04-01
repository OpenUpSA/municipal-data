from flask import Flask
app = Flask(__name__)


from flask import Flask
from sqlalchemy import create_engine
from babbage.manager import JSONCubeManager
from babbage.api import configure_api

app = Flask('demo')
engine = create_engine('postgresql://localhost/procurement')
models_directory = 'models/'
manager = JSONCubeManager(engine, models_directory)
blueprint = configure_api(app, manager)
app.register_blueprint(blueprint, url_prefix='/api/babbage')


if __name__ == "__main__":
    app.run()
