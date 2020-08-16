import socket
import struct


# Copied and adapted from tools/faker.js in github.com/foucdeg/airspaces
_START_BUFFER = bytes([68, 65, 84, 65, 60, 20, 0, 0, 0])
_END_BUFFER = bytes([0] * 20)
_START_TRANSPONDER = bytes([104, 0, 0, 0, 0, 0, 0, 0])
_END_TRANSPONDER = bytes([0] * 24)


def _encode(position):
    return _START_BUFFER \
        + struct.pack("<fff", position.latitude, position.longitude, position.altitude) \
        + _END_BUFFER \
        + _START_TRANSPONDER \
        + struct.pack("<f", position.transponder) \
        + _END_TRANSPONDER


class XPlaneDataOut():
    def __init__(self, host, port):
        self.address = (host, port)

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def write(self, data):
        self.socket.sendto(_encode(data), self.address)
