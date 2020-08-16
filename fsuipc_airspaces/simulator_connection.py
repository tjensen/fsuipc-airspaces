from types import TracebackType
from typing import Optional, Type, Union

import fsuipc

from fsuipc_airspaces.fs_position import FSPosition
from fsuipc_airspaces.gps_position import GPSPosition
from fsuipc_airspaces.position import Position


class SimulatorConnection():
    def __init__(self, position: Union[FSPosition, GPSPosition]) -> None:
        self._fsuipc = fsuipc.FSUIPC()
        self._position = position

        self._prepared_data = self._fsuipc.prepare_data(self._position.data_specification(), True)

    def close(self) -> None:
        self._fsuipc.close()

    def read(self) -> Position:
        return self._position.process_data(self._prepared_data.read())

    def __enter__(self) -> "SimulatorConnection":
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        self.close()
