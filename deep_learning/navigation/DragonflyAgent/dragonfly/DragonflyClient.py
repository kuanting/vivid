from __future__ import print_function
import msgpackrpc #install as admin: pip install msgpack-rpc-python
import numpy as np #pip install numpy
import msgpack
import math
import time
import sys
import os
import inspect
import types
import re

class MsgpackMixin:
    def to_msgpack(self, *args, **kwargs):
        return self.__dict__ #msgpack.dump(self.to_dict(*args, **kwargs))

    @classmethod
    def from_msgpack(cls, encoded):
        obj = cls()
        obj.__dict__ = {k.decode('utf-8'): v for k, v in encoded.items()}
        return obj

class Vector3r(MsgpackMixin):
    x_val = np.float32(0)
    y_val = np.float32(0)
    z_val = np.float32(0)

    def __init__(self, x_val = np.float32(0), y_val = np.float32(0), z_val = np.float32(0)):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
		
class Quaternionr(MsgpackMixin):
    w_val = np.float32(0)
    x_val = np.float32(0)
    y_val = np.float32(0)
    z_val = np.float32(0)

    def __init__(self, x_val = np.float32(0), y_val = np.float32(0), z_val = np.float32(0), w_val = np.float32(1)):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        self.w_val = w_val
		
class AirSimImageType:    
    Scene = 0
    DepthMeters = 1
    DepthVis = 2
    DisparityNormalized = 3
    Segmentation = 4
    SurfaceNormals = 5

class ImageRequest(MsgpackMixin):
    camera_id = np.uint8(0)
    image_type = AirSimImageType.Scene
    pixels_as_float = False
    compress = False

    def __init__(self, camera_id, image_type, pixels_as_float = False, compress = True):
        self.camera_id = camera_id
        self.image_type = image_type
        self.pixels_as_float = pixels_as_float
        self.compress = compress


class ImageResponse(MsgpackMixin):
    image_data_uint8 = np.uint8(0)
    image_data_float = np.float32(0)
    camera_position = Vector3r()
    camera_orientation = Quaternionr()
    time_stamp = np.uint64(0)
    message = ''
    pixels_as_float = np.float32(0)
    compress = True
    width = 0
    height = 0
    image_type = AirSimImageType.Scene


class DragonflyClient:
    def __init__(self, ip="127.0.0.1", port=41451):
        self.client = msgpackrpc.Client(msgpackrpc.Address(ip, port), timeout = 5)
        
    # basic flight control
    def moveByDistance(self, dx, dy, dz):
        result = self.client.call('moveByDistance', dx, dy, dz)
        time.sleep(0.1)
        return result

    def turnByDegree(self, degree):
        result =  self.client.call('turnByDegree', degree)
        time.sleep(0.1)
        return result

    def isHit(self):
        result =  self.client.call('isHit')
        return result

    def reset(self):
        result =  self.client.call('reset')
        time.sleep(0.1)
        return result

    # camera control
    # simGetImage returns compressed png in array of bytes
    # image_type uses one of the AirSimImageType members
    def simGetImages(self, requests):
        responses_raw = self.client.call('simGetImages', requests)
        return [ImageResponse.from_msgpack(response_raw) for response_raw in responses_raw]

    def simSetPose(self, pose, ignore_collison):
        self.client.call('simSetPose', pose, ignore_collison)

    def simGetPose(self):
        return self.client.call('simGetPose')
