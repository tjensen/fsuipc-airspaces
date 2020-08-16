from fsuipc_airspaces import offsets
from fsuipc_airspaces import position


class GPSPosition():
    def data_specification(self):
        return [
            (offsets.TRANSPONDER, "H"),
            (offsets.GPS_LATITUDE, "f"),
            (offsets.GPS_LONGITUDE, "f"),
            (offsets.GPS_ALTITUDE, "f")
        ]

    def process_data(self, data):
        return position.Position(
            transponder=self._transponder(data[0]),
            latitude=data[1],
            longitude=data[2],
            altitude=data[3]
        )

    def _transponder(self, raw):
        return int(f"{raw:x}")
