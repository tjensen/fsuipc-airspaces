from typing import List, Tuple, Union, cast

from fsuipc_airspaces import offsets
from fsuipc_airspaces import position


class GPSPosition():
    def data_specification(self) -> List[Tuple[int, Union[str, int]]]:
        return [
            (offsets.TRANSPONDER, "H"),
            (offsets.GPS_LATITUDE, "f"),
            (offsets.GPS_LONGITUDE, "f"),
            (offsets.GPS_ALTITUDE, "f")
        ]

    def process_data(self, data: List[Union[int, float, bytes]]) -> position.Position:
        return position.Position(
            transponder=self._transponder(cast(int, data[0])),
            latitude=cast(float, data[1]),
            longitude=cast(float, data[2]),
            altitude=cast(float, data[3])
        )

    def _transponder(self, raw: int) -> int:
        return int(f"{raw:x}")
