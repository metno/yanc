import unittest
import yanc
import time


class OperationalTest(unittest.TestCase):
    def assertValid(self, cmd):
        """
      Wrapper function for testing if a command-line input succeeds. The test fails if the command
      throws an error.
      """
        with self.assertRaises(SystemExit) as cm:
            yanc.run(cmd.split(" "))
        if cm.exception.code != 0:
            print("This command failed: '{}'".format(cmd))
        self.assertTrue(cm.exception.code == 0)

    def get_current_file(self, tag):
        """
      Retrieves an operational file (the one valid at 00 for yesterday)
      """
        date = time.strftime("%Y%m%d", time.gmtime(time.time() - 24 * 3600))
        hour = "00"
        basedir = "/lustre/storeB/project/metproduction/products/meps"
        filename = "{}/{}_{}T{}Z.nc".format(basedir, tag, date, hour)
        return filename

    def test_meps_det_pp(self):
        filename = self.get_current_file("member_0/meps_mbr0_pp_2_5km")
        self.assertValid(
            "--template templates/meps_det_pp_2_5km.yml --ncfile {}".format(filename)
        )

    def test_meps_det_extracted(self):
        filename = self.get_current_file("member_0/meps_mbr0_extracted_2_5km")
        self.assertValid(
            "--template templates/meps_det_extracted_2_5km.yml --ncfile {}".format(
                filename
            )
        )

    def test_meps_allmembers_extracted(self):
        filename = self.get_current_file("meps_full_2_5km")
        self.assertValid(
            "--template templates/meps_allmembers_extracted_2_5km.yml --ncfile {}".format(
                filename
            )
        )


if __name__ == "__main__":
    unittest.main()
