import json
import abc


class Jsonable(abc.ABC):
    """
    Create an interface to force objects to implement a JSON method
    for debugging purposes
    """
    @abc.abstractmethod
    def __json__(self):
        pass

    def __str__(self):
        return json.dumps(self.__json__())
