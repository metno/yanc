import unittest
import yanc

class IntegrationTest(unittest.TestCase):
   def assertError(self, cmd):
      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' '))
      self.assertTrue(cm.exception.code != 0)

   def assertValid(self, cmd):
      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' '))
      self.assertTrue(cm.exception.code == 0)

   def test_missing_ncfile(self):
      self.assertError('--template tests/template.yml')

   def test_missing_template(self):
      self.assertError('--ncfile tests/sample.nc')

   def test_missing_template(self):
      self.assertError('--template tests/template_missing.yml --ncfile tests/sample.nc')

   def test_missing_dim(self):
      self.assertError('--template tests/template_missing_dim.yml --ncfile tests/sample.nc')

   def test_wrong_dim_length(self):
      self.assertError('--template tests/template_wrong_dim_length.yml --ncfile tests/sample.nc')

   def test_valid(self):
      self.assertValid('--template tests/template.yml --ncfile tests/sample.nc')


if __name__ == '__main__':
   unittest.main()
