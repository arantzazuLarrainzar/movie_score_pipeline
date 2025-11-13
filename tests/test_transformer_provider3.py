import unittest
import pandas as pd
from modules.transforms import TransformProvider3


class TestTransformProv3(unittest.TestCase):
    """
    This class checks the behavior of the method `transform` of class
    `TransformProvider3`.
    """
    tran_csv: TransformProvider3

    # def setUp(self):
    @classmethod
    def setUpClass(cls):
        cls.tran_csv = TransformProvider3()
        cls.data_dom = pd.DataFrame(
            columns=[
                "film_name", "year_of_release", "box_office_gross_usd"],
            data=[["Inception", 2010, 292576195],
                  ["The Dark Knight", 2008, 533345358]])
        cls.clean_dom = pd.DataFrame(
            columns=[
                "movie_title", "release_year",
                "domestic_box_office_gross_usd"],
            data=[["Inception", 2010, 292576195],
                  ["The Dark Knight", 2008, 533345358]])
        cls.clean_dom = cls.clean_dom.astype({
            "movie_title": "string", "release_year": "uint16",
            "domestic_box_office_gross_usd": "int64"})
        cls.clean_dom.set_index(["movie_title", "release_year"],
                                inplace=True)
        
        cls.data_int = pd.DataFrame(
            columns=[
                "film_name", "year_of_release", "box_office_gross_usd"],
            data=[["Inception", 2010, 535700000],
                  ["The Dark Knight", 2008, 469700000]])
        cls.clean_int = pd.DataFrame(
            columns=[
                "movie_title", "release_year",
                "international_box_office_gross_usd"],
            data=[["Inception", 2010, 535700000],
                  ["The Dark Knight", 2008, 469700000]])
        cls.clean_int = cls.clean_int.astype({
            "movie_title": "string", "release_year": "uint16",
            "international_box_office_gross_usd": "int64"})
        cls.clean_int.set_index(["movie_title", "release_year"],
                                inplace=True)
        
        cls.data_fin = pd.DataFrame(
            columns=[
                "film_name", "year_of_release", "production_budget_usd",
                "marketing_spend_usd"],
            data=[["Inception", 2010, 160000000, 100000000],
                  ["The Dark Knight", 2008, 185000000, 150000000]])
        cls.clean_fin = pd.DataFrame(
            columns=[
                "movie_title", "release_year", "production_budget_usd",
                "marketing_spend_usd"],
            data=[["Inception", 2010, 160000000, 100000000],
                  ["The Dark Knight", 2008, 185000000, 150000000]],
            index=["movie_title", "release_year"])
        cls.clean_fin = cls.clean_fin.astype({
            "movie_title": "string", "release_year": "uint16",
            "production_budget_usd": "int64", "marketing_spend_usd": "int64"})
        cls.clean_fin.set_index(["movie_title", "release_year"],
                                inplace=True)

    # methods
    def test_transform_correct_dataframe(self):
        """
        This method checks if the method `transform` of class `TransformProvider3`
        works correctly when correct data is given.
        """
        # get data
        final_dfs = [self.clean_dom, self.clean_int, self.clean_fin]
        # check function extract of the class TransformProvider3
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform([
                self.data_dom, self.data_int, self.data_fin
            ])
        # test correct logs
        for indx in range(3):
            pd.testing.assert_frame_equal(final_dfs[indx], returned_df[indx])
        self.assertEqual(len(captured.records), 12)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider3 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider3 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider3 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")
        self.assertEqual(
            captured.records[3].getMessage(),
            "[Provider3 transformer] Data of file 0 has been turned into the "\
            "standard format.")

    def test_transform_one_column_missing(self):
        """
        This method checks if the method `transform` of class `TransformProvider3`
        works properly even if a column is missing.
        """
        # get data
        one_missing_col_clean = [
            self.clean_dom, self.clean_int,
            self.clean_fin.drop("marketing_spend_usd", axis=1)]
        one_missing_col_dfs = [
            self.data_dom, self.data_int,
            self.data_fin.drop("marketing_spend_usd", axis=1)]
        # check function extract of the class TransformProvider3
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_missing_col_dfs)
        # test correct logs
        for indx in range(3):
            pd.testing.assert_frame_equal(
                one_missing_col_clean[indx], returned_df[indx])
        self.assertEqual(len(captured.records), 12)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider3 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider3 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider3 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")
        self.assertEqual(
            captured.records[3].getMessage(),
            "[Provider3 transformer] Data of file 0 has been turned into the "\
            "standard format.")
    
    def test_transform_no_index_one_df(self):
        """
        This method checks if the method `transform` of class `TransformProvider3`
        fails when one of the fields for the index are missing.
        """
        # get data
        one_indx_missing_col_df_clean = [None, self.clean_int, self.clean_fin]
        one_indx_missing_col_dfs = [
            self.data_dom.drop("year_of_release", axis=1),
            self.data_int, self.data_fin]
        # check function extract of the class TransformProvider3
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_indx_missing_col_dfs)
        # test correct logs
        self.assertEqual(returned_df[0], None)
        pd.testing.assert_frame_equal(
            one_indx_missing_col_df_clean[1], returned_df[1])
        pd.testing.assert_frame_equal(
            one_indx_missing_col_df_clean[2], returned_df[2])

        self.assertEqual(len(captured.records), 11)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider3 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider3 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider3 transformer] The data does not contain any of the "\
            "columns `movie_title` or `release_year`, so it was not possible "\
            "to set them as index.")

    def test_transform_one_data_none(self):
        """
        This method checks if the method `transform` of class `TransformProvider3`
        works properly even if one of the datasets are missing, i.e., is equal
        to None.
        """
        # get data
        one_none_df_clean = [self.clean_dom, None, self.clean_fin]
        one_none_df = [self.data_dom, None, self.data_fin]
        # check function extract of the class TransformProvider3
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(one_none_df)
        # test correct logs
        pd.testing.assert_frame_equal(one_none_df_clean[0], returned_df[0])
        self.assertEqual(one_none_df_clean[1], returned_df[1])
        pd.testing.assert_frame_equal(one_none_df_clean[2], returned_df[2])
        # check logs
        self.assertEqual(len(captured.records), 8)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider3 transformer] The columns of the data have been "\
            "renamed.")
        self.assertEqual(
            captured.records[1].getMessage(),
            "[Provider3 transformer] The data types have been established in "\
            "the dataframe.")
        self.assertEqual(
            captured.records[2].getMessage(),
            "[Provider3 transformer] The columns `movie_title` and "\
            "`release_year` have been set as index in the givend data.")
        self.assertEqual(
            captured.records[3].getMessage(),
            "[Provider3 transformer] Data of file 0 has been turned into the "\
            "standard format.")

    def test_incorrect_length(self):
        """
        This method checks if the method `transform` of class `TransformProvider3`
        fails when the elements given as parameters are less than 3.
        """
        # get data
        incorrect_list = [self.clean_dom]
        # check function extract of the class TransformProvider3
        with self.assertLogs() as captured:
            returned_df = self.tran_csv.transform(incorrect_list)
        # test correct logs
        for indx in range(3):
            self.assertEqual(returned_df[indx], None)
        # check logs
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Provider3 transformer] All files that supplies provider 3 are "\
            "not used.")
