import argparse
import logging
import sys
import time
from typing import Union

import fsuipc

from fsuipc_airspaces.fs_position import FSPosition
from fsuipc_airspaces.gps_position import GPSPosition
from fsuipc_airspaces.simulator_connection import SimulatorConnection
from fsuipc_airspaces.xplane_dataout import XPlaneDataOut


SPINNER = ["\\", "|", "/", "-"]


def polling_loop(
    hostname: str, port: int, interval: float, position: Union[FSPosition, GPSPosition]
) -> None:
    with SimulatorConnection(position) as sim:
        dataout = XPlaneDataOut(hostname, port)

        while True:
            try:
                spinner = SPINNER.pop(0)
                SPINNER.append(spinner)
                sys.stdout.write(f"  {spinner} Running (Press Ctrl+C to stop)\r")

                try:
                    data = sim.read()
                    dataout.write(data)
                except fsuipc.FSUIPCException:
                    logging.exception("Error reading from simulator")
                except OSError:
                    logging.exception("Error writing to Airspaces server")

                time.sleep(interval)

            except KeyboardInterrupt:
                break


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="Hostname of Airspaces server")
    parser.add_argument(
        "port", type=int, nargs="?", default=49003,
        help="Port on Airspaces server to connect to (default 49003)")
    parser.add_argument(
        "--interval", type=float, default=1,
        help="Number of seconds to wait between polling for updates (default 1.0)")
    parser.add_argument(
        "--gps", action="store_true", help="Poll aircraft coordinates from GPS data")
    args = parser.parse_args()

    position: Union[FSPosition, GPSPosition]
    if args.gps:
        position = GPSPosition()
    else:
        position = FSPosition()

    polling_loop(args.hostname, args.port, args.interval, position)
