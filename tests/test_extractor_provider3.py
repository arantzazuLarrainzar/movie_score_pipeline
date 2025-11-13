import unittest
import pandas as pd
from modules.extractors import ExtractorProvider3


class TestExtractorProv3(unittest.TestCase):
    """
    This class checks the behavior of the method `extract` of class
    `ExtractorProvider3`.
    """
    ext_csv: ExtractorProvider3

    # def setUp(self):
    @classmethod
    def setUpClass(cls):
        cls.ext_csv = ExtractorProvider3()

    # methods
    def test_extract_correct_csvs(self):
        """
        This method checks if the method `extract` of class `ExtractProvider3`
        works correctly when correct data is given.
        """
        # get data
        list_dfs = [
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "box_office_gross_usd"
                ], data=[
                    ["Inception", 2010, 292576195],
                    ["The Dark Knight", 2008, 533345358]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "box_office_gross_usd"
                ], data=[
                    ["Inception", 2010, 535700000],
                    ["The Dark Knight", 2008, 469700000]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "production_budget_usd",
                    "marketing_spend_usd"
                ], data=[
                    ["Inception", 2010, 160000000, 100000000],
                    ["The Dark Knight", 2008, 185000000, 150000000]
                ])
        ]
        # check function extract of the class ExtractorProvider3
        list_raw_data = [
            df.to_csv(index=False).encode("utf-8") for df in list_dfs]
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(list_raw_data)
        # test correct logs
        self.assertEqual(len(captured.records), 3)
        for indx in range(3):
            pd.testing.assert_frame_equal(list_dfs[indx], returned_df[indx])
            self.assertEqual(
                captured.records[indx].getMessage(),
                f"[Provider3 extractor] The data {indx} has been turned into a"\
                " dataframe object and contains the correct columns.")

    def test_extract_one_incorrect_csv_one_incorrect_col(self):
        """
        This method checks if the method `extract` of class `ExtractProvider3`
        works even if one of the dataframes being incorrect. For that, it
        returns a None object in the space of the list where the incorrect
        dataframe was.
        """
        # get data
        list_dfs = [
            pd.DataFrame(
                columns=[
                    "movie", "year_of_release", "box_office_gross_usd"
                ], data=[
                    ["Inception", 2010, 292576195],
                    ["The Dark Knight", 2008, 533345358]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "box_office_gross_usd"
                ], data=[
                    ["Inception", 2010, 535700000],
                    ["The Dark Knight", 2008, 469700000]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "production_budget_usd",
                    "marketing_spend_usd"
                ], data=[
                    ["Inception", 2010, 160000000, 100000000],
                    ["The Dark Knight", 2008, 185000000, 150000000]
                ])
        ]
        # check function extract of the class ExtractorProvider3
        list_raw_data = [
            df.to_csv(index=False).encode("utf-8") for df in list_dfs]
        with self.assertLogs() as captured:
            returned_dfs = self.ext_csv.extract(list_raw_data)
        # test correct logs
        self.assertEqual(len(captured.records), 3)
        self.assertEqual(returned_dfs[0], None)
        self.assertEqual(
                captured.records[0].getMessage(),
                "[Provider3 extractor] The data 0 does not contain the "\
                "proper columns.")
        for indx in range(1, 3):
            pd.testing.assert_frame_equal(list_dfs[indx], returned_dfs[indx])
            self.assertEqual(
                captured.records[indx].getMessage(),
                f"[Provider3 extractor] The data {indx} has been turned into a"\
                " dataframe object and contains the correct columns.")

    
    def test_extract_non_correct_columns_all(self):
        """
        This method checks if the method `extract` of class `ExtractProvider3`
        fails when all the columns are not correct by logging an error message
        and returning a None object for each dataset.
        """
        # get data
        list_dfs = [
            pd.DataFrame(
                columns=["feat1", "feat2"], data=[["a", 2010], ["b", 2008]]),
            pd.DataFrame(
                columns=["feat3", "feat4"], data=[["a", 4534], ["b", 6758]]),
            pd.DataFrame(
                columns=["feat4", "feat5"], data=[["a", 2313], ["b", 3456]])
        ]
        # check function extract of the class ExtractorProvider3
        list_raw_data = [
            df.to_csv(index=False).encode("utf-8") for df in list_dfs]
        with self.assertLogs() as captured:
            returned_dfs = self.ext_csv.extract(list_raw_data)
        # test correct logs
        self.assertEqual(len(captured.records), 3)
        for indx in range(3):
            self.assertEqual(returned_dfs[indx], None)
            self.assertEqual(
                captured.records[indx].getMessage(),
                f"[Provider3 extractor] The data {indx} does not contain the "\
                "proper columns.")
    
    def test_extract_one_missing_col(self):
        """
        This method checks if the method `extract` of class `ExtractProvider3`
        works properly even if one of the datasets has a missing column.
        """
        # get data
        list_dfs = [
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release"
                ], data=[
                    ["Inception", 2010],
                    ["The Dark Knight", 2008]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "box_office_gross_usd"
                ], data=[
                    ["Inception", 2010, 535700000],
                    ["The Dark Knight", 2008, 469700000]
                ]),
            pd.DataFrame(
                columns=[
                    "film_name", "year_of_release", "production_budget_usd",
                    "marketing_spend_usd"
                ], data=[
                    ["Inception", 2010, 160000000, 100000000],
                    ["The Dark Knight", 2008, 185000000, 150000000]
                ])
        ]
        # check function extract of the class ExtractorProvider3
        list_raw_data = [
            df.to_csv(index=False).encode("utf-8") for df in list_dfs]
        with self.assertLogs() as captured:
            returned_df = self.ext_csv.extract(list_raw_data)
        # test correct logs
        self.assertEqual(len(captured.records), 3)
        for indx in range(3):
            pd.testing.assert_frame_equal(list_dfs[indx], returned_df[indx])
            self.assertEqual(
                captured.records[indx].getMessage(),
                f"[Provider3 extractor] The data {indx} has been turned into a"\
                " dataframe object and contains the correct columns.")
