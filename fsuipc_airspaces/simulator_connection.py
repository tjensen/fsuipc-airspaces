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
    def __init__(self):
        self.fsuipc = fsuipc.FSUIPC()

    def close(self):
        self.fsuipc.close()

    def read(self):
        prepared_data = self.fsuipc.prepare_data(
            [
                (_TRANSPONDER_ADDR, "H"),
                (_LATITUDE_ADDR, "l"),
                (_LONGITUDE_ADDR, "l"),
                (_ALTITUDE_ADDR, "l")
            ], True)

        data = prepared_data.read()

        return {
            "transponder": _transponder(data[0]),
            "latitude": _latitude(data[1]),
            "longitude": _longitude(data[2]),
            "altitude": _altitude(data[3])
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
