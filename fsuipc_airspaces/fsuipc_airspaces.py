import argparse
import sys
import time

from fsuipc_airspaces.fsuipc import FSUIPC
from fsuipc_airspaces.xplane_dataout import XPlaneDataOut


SPINNER = ["\\", "|", "/", "-"]


def polling_loop(hostname, port, interval):
    with FSUIPC() as fsuipc:
        dataout = XPlaneDataOut(hostname, port)

        while True:
            try:
                spinner = SPINNER.pop(0)
                SPINNER.append(spinner)
                sys.stdout.write(f"\r{spinner} Running (Press Ctrl+C to stop)")

                data = fsuipc.read()

                dataout.write(data)

                time.sleep(interval)

            except KeyboardInterrupt:
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="Hostname of Airspaces server")
    parser.add_argument(
        "port", type=int, nargs="?", default=49003,
        help="Port on Airspaces server to connect to (default 49003)")
    parser.add_argument(
        "--interval", type=float, default=1,
        help="Number of seconds to wait between polling for updates (default 1.0)")
    args = parser.parse_args()

    polling_loop(args.hostname, args.port, args.interval)
