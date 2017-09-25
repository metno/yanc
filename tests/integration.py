import unittest
import yanc

class IntegrationTest(unittest.TestCase):
   def test_t(self):
      raise Exception
      yanc.main(['--template', '../../templates/meps_test.yaml'])
   def test_1(self):
      self.assertEqual(1,2)


if __name__ == '__main__':
   unittest.main()
