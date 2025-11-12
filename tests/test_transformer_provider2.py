import unittest
import pandas as pd
from modules import TransformProvider2


class TestTransformProv2(unittest.TestCase):
    """
    This class checks the behavior of the method `transform` of class
    `TransformProvider2`.
    """
    tran_csv: TransformProvider2

    # def setUp(self):
    @classmethod
    def setUpClass(cls):
        cls.tran_csv = TransformProvider2()

    # methods
    def test_transform_correct_dataframe(self):
        """
        This method checks if the method `transform` of class `TransformProvider2`
        works correctly when correct data is given.
        """
        # get data
        data = pd.DataFrame(
            columns=[
                "title", "year", "audience_average_score",
                "total_audience_ratings", "domestic_box_office_gross"],
            data=[["Inception", 2010, 9.1, 1500000, 292576195],
                  ["The Dark Knight", 2008, 9.4, 2200000, 533345358],
                  ["Parasite", 2019, 9.0, 800000, 53369749]]
        )
        final_df = data.rename(
            columns={"title": "movie_title", "year": "release_year"})
        final_df = final_df.astype({
            "movie_title": "string", "release_year": "uint16",
            "audience_average_score": "float32", "total_audience_ratings": "int32",
            "domestic_box_office_gross": "int64"})
        final_df.set_index(["movie_title", "release_year"], inplace=True)
        # check function extract of the class TransformProvider2
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(data)
        # test correct logs
        pd.testing.assert_frame_equal(final_df, returned_df)
        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider2 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider2 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")

    def test_transform_one_column_missing(self):
        """
        This method checks if the method `transform` of class `TransformProvider2`
        works properly even if a column is missing.
        """
        # get data
        one_missing_col_df = pd.DataFrame(
            columns=[
                "title", "year", "total_audience_ratings",
                "domestic_box_office_gross"],
            data=[["Inception", 2010, 1500000, 292576195],
                  ["The Dark Knight", 2008, 2200000, 533345358],
                  ["Parasite", 2019, 800000, 53369749]]
        )
        final_df_miss_col = one_missing_col_df.rename(
            columns={"title": "movie_title", "year": "release_year"})
        final_df_miss_col = final_df_miss_col.astype({
            "movie_title": "string", "release_year": "uint16",
            "total_audience_ratings": "int32",
            "domestic_box_office_gross": "int64"})
        final_df_miss_col.set_index(["movie_title", "release_year"], inplace=True)
        # check function extract of the class TransformProvider2
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_missing_col_df)
        # test correct logs
        pd.testing.assert_frame_equal(final_df_miss_col, returned_df)
        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider2 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider2 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")
    
    def test_transform_no_index(self):
        """
        This method checks if the method `transform` of class `TransformProvider2`
        fails when one of the fields for the index are missing.
        """
        # get data
        one_missing_col_df = pd.DataFrame(
            columns=[
                "year", "audience_average_score",
                "total_audience_ratings", "domestic_box_office_gross"],
            data=[[2010, 9.1, 1500000, 292576195],
                  [2008, 9.4, 2200000, 533345358],
                  [2019, 9.0, 800000, 53369749]]
        )
        # check function extract of the class TransformProvider2
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_missing_col_df)
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 3)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider2 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider2 transformer] The data does not contain any of the "\
            "columns `movie_title` or `release_year`, so it was not possible "\
            "to set them as index.")
