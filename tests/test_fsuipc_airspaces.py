import sys
import unittest
from unittest import mock

from fsuipc_airspaces import fsuipc_airspaces


@mock.patch("fsuipc_airspaces.fsuipc_airspaces.polling_loop")
class TestMain(unittest.TestCase):
    def test_main_parses_command_line_and_starts_polling_loop(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "HOSTNAME", "54321"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 54321, 1)

    def test_main_defaults_port_to_49003_when_not_specified(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "HOSTNAME"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 49003, 1)

    def test_main_sets_polling_interval_when_specified(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "--interval", "0.25", "HOSTNAME"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 49003, 0.25)


@mock.patch("fsuipc_airspaces.fsuipc_airspaces.SimulatorConnection")
@mock.patch("fsuipc_airspaces.fsuipc_airspaces.XPlaneDataOut")
@mock.patch("time.sleep")
class TestPollingLoop(unittest.TestCase):
    def test_loops_until_ctrl_c_is_pressed(
            self, mock_sleep, mock_xplane_dataout_class, mock_simulator_class):
        mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        mock_simulator = mock_simulator_class.return_value.__enter__.return_value

        mock_xplane_dataout = mock_xplane_dataout_class.return_value

        fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5)

        mock_simulator_class.assert_called_once_with()

        mock_xplane_dataout_class.assert_called_once_with("HOSTNAME", 12345)

        self.assertEqual(4, mock_simulator.read.call_count)
        mock_simulator.read.assert_called_with()

        self.assertEqual(4, mock_xplane_dataout.write.call_count)
        mock_xplane_dataout.write.assert_called_with(mock_simulator.read.return_value)

        self.assertEqual(4, mock_sleep.call_count)
