import sys
import unittest
from unittest import mock

import fsuipc

from fsuipc_airspaces import fsuipc_airspaces
from fsuipc_airspaces.fs_position import FSPosition
from fsuipc_airspaces.gps_position import GPSPosition


@mock.patch("fsuipc_airspaces.fsuipc_airspaces.polling_loop", autospec=True)
class TestMain(unittest.TestCase):
    def test_main_parses_command_line_and_starts_polling_loop(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "HOSTNAME", "54321"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 54321, 1, mock.ANY)

        self.assertEqual(
            FSPosition().data_specification(),
            mock_polling_loop.call_args[0][3].data_specification())

    def test_main_defaults_port_to_49003_when_not_specified(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "HOSTNAME"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 49003, 1, mock.ANY)

        self.assertEqual(
            FSPosition().data_specification(),
            mock_polling_loop.call_args[0][3].data_specification())

    def test_main_sets_polling_interval_when_specified(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "--interval", "0.25", "HOSTNAME"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 49003, 0.25, mock.ANY)

        self.assertEqual(
            FSPosition().data_specification(),
            mock_polling_loop.call_args[0][3].data_specification())

    def test_main_uses_gps_position_when_specified(self, mock_polling_loop):
        with mock.patch.object(sys, "argv", ["ARGV0-UNUSED", "--gps", "HOSTNAME"]):
            fsuipc_airspaces.main()

        mock_polling_loop.assert_called_once_with("HOSTNAME", 49003, 1, mock.ANY)

        self.assertEqual(
            GPSPosition().data_specification(),
            mock_polling_loop.call_args[0][3].data_specification())


class TestPollingLoop(unittest.TestCase):
    def setUp(self):
        super().setUp()

        simulator_patcher = mock.patch(
            "fsuipc_airspaces.fsuipc_airspaces.SimulatorConnection", autospec=True)
        self.mock_simulator_class = simulator_patcher.start()
        self.addCleanup(simulator_patcher.stop)

        dataout_patcher = mock.patch(
            "fsuipc_airspaces.fsuipc_airspaces.XPlaneDataOut", autospec=True)
        self.mock_xplane_dataout_class = dataout_patcher.start()
        self.addCleanup(dataout_patcher.stop)

        sleep_patcher = mock.patch("time.sleep")
        self.mock_sleep = sleep_patcher.start()
        self.addCleanup(sleep_patcher.stop)

        self.mock_simulator = self.mock_simulator_class.return_value.__enter__.return_value
        self.mock_xplane_dataout = self.mock_xplane_dataout_class.return_value

    def test_loops_until_ctrl_c_is_pressed(self):
        self.mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5, mock.sentinel.position)

        self.mock_simulator_class.assert_called_once_with(mock.sentinel.position)

        self.mock_xplane_dataout_class.assert_called_once_with("HOSTNAME", 12345)

        self.assertEqual(4, self.mock_simulator.read.call_count)
        self.mock_simulator.read.assert_called_with()

        self.assertEqual(4, self.mock_xplane_dataout.write.call_count)
        self.mock_xplane_dataout.write.assert_called_with(self.mock_simulator.read.return_value)

        self.assertEqual(4, self.mock_sleep.call_count)

    def test_continues_polling_when_write_raises_an_os_error(self):
        self.mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        self.mock_xplane_dataout.write.side_effect = OSError

        fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5, mock.sentinel.position)

        self.assertEqual(4, self.mock_simulator.read.call_count)
        self.assertEqual(4, self.mock_xplane_dataout.write.call_count)
        self.assertEqual(4, self.mock_sleep.call_count)

    def test_stops_polling_when_write_raises_an_exception_that_is_not_an_os_error(self):
        self.mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        self.mock_xplane_dataout.write.side_effect = RuntimeError

        with self.assertRaises(RuntimeError):
            fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5, mock.sentinel.position)

        self.assertEqual(1, self.mock_simulator.read.call_count)
        self.assertEqual(1, self.mock_xplane_dataout.write.call_count)
        self.assertEqual(0, self.mock_sleep.call_count)

    def test_continues_polling_when_read_raises_an_fsuipc_exception(self):
        self.mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        self.mock_simulator.read.side_effect = fsuipc.FSUIPCException(fsuipc.ERR_TIMEOUT)

        fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5, mock.sentinel.position)

        self.assertEqual(4, self.mock_simulator.read.call_count)
        self.assertEqual(0, self.mock_xplane_dataout.write.call_count)
        self.assertEqual(4, self.mock_sleep.call_count)

    def test_stops_polling_when_read_raises_an_exception_that_is_not_an_fsuipc_exception(self):
        self.mock_sleep.side_effect = [None, None, None, KeyboardInterrupt]

        self.mock_simulator.read.side_effect = RuntimeError

        with self.assertRaises(RuntimeError):
            fsuipc_airspaces.polling_loop("HOSTNAME", 12345, 7.5, mock.sentinel.position)

        self.assertEqual(1, self.mock_simulator.read.call_count)
        self.assertEqual(0, self.mock_xplane_dataout.write.call_count)
        self.assertEqual(0, self.mock_sleep.call_count)
