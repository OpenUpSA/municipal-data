from django.conf import settings
from sqlalchemy import create_engine
from babbage.manager import JSONCubeManager

engine = create_engine(settings.DATABASE_URL)
models_directory = 'models/'

cube_manager = JSONCubeManager(engine, models_directory)
