import unittest
from mock import Mock
import app.battle
import app.units


class TestSquad(unittest.TestCase):
    def setUp(self):
        self.squad = app.battle.Squad(number_of_units=5)

    def test_get_units(self):
        self.squad.number_of_units = 20
        self.squad.get_units()
        self.assertEqual(self.squad.number_of_units, 10)
        self.squad.number_of_units = 1
        self.squad.get_units()
        self.assertEqual(self.squad.number_of_units, 5)

    def test_is_active_units(self):
        unit = Mock()
        self.squad.units[0] = unit
        self.squad.units[1] = unit
        self.squad.units[2] = unit
        self.squad.units[3] = unit
        self.squad.units[4] = unit
        unit.active = True
        units = [unit, unit, unit, unit, unit]
        self.assertEqual(self.squad.is_active_units(), units)
        unit.active = False
        self.assertEqual(self.squad.is_active_units(), [])

    def test_get_power_units(self):
        self.squad.units[0].do_atack = Mock(return_value=0)
        self.squad.units[1].do_atack = Mock(return_value=0)
        self.squad.units[2].do_atack = Mock(return_value=0)
        self.squad.units[3].do_atack = Mock(return_value=0)
        self.squad.units[4].do_atack = Mock(return_value=0)
        self.squad.is_active_units = Mock(return_value=self.squad.units)
        self.assertEqual(self.squad.get_power(), 0)

    def test_take_damage_units(self):
        self.squad.get_units()
        self.squad.take_damage(mutual_damage=50)
        if isinstance(self.squad.units[0], app.units.Solder):
            self.assertEqual(self.squad.units[0].health, 95.03)
        elif isinstance(self.squad.units[0], app.units.Vehicle):
            self.assertEqual(self.squad.units[0].health, 247.025)
