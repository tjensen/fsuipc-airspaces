import unittest
from unittest import mock

import pyuipc

from fsuipc_airspaces.fsuipc import FSUIPC


class TestFSUIPC(unittest.TestCase):
    def setUp(self):
        self.mock_pyuipc_open = mock.Mock(name="pyuipc.open")
        self.mock_pyuipc_close = mock.Mock(name="pyuipc.close")
        self.mock_pyuipc_prepare_data = mock.Mock(name="pyuipc.prepare_data")
        self.mock_pyuipc_read = mock.Mock(name="pyuipc.read")

        pyuipc_patcher = mock.patch.multiple(
            pyuipc, open=self.mock_pyuipc_open, close=self.mock_pyuipc_close,
            prepare_data=self.mock_pyuipc_prepare_data, read=self.mock_pyuipc_read)
        pyuipc_patcher.start()
        self.addCleanup(pyuipc_patcher.stop)

    def test_constructor_calls_open(self):
        FSUIPC()

        self.mock_pyuipc_open.assert_called_once_with(pyuipc.SIM_ANY)

    def test_close_calls_close(self):
        FSUIPC().close()

        self.mock_pyuipc_close.assert_called_once_with()

    def test_can_be_used_as_a_context_manager(self):
        with FSUIPC() as fsuipc:
            self.mock_pyuipc_open.assert_called_once_with(pyuipc.SIM_ANY)

        self.mock_pyuipc_close.assert_called_once_with()

    def test_read_returns_transponder_code_and_latitude_and_longitude_and_altitude(self):
        self.mock_pyuipc_read.return_value = [
            0x1234, 0x5240c70c992ba0, -0x57797e88d4031c00, 0x19d705b6f59]

        with FSUIPC() as fsuipc:
            data = fsuipc.read()

        self.mock_pyuipc_prepare_data.assert_called_once_with(
            [(0x354, "H"), (0x560, "l"), (0x568, "l"), (0x570, "l")], True)

        self.mock_pyuipc_read.assert_called_once_with(self.mock_pyuipc_prepare_data.return_value)

        self.assertEqual(4, len(data))
        self.assertEqual(1234, data["transponder"])
        self.assertAlmostEqual(48.50632683, data["latitude"])
        self.assertAlmostEqual(-123.0111380, data["longitude"])
        self.assertAlmostEqual(1356.4268649, data["altitude"])
