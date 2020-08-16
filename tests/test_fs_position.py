import unittest

from fsuipc_airspaces.fs_position import FSPosition


class TestFSPosition(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.position = FSPosition()

    def test_data_specification_returns_data_specification_for_reading_position_in_fs_units(
            self) -> None:
        specification = self.position.data_specification()

        self.assertEqual(
            [
                (0x354, "H"),
                (0x560, "l"),
                (0x568, "l"),
                (0x570, "l")
            ],
            specification)

    def test_process_data_returns_position_for_given_data(self) -> None:
        position = self.position.process_data(
            [0x1234, 0x5240c70c992ba0, -0x57797e88d4031c00, 0x19d705b6f59])

        self.assertEqual(1234, position.transponder)
        self.assertAlmostEqual(48.50632683, position.latitude)
        self.assertAlmostEqual(-123.0111380, position.longitude)
        self.assertAlmostEqual(1356.4268649, position.altitude)
