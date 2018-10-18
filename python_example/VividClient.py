import time

from AirSimClient import *

# make sure that each call is completed
def delay(seconds=0.1):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            time.sleep(seconds)
            return result
        return wrapper
    return decorator

class VividClient(AirSimClientBase, object):
    def __init__(self, ip="127.0.0.1", port=16612, timeout=10):
        self.config = {'ip': ip, 'port': port, 'timeout_value': timeout}
        self._connect()

    def _connect(self):
        super(VividClient, self).__init__(**self.config)
        
    @delay()
    def moveByDistance(self, dx, dy, dz):
        return self.client.call('moveByDistance', dx, dy, dz)
    
    @delay()
    def turnByDegree(self, degree):
        return self.client.call('turnByDegree', degree)

    @delay()
    def setLocation(self, x, y, z):
        return self.client.call('setLocation', x, y, z)

    @delay()
    def resetLocation(self):
        return self.client.call('resetLocation')
    
    def isHit(self):
        return self.client.call('isHit')

    def getLocation(self):
        return self.client.call('getLocation')

    def getRotation(self):
        return self.client.call('getRotation')

    @delay()
    def createMapObject(self, type_id, x, y, z):
        return self.client.call('createMapObject', type_id, x, y, z)
    
    def loadMap(self, map_id):
        res = self.client.call('loadMap', map_id)
        time.sleep(0.1)
        self._connect()
        return res
    
    def getMapNames(self):
        return self.client.call('getMapNames')

    # "reset" has no effect, use "loadMap" instead
    def reset(self):
        raise NotImplementedError


class VividMapObjectType:
    Chair = 0
    Table = 1
    BookShelves = 2
    Door = 3
    Stairs = 4
    Fire = -1
