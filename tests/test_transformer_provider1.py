import unittest
import pandas as pd
from modules.transforms import TransformProvider1


class TestTransformProv1(unittest.TestCase):
    """
    This class checks the behavior of the method `transform` of class
    `TransformProvider1`.
    """
    tran_csv: TransformProvider1

    # def setUp(self):
    @classmethod
    def setUpClass(cls):
        cls.tran_csv = TransformProvider1()

    # methods
    def test_transform_correct_dataframe(self):
        """
        This method checks if the method `transform` of class `TransformProvider1`
        works correctly when correct data is given.
        """
        # get data
        data = pd.DataFrame(
            columns=["movie_title", "release_year", "critic_score_percentage",
                     "top_critic_score", "total_critic_reviews_counted"],
            data=[["Inception", 2010, 87, 8.1, 450],
                  ["The Dark Knight", 2008, 94, 8.6, 350],
                  ["Parasite", 2019, 99, 9.5, 475]]
        )
        final_df = data.astype({
            "movie_title": "string", "release_year": "uint16",
            "critic_score_percentage": "uint8", "top_critic_score": "float32",
            "total_critic_reviews_counted": "int32"})
        final_df.set_index(["movie_title", "release_year"], inplace=True)
        # check function extract of the class TransformProvider1
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(data)
        # test correct logs
        pd.testing.assert_frame_equal(final_df, returned_df)
        self.assertEqual(len(captured.records), 2)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider1 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")

    def test_transform_one_column_missing(self):
        """
        This method checks if the method `transform` of class `TransformProvider1`
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
        final_df_one_miss = one_missing_col_df.astype({
            "movie_title": "string", "release_year": "uint16",
            "critic_score_percentage": "uint8", "top_critic_score": "float32"})
        final_df_one_miss.set_index(
            ["movie_title", "release_year"], inplace=True)
        # check function extract of the class TransformProvider1
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_missing_col_df)
        # test correct logs
        pd.testing.assert_frame_equal(final_df_one_miss, returned_df)
        self.assertEqual(len(captured.records), 2)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider1 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")
    
    def test_transform_no_index(self):
        """
        This method checks if the method `transform` of class `TransformProvider1`
        fails when one of the fields for the index are missing.
        """
        # get data
        one_missing_col_df = pd.DataFrame(
            columns=["release_year", "critic_score_percentage",
                     "top_critic_score"],
            data=[[2010, 87, 8.1],
                  [2008, 94, 8.6],
                  [2019, 99, 9.5]]
        )
        # check function extract of the class TransformProvider1
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_missing_col_df)
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 2)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider1 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider1 transformer] The data does not contain any of the "\
            "columns `movie_title` or `release_year`, so it was not possible "\
            "to set them as index.")
