from secure_all.data.attribute_dni import Dni
from secure_all.access_manager import AccessManager
import unittest


class TestAccessManager(unittest.TestCase):
    def test_singleton_access_manager(self):
        access_manager_1 = AccessManager()
        access_manager_2 = AccessManager()
        access_manager_3 = AccessManager()
        access_manager_4 = AccessManager()

        self.assertEqual(access_manager_1, access_manager_2)
        self.assertEqual(access_manager_2, access_manager_3)
        self.assertEqual(access_manager_3, access_manager_4)

        dni_1 = Dni("12345678Z")
        dni_2 = Dni("12345678Z")

        self.assertNotEqual(dni_1, dni_2)


if __name__ == '__main__':
    unittest.main()
