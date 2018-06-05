from AirSimClient import *

class VividClient(AirSimClientBase, object):
    def __init__(self, ip="127.0.0.1", port=16612, timeout=3000):
        super(VividClient, self).__init__(ip, port, timeout)
        
    def moveByDistance(self, dx, dy, dz):
        return self.client.call('moveByDistance', dx, dy, dz)
    
    def turnByDegree(self, degree):
        return self.client.call('turnByDegree', degree)
    
    def isHit(self):
        return self.client.call('isHit')
    
    def getPosition(self):
        return self.client.call('getPosition')

    def reset(self):
        return self.client.call('reset')

    def createMapObject(self, type_id, x, y, z):
        return self.client.call('createMapObject', type_id, x, y, z)


class VividMapObjectType:
    Chair = 0
    Table = 1
    BookShelves = 2
    Door = 3
    Stairs = 4
    Fire = -1


