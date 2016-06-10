from django.conf import settings
from sqlalchemy import create_engine
from babbage.manager import JSONCubeManager

engine = create_engine(settings.DATABASE_URL)
models_directory = 'models/'


class PreloadingJSONCubeManager(JSONCubeManager):
    """A simple extension of a JSONCubeManager initialising and caching all
    cubes on construction"""

    def __init__(self, engine, directory):
        super(PreloadingJSONCubeManager, self).__init__(engine, directory)
        self._cubes = {}
        self._models = {}
        self._cube_names = set(super(PreloadingJSONCubeManager, self).list_cubes())
        for name in self._cube_names:
            self._models[name] = super(PreloadingJSONCubeManager, self).get_cube_model(name)
            self._cubes[name] = super(PreloadingJSONCubeManager, self).get_cube(name)
            # Hack to cheaply force babbage to read and cache tables
            # Do some query that hits all tables in the cube but cut on
            # something that probably doesn't exist to minimize the rows
            # counted for the result
            for dname, dimension in self._models[name]['dimensions'].iteritems():
                for aname, attribute in dimension['attributes'].iteritems():
                    if attribute['type'] == 'string':
                        someref = "%s.%s" % (dname, aname)
            self._cubes[name].facts(page_size=1, cuts=someref + ':dummy')

    def list_cubes(self):
        return self._cube_names

    def has_cube(self, name):
        return name in self._cube_names

    def get_cube(self, name):
        return self._cubes[name]

    def get_cube_model(self, name):
        return self._models[name]

_cube_manager = None


def get_manager():
    global _cube_manager
    if _cube_manager is None:
        _cube_manager = PreloadingJSONCubeManager(engine, models_directory)
    return _cube_manager
