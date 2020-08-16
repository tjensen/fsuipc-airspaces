import fsuipc


_TRANSPONDER_ADDR = 0x354
_LATITUDE_ADDR = 0x560
_LONGITUDE_ADDR = 0x568
_ALTITUDE_ADDR = 0x570


def _transponder(raw):
    return int(f"{raw:x}")


def _latitude(raw):
    return float(raw) * 90 / (10001750 * 65536 * 65536)


def _longitude(raw):
    return float(raw) * 360 / (65536 * 65536 * 65536 * 65536)


def _altitude(raw):
    return float(raw) * 3.28084 / (65536 * 65536)


class SimulatorConnection():
    def __init__(self, position):
        self._fsuipc = fsuipc.FSUIPC()
        self._position = position

        self._prepared_data = self._fsuipc.prepare_data(self._position.data_specification(), True)

    def close(self):
        self._fsuipc.close()

    def read(self):
        return self._position.process_data(self._prepared_data.read())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
