import unittest
from unittest import mock

from fsuipc_airspaces.simulator_connection import SimulatorConnection


class TestSimulatorConnection(unittest.TestCase):
    def setUp(self):
        fsuipc_patcher = mock.patch("fsuipc.FSUIPC")
        self.mock_fsuipc_class = fsuipc_patcher.start()
        self.addCleanup(fsuipc_patcher.stop)

        self.mock_fsuipc = self.mock_fsuipc_class.return_value

    def test_constructor_calls_open_and_prepares_data(self):
        SimulatorConnection()

        self.mock_fsuipc_class.assert_called_once_with()

        self.mock_fsuipc.prepare_data.assert_called_once_with(
            [(0x354, "H"), (0x560, "l"), (0x568, "l"), (0x570, "l")], True)

    def test_close_calls_close(self):
        SimulatorConnection().close()

        self.mock_fsuipc.close.assert_called_once_with()

    def test_can_be_used_as_a_context_manager(self):
        with SimulatorConnection():
            self.mock_fsuipc_class.assert_called_once_with()

        self.mock_fsuipc.close.assert_called_once_with()

    def test_read_returns_transponder_code_and_latitude_and_longitude_and_altitude(self):
        mock_prepared_data = self.mock_fsuipc.prepare_data.return_value

        mock_prepared_data.read.return_value = [
            0x1234, 0x5240c70c992ba0, -0x57797e88d4031c00, 0x19d705b6f59]

        with SimulatorConnection() as sim:
            data = sim.read()

        mock_prepared_data.read.assert_called_once_with()

        self.assertEqual(4, len(data))
        self.assertEqual(1234, data["transponder"])
        self.assertAlmostEqual(48.50632683, data["latitude"])
        self.assertAlmostEqual(-123.0111380, data["longitude"])
        self.assertAlmostEqual(1356.4268649, data["altitude"])
