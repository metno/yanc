import unittest
import yanc
import glob


class CommandLineTest(unittest.TestCase):
   def assertError(self, cmd):
      """
      Wrapper function for testing if a command-line input fails. The test fails if the command does
      not throw an error.

      Check also that adding --debug works.
      """
      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' '))
      if cm.exception.code == 0:
         print("This command did not fail: '{}'".format(cmd))
      self.assertTrue(cm.exception.code != 0)

      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' ') + ['--debug'])
      if cm.exception.code == 0:
         print("This command did not fail: '{}'".format(cmd + ' --debug'))
      self.assertTrue(cm.exception.code != 0)

   def assertValid(self, cmd):
      """
      Wrapper function for testing if a command-line input succeeds. The test fails if the command
      throws an error.
      """
      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' '))
      if cm.exception.code != 0:
         print("This command failed: '{}'".format(cmd))
      self.assertTrue(cm.exception.code == 0)

      with self.assertRaises(SystemExit) as cm:
         yanc.run(cmd.split(' ') + ["--debug"])
      if cm.exception.code != 0:
         print("This command failed: '{}'".format(cmd + ' --debug'))
      self.assertTrue(cm.exception.code == 0)

   def test_no_ncfile(self):
      """
      No NetCDF provided on the command-line
      """
      self.assertError('--template tests/template.yml')

   def test_no_template(self):
      """
      No templte file provided on the command-line
      """
      self.assertError('--ncfile tests/sample.nc')

   def test_missing_ncfile(self):
      """
      NetCDF file does not exist
      """
      self.assertError('--template tests/template.yml --ncfile tests/sample_missing.nc')

   def test_missing_template(self):
      """
      Template file does not exist
      """
      self.assertError('--template tests/template_missing.yml --ncfile tests/sample.nc')

   def test_invalid_auto(self):
      """
      Checks that the sample file fails to conform to all templates in the tests/invalid folder
      """
      templates = glob.glob("tests/invalid/*.yml")
      for template in templates:
         self.assertError('--template {} --ncfile tests/sample.nc'.format(template))

   def test_valid_auto(self):
      """
      Checks that the sample file conforms to all templates in the tests/valid folder
      """
      templates = glob.glob("tests/valid/*.yml")
      for template in templates:
         self.assertValid('--template {} --ncfile tests/sample.nc'.format(template))

   def test_valid(self):
      self.assertValid('--template tests/template.yml --ncfile tests/sample.nc')


if __name__ == '__main__':
   unittest.main()
