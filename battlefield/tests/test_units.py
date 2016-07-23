import unittest
from mock import Mock, patch
import app.units


class TestSolder(unittest.TestCase):
    def setUp(self):
        self.solder = app.units.Solder()

    def test_get_armor(self):
        self.solder.experience = 2
        self.assertEqual(self.solder.get_armour(), 0.035)

    @patch('app.units.random')
    def test_do_attack(self, mock_random):
        mock_random.randrange = Mock(return_value=5)

        self.solder.health = 100
        self.assertEqual(self.solder.do_attack(), 1.5)
        self.solder.recharged = False
        self.assertEqual(self.solder.do_attack(), 0)

    def test_take_damage(self):
        self.solder.experience = 2
        self.solder.health = 100
        damage = 20
        self.solder.take_damage(damage)
        self.assertEqual(self.solder.health, 80.035)
        damage = 0
        self.solder.armour = 5
        self.assertEqual(self.solder.take_damage(damage), None)
        self.solder.health = 0
        self.solder.armour = 0
        self.solder.take_damage(damage=1)
        self.assertEqual(self.solder.active, False)


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.vehicle = app.units.Vehicle()

    def test_do_attack(self):
        self.vehicle.get_operators_damage = Mock(return_value=20)

        self.vehicle.health = 150
        self.assertEqual(self.vehicle.do_attack(), 1000)
        self.vehicle.recharged = False
        self.assertEqual(self.vehicle.do_attack(), 0)

    def test_take_damage(self):
        damage = 60
        self.vehicle.health = 150
        self.vehicle.armour = 30
        self.vehicle.take_damage(damage)
        self.assertEqual(self.vehicle.health, 144)
        damage = 0
        self.vehicle.armour = 1
        self.assertEqual(self.vehicle.take_damage(damage), None)
        self.vehicle.health = 0
        self.vehicle.take_damage(damage=10)
        self.assertEqual(self.vehicle.active, False)

    def test_get_armour(self):
        self.vehicle.calc_experience = Mock(return_value=5)
        self.assertEqual(self.vehicle.get_armour(), 0.05)

    def test_get_health(self):
        operator = Mock()
        operator.health = 100
        self.vehicle.operators = [operator, operator, operator]
        self.assertEqual(self.vehicle.get_health(), 333.3333333333333)

    def test_calc_experience(self):
        operator = Mock()
        operator.experience = 5
        self.vehicle.operators = [operator, operator, operator]
        self.assertEqual(self.vehicle.calc_experience(), 15)

    def test_get_operators_damage(self):
        self.vehicle.operators[0].do_attack = Mock(return_value=5)
        self.vehicle.operators[1].do_attack = Mock(return_value=5)
        self.assertEqual(self.vehicle.get_operators_damage(), 5)
        self.vehicle.operators[0].do_attack = Mock(return_value=0)
        self.vehicle.operators[1].do_attack = Mock(return_value=0)
        self.assertEqual(self.vehicle.get_operators_damage(), 0)
