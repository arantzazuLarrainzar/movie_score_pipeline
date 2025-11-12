import unittest
import pandas as pd
from modules import ExtractorProvider2


class TestExtractorProv2(unittest.TestCase):
    """
    This class checks the behavior of the method `extract` of the class
    `ExtractorProvider2`.
    """
    ext_prov2: ExtractorProvider2

    @classmethod
    def setUpClass(cls):
        cls.ext_prov2 = ExtractorProvider2()

    # methods
    def test_extract_correct_json(self):
        """
        This method checks if the method `extract` of class `ExtractProvider2`
        works correctly when correct data is given.
        """
        # get data
        correct_df = pd.DataFrame(
            columns=[
                "title", "year", "audience_average_score",
                "total_audience_ratings", "domestic_box_office_gross"],
            data=[["Inception", 2010, 9.1, 1500000, 292576195],
                  ["The Dark Knight", 2008, 9.4, 2200000, 533345358],
                  ["Parasite", 2019, 9.0, 800000, 53369749]]
        )
        # check function extract of the class ExtractorProvider2
        with self.assertLogs() as captured:
            returned_df = self.ext_prov2.extract(
                correct_df.to_json().encode("utf-8"))
        # test correct logs
        pd.testing.assert_frame_equal(correct_df, returned_df)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 extractor] The data has been turned into a dataframe "\
            "object and contains the correct columns.")

    def test_extractor1_non_correct_columns_all(self):
        """
        This method checks if the method `extract` of class `ExtractProvider2`
        fails when all the columns are not correct by logging an error message
        and returning a None object.
        """
        # get data
        non_correct_df = pd.DataFrame(
            columns=["feat1", "feat2"],
            data=[["Inception", 2010], ["The Dark Knight", 2008],
                  ["Parasite", 2019]])
        # check function extract of the class ExtractorProvider2
        bytes_data = non_correct_df.to_json().encode("utf-8")
        with self.assertLogs() as captured:
            returned_df = self.ext_prov2.extract(bytes_data)
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 extractor] The data does not contain the proper columns.")
    
    def test_extractor1_non_correct_one_column(self):
        """
        This method checks if the method `extract` of class `ExtractProvider2`
        fails when one of the column is incorrect, by logging an error message
        and returning a None object.
        """
        # get data
        non_correct_df = pd.DataFrame(
            columns=[
                "movie_title", "year", "audience_average_score",
                "total_audience_ratings", "domestic_box_office_gross"],
            data=[["Inception", 2010, 9.1, 1500000, 292576195],
                  ["The Dark Knight", 2008, 9.4, 2200000, 533345358],
                  ["Parasite", 2019, 9.0, 800000, 53369749]]
        )
        # check function extract of the class ExtractorProvider2
        with self.assertLogs() as captured:
            returned_df = self.ext_prov2.extract(
                non_correct_df.to_json().encode("utf-8"))
        # test correct logs
        self.assertEqual(returned_df, None)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 extractor] The data does not contain the proper columns.")

    def test_extractor1_one_column_missing(self):
        """
        This method checks if the method `extract` of class `ExtractProvider2`
        works properly even if a column is missing.
        """
        # get data
        one_missing_col_df = pd.DataFrame(
            columns=["title", "year", "total_audience_ratings", "domestic_box_office_gross"],
            data=[["Inception", 2010, 1500000, 292576195],
                  ["The Dark Knight", 2008, 2200000, 533345358],
                  ["Parasite", 2019, 800000, 53369749]]
        )
        # check function extract of the class ExtractorProvider2
        with self.assertLogs() as captured:
            returned_df = self.ext_prov2.extract(
                one_missing_col_df.to_json().encode("utf-8"))
        # test correct logs
        pd.testing.assert_frame_equal(returned_df, one_missing_col_df)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider2 extractor] The data has been turned into a dataframe "\
            "object and contains the correct columns.")
