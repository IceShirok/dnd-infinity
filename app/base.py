
import json

"""
An interface to allow objects to be viewed in a JSON format.
This is more for testing and debugging purposes, and some
features may be replaced with objects instead.
"""
class Jsonable(object):
    def __json__(self):
        pass

    def __str__(self):
        return json.dumps(self.__json__(), indent=4, sort_keys=False)
