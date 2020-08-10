import socket
import unittest
from unittest import mock

from fsuipc_airspaces.xplane_dataout import XPlaneDataOut


class TestXPlaneDataOut(unittest.TestCase):
    @mock.patch("socket.socket")
    def test_sends_data_to_airspaces_server(self, mock_socket_class):
        mock_socket = mock_socket_class.return_value

        dataout = XPlaneDataOut("some.host.name", 12345)

        mock_socket_class.assert_called_once_with(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        dataout.write({
            "transponder": 4321,
            "latitude": 48.50632683,
            "longitude": -123.0111380,
            "altitude": 1356.4268649
        })

        mock_socket.sendto.assert_called_once_with(mock.ANY, ("some.host.name", 12345))
        self.assertEqual(
            bytes([
                68, 65, 84, 65, 60, 20, 0, 0, 0,
                123, 6, 66, 66,
                180, 5, 246, 194,
                169, 141, 169, 68,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                104, 0, 0, 0, 0, 0, 0, 0,
                0, 8, 135, 69,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]),
            mock_socket.sendto.call_args[0][0])
