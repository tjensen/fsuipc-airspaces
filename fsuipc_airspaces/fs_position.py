from fsuipc_airspaces import offsets
from fsuipc_airspaces import position


class FSPosition():
    def data_specification(self):
        return [
            (offsets.TRANSPONDER, "H"),
            (offsets.FS_LATITUDE, "l"),
            (offsets.FS_LONGITUDE, "l"),
            (offsets.FS_ALTITUDE, "l")
        ]

    def process_data(self, data):
        return position.Position(
            transponder=self._transponder(data[0]),
            latitude=self._latitude(data[1]),
            longitude=self._longitude(data[2]),
            altitude=self._altitude(data[3])
        )

    def _transponder(self, raw):
        return int(f"{raw:x}")

    def _latitude(self, raw):
        return float(raw) * 90 / (10001750 * 65536 * 65536)

    def _longitude(self, raw):
        return float(raw) * 360 / (65536 * 65536 * 65536 * 65536)

    def _altitude(self, raw):
        return float(raw) * 3.28084 / (65536 * 65536)
