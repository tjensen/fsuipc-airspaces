import unittest

from fsuipc_airspaces.gps_position import GPSPosition


class TestGPSPosition(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.position = GPSPosition()

    def test_data_specification_returns_data_specification_for_reading_position_in_fs_units(self):
        specification = self.position.data_specification()

        self.assertEqual(
            [
                (0x354, "H"),
                (0x6010, "f"),
                (0x6018, "f"),
                (0x6020, "f")
            ],
            specification)

    def test_process_data_returns_position_for_given_data(self):
        position = self.position.process_data([0x1234, 48.50632683, -123.0111380, 1356.4268649])

        self.assertEqual(1234, position.transponder)
        self.assertAlmostEqual(48.50632683, position.latitude)
        self.assertAlmostEqual(-123.0111380, position.longitude)
        self.assertAlmostEqual(1356.4268649, position.altitude)
