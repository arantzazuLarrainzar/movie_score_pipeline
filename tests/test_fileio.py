import os
import unittest
import pandas as pd
from modules import FileIO


class TestFileIO(unittest.TestCase):
    """
    This class tests the methods implemented in FileIO class.
    """
    # methods
    def test_read_existing_file(self):
        """
        This methods checks if the function `read_file` returns a byte object
        from an existing file.
        """
        bytes_content = b"hello world!"
        path = "tests/data/fileio_read_test_method.csv"
        with self.assertLogs() as captured:
            read_content = FileIO().read_file(path)
        assert bytes_content == read_content
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"The file in '{path}' has been read.")

    def test_read_non_existing_file(self):
        """
        This method checks if the function `read_file` returns a None object
        from a file that do not exist.
        """
        # read the non-existing file
        with self.assertLogs() as captured:
            read_content = FileIO().read_file("./non_existing_file.csv")
        # check if the method returns a None object and sends the proper logs
        # messages
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "The file in './non_existing_file.csv' does not exist.")
        assert read_content is None
    
    def test_read_non_access_allowed(self):
        """
        This method checks if the function `read_file` returns a None object
        from a file that can not be accessed, because the user has not
        permissions.
        """
        # read the non-existing file
        with self.assertLogs() as captured:
            read_content = FileIO().read_file("tests/data/fileio_non_permissions.csv")
        # check if the method returns a None object and sends the proper logs
        # messages
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "The file in 'tests/data/fileio_non_permissions.csv' can not be accessed.")
        assert read_content is None
    
    def test_write_new_file(self):
        """
        This method checks if the method `write_csv` in FileIO saves a
        pandas.DataFrame into a file that does not initially exist.
        """
        to_save_obj = pd.DataFrame({"feat1": [0, 1, 2], "feat2": [4, 5, 6]})
        path = "tests/data/non_file.csv"
        # save the DataFrame object
        with self.assertLogs() as captured:
            FileIO().write_csv(path, to_save_obj)
        # read the saved information and remove the created file
        saved_object = pd.read_csv(path)
        os.remove(path)
        # test the DataFrame object is equal to the saved object
        pd.testing.assert_frame_equal(to_save_obj, saved_object)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"The data has been saved into the CSV file in '{path}'")
    
    def test_write_old_file(self):
        """
        This method checks if the method `write_csv` in FileIO saves a
        pandas.DataFrame into a file that exists previously.
        """
        to_save_obj = pd.DataFrame({"feat1": [0, 1, 2], "feat2": [4, 5, 6]})
        path = "tests/data/fileio_write_test_method_old_file.csv"
        # save the DataFrame object
        with self.assertLogs() as captured:
            FileIO().write_csv(path, to_save_obj)
        # read the saved information and test if it is equal to the DataFrame object
        saved_object = pd.read_csv(path)
        pd.testing.assert_frame_equal(to_save_obj, saved_object)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"The data has been saved into the CSV file in '{path}'")
    
    def test_write_no_permissions(self):
        """
        This method checks if the method `write_csv` in FileIO logs a message
        error when it tries to save the dataframe into a directory that has not
        permissions to access.
        """
        to_save_obj = pd.DataFrame({"feat1": [0, 1, 2], "feat2": [4, 5, 6]})
        # save the DataFrame object
        with self.assertLogs() as captured:
            FileIO().write_csv(
                "tests/data/dir_non_permissions/write_test_method_new_file.csv",
                to_save_obj)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "There are no permissions to write in 'tests/data/dir_non_permissi"\
            "ons/write_test_method_new_file.csv'.")


if __name__ == '__main__':
    unittest.main()
