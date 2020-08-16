from typing import List, Tuple, Union, cast

from fsuipc_airspaces import offsets
from fsuipc_airspaces import position


class FSPosition():
    def data_specification(self) -> List[Tuple[int, Union[str, int]]]:
        return [
            (offsets.TRANSPONDER, "H"),
            (offsets.FS_LATITUDE, "l"),
            (offsets.FS_LONGITUDE, "l"),
            (offsets.FS_ALTITUDE, "l")
        ]

    def process_data(self, data: List[Union[int, float, bytes]]) -> position.Position:
        return position.Position(
            transponder=self._transponder(cast(int, data[0])),
            latitude=self._latitude(cast(int, data[1])),
            longitude=self._longitude(cast(int, data[2])),
            altitude=self._altitude(cast(int, data[3]))
        )

    def _transponder(self, raw: int) -> int:
        return int(f"{raw:x}")

    def _latitude(self, raw: int) -> float:
        return float(raw) * 90 / (10001750 * 65536 * 65536)

    def _longitude(self, raw: int) -> float:
        return float(raw) * 360 / (65536 * 65536 * 65536 * 65536)

    def _altitude(self, raw: int) -> float:
        return float(raw) * 3.28084 / (65536 * 65536)
