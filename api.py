from flask import Flask
import logging

app = Flask(__name__)


from flask import Flask
from sqlalchemy import create_engine
from babbage.manager import JSONCubeManager
from babbage.api import configure_api

app = Flask('demo')
loghandler = logging.StreamHandler()
loghandler.setLevel(logging.DEBUG)
app.logger.addHandler(loghandler)
engine = create_engine('postgresql://postgres@localhost/municipal_finance')
models_directory = 'models/'
manager = JSONCubeManager(engine, models_directory)
blueprint = configure_api(app, manager)
app.register_blueprint(blueprint, url_prefix='/api')


if __name__ == "__main__":
    app.run()
    app.logger.warning('A warning message is sent.')
    app.logger.error('An error message is sent.')
    app.logger.info('Information: 3 + 2 = %d', 5)
