import unittest
import pandas as pd
from modules import ExtractorProvider1


class TestExtractorProv1(unittest.TestCase):
    """
    This class checks the behavior of the method `extract` of class
    `ExtractorProvider1`.
    """
    ext_csv: ExtractorProvider1

    # def setUp(self):
    @classmethod
    def setUpClass(cls):
        cls.ext_csv = ExtractorProvider1()

    # methods
    def test_extractor1_correct_csv(self):
        """
        This method checks if the method `extract` of class `ExtractProvider1`
        works correctly when correct data is given.
        """
        # get data
        correct_df = pd.DataFrame(
            columns=["movie_title", "release_year", "critic_score_percentage",
                     "top_critic_score", "total_critic_reviews_counted"],
            data=[["Inception", 2010, 87, 8.1, 450],
                  ["The Dark Knight", 2008, 94, 8.6, 350],
                  ["Parasite", 2019, 99, 9.5, 475]]
        )
        # check function extract of the class ExtractorProvider1
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(
                correct_df.to_csv(index=False).encode("utf-8"))
        # test correct logs
        pd.testing.assert_frame_equal(correct_df, returned_df)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 extractor] The data has been turned into a dataframe "\
            "object and contains the correct columns.")

    def test_extractor1_non_correct_columns_all(self):
        """
        This method checks if the method `extract` of class `ExtractProvider1`
        fails when all the columns are not correct by logging an error message
        and returning a None object.
        """
        # get data
        non_correct_df = pd.DataFrame(
            columns=["feat1", "feat2"],
            data=[["Inception", 2010], ["The Dark Knight", 2008],
                  ["Parasite", 2019]])
        # check function extract of the class ExtractorProvider1
        bytes_data = non_correct_df.to_csv(index=False).encode("utf-8")
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(bytes_data)
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 extractor] The data does not contain the proper columns.")
    
    def test_extractor1_non_correct_one_column(self):
        """
        This method checks if the method `extract` of class `ExtractProvider1`
        fails when one of the column is incorrect, by logging an error message
        and returning a None object.
        """
        # get data
        non_correct_df = pd.DataFrame(
            columns=["movie_title", "year", "critic_score_percentage",
                     "top_critic_score", "total_critic_reviews_counted"],
            data=[["Inception", 2010, 87, 8.1, 450],
                  ["The Dark Knight", 2008, 94, 8.6, 350],
                  ["Parasite", 2019, 99, 9.5, 475]]
        )
        # check function extract of the class ExtractorProvider1
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(
                non_correct_df.to_csv(index=False).encode("utf-8"))
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 extractor] The data does not contain the proper columns.")

    def test_extractor1_one_column_missing(self):
        """
        This method checks if the method `extract` of class `ExtractProvider1`
        works properly even if a column is missing.
        """
        # get data
        one_missing_col_df = pd.DataFrame(
            columns=["movie_title", "release_year", "critic_score_percentage",
                     "top_critic_score"],
            data=[["Inception", 2010, 87, 8.1],
                  ["The Dark Knight", 2008, 94, 8.6],
                  ["Parasite", 2019, 99, 9.5]]
        )
        # check function extract of the class ExtractorProvider1
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(
                one_missing_col_df.to_csv(index=False).encode("utf-8"))
        # test correct logs
        pd.testing.assert_frame_equal(returned_df, one_missing_col_df)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 extractor] The data has been turned into a dataframe "\
            "object and contains the correct columns.")
