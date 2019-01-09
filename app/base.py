
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


"""
An interface to add two functions for users to input custom
information into the object. This is more going to be manipulated
by whatever factory is constructing the object.
"""
class Requireable(object):
    def _required_customization(self):
        """
        Return a list of features that need to be fulfilled in order for
        the verify function to not spit out fire and brimstone.
        This should be a list of JSON objects.
        """
        return []

    def _verify(self):
        """
        This function serves to make sure that the race, with its inputs,
        is considered valid. In most cases, this applies for races that
        requires selecting a feature amongst a selection (i.e. select a
        skill proficiency from a list of 3).
        Return true if all verification has passed, or throw an exception
        (ValueError?) with a message saying what is invalid.
        """
        return True
