import os
import unittest
import pandas as pd
from modules.fileio import FileIO


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
            f"[File IO] The file in '{path}' has been read.")
    
    def test_read_existing_file_list(self):
        """
        This methods checks if the function `read_file` returns a list of byte
        objects when a list of paths are given as parameter and the files
        related with those paths exist.
        """
        bytes_content = b"hello world!"
        path = [
            "tests/data/fileio_read_test_method.csv",
            "tests/data/fileio_read_test_method.csv",
            "tests/data/fileio_read_test_method.csv"
        ]
        with self.assertLogs() as captured:
            read_content = FileIO().read_file(path)
        self.assertEqual(len(read_content), 3)
        self.assertEqual(bytes_content, read_content[0])
        self.assertEqual(bytes_content, read_content[1])
        self.assertEqual(bytes_content, read_content[2])

        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"[File IO] The file in '{path[0]}' has been read.")
        self.assertEqual(
            captured.records[1].getMessage(),
            f"[File IO] The file in '{path[1]}' has been read.")
        self.assertEqual(
            captured.records[2].getMessage(),
            f"[File IO] The file in '{path[2]}' has been read.")

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
            "[File IO] The file in './non_existing_file.csv' does not exist.")
        assert read_content is None

    def test_read_one_non_existing_file_from_list(self):
        """
        This method checks if the function `read_file` works properly even if
        one of files does not exists. The method should return the list with
        the raw data, except for the wrong path that should be a None object.
        """
        # read the non-existing file
        path = [
            "tests/data/fileio_read_test_method.csv",
            "./non_existing_file.csv",
            "tests/data/fileio_read_test_method.csv"
        ]
        bytes_content = b"hello world!"
        with self.assertLogs() as captured:
            read_content = FileIO().read_file(path)
        # check if the result and logs messages
        self.assertEqual(len(read_content), 3)
        self.assertEqual(bytes_content, read_content[0])
        self.assertEqual(None, read_content[1])
        self.assertEqual(bytes_content, read_content[2])

        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"[File IO] The file in '{path[0]}' has been read.")
        self.assertEqual(
            captured.records[1].getMessage(),
            f"[File IO] The file in '{path[1]}' does not exist.")
        self.assertEqual(
            captured.records[2].getMessage(),
            f"[File IO] The file in '{path[2]}' has been read.")
    
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
            "[File IO] The file in 'tests/data/fileio_non_permissions.csv' can not be accessed.")
        assert read_content is None

    def test_read_one_non_access_allowed_list(self):
        """
        This method checks if the function `read_file` works properly even if
        one of the files has no access permissions. It should return the raw
        data of the files which have access and a None object for the one
        without access.
        """
        paths = [
            "tests/data/fileio_read_test_method.csv",
            "tests/data/fileio_non_permissions.csv",
            "tests/data/fileio_read_test_method.csv"
        ]
        bytes_content = b"hello world!"
        # read files
        with self.assertLogs() as captured:
            read_content = FileIO().read_file(paths)
        # check if the result and logs messages
        self.assertEqual(len(read_content), 3)
        self.assertEqual(bytes_content, read_content[0])
        self.assertEqual(None, read_content[1])
        self.assertEqual(bytes_content, read_content[2])

        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"[File IO] The file in '{paths[0]}' has been read.")
        self.assertEqual(
            captured.records[1].getMessage(),
            f"[File IO] The file in '{paths[1]}' can not be accessed.")
        self.assertEqual(
            captured.records[2].getMessage(),
            f"[File IO] The file in '{paths[2]}' has been read.")
    
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
        saved_object = pd.read_csv(path, index_col=0)
        os.remove(path)
        # test the DataFrame object is equal to the saved object
        pd.testing.assert_frame_equal(to_save_obj, saved_object)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"[File IO] The data has been saved into the CSV file in '{path}'")
    
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
        saved_object = pd.read_csv(path, index_col=0)
        pd.testing.assert_frame_equal(to_save_obj, saved_object)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            f"[File IO] The data has been saved into the CSV file in '{path}'")
    
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
            "[File IO] There are no permissions to write in 'tests/data/dir_non_permissi"\
            "ons/write_test_method_new_file.csv'.")


if __name__ == '__main__':
    unittest.main()
