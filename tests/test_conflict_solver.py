import unittest
import pandas as pd
from modules import ConflictSolver


class TestConflictSolver(unittest.TestCase):
    """
    This class checks the behavior of the methods of the class
    `ConflictSolver`.
    """
    conf_solv: ConflictSolver

    @classmethod
    def setUpClass(cls):
        cls.conf_solv = ConflictSolver()
        cls.first_df = pd.DataFrame(
            columns=[
                "movie_title", "release_year", "production_budget_usd",
                "marketing_spend_usd"],
            data=[
                ["Inception", 2010, 160000000, 100000000],
                ["The Dark Knight", 2008, 185000000, 150000000]])
        cls.first_df.set_index(["movie_title", "release_year"], inplace=True)
        cls.second_df = pd.DataFrame(
            columns=["movie_title", "release_year", "box_office_gross_usd"],
            data=[["Inception", 2010, 292576195],
                    ["The Dark Knight", 2008, 533345358]])
        cls.second_df.set_index(["movie_title", "release_year"], inplace=True)
        cls.df_merged = pd.DataFrame(
            columns=[
                "movie_title", "release_year", "production_budget_usd",
                "marketing_spend_usd", "box_office_gross_usd"],
            data=[
                ["Inception", 2010, 160000000, 100000000, 292576195],
                ["The Dark Knight", 2008, 185000000, 150000000, 533345358]])
        cls.df_merged.set_index(["movie_title", "release_year"], inplace=True)
    
    def test_merge_correct_dataframes(self):
        """
        This method checks if the method `merge_two_datasets` works properly 
        when both dataframe are correct.
        """
        # merge them
        with self.assertLogs() as capture:
            returned_df = self.conf_solv.merge_two_datasets(
                self.first_df, self.second_df)
        # check if the method works properly
        pd.testing.assert_frame_equal(self.df_merged, returned_df)
        self.assertEqual(len(capture.records), 1)
        self.assertEqual(capture.records[0].getMessage(),
                         "[Conflict solver] The datasets have been merged.")

    def test_merge_first_df_none(self):
        """
        This method checks if the method `merge_two_datasets` works properly 
        when the first dataframe is not given, i.e., it is equal to zero.
        """
        # merge them
        with self.assertLogs() as capture:
            returned_df = self.conf_solv.merge_two_datasets(None, self.second_df)
        # check if the method works properly
        pd.testing.assert_frame_equal(self.second_df, returned_df)
        self.assertEqual(len(capture.records), 1)
        self.assertEqual(capture.records[0].getMessage(),
                         "[Conflict solver] The datasets have been merged.")

    def test_merge_second_df_none(self):
        """
        This method checks if the method `merge_two_datasets` works properly
        when the second dataframe is not given, i.e., it is equal to zero.
        """
        # merge them
        with self.assertLogs() as capture:
            returned_df = self.conf_solv.merge_two_datasets(self.first_df, None)
        # check if the method works properly
        pd.testing.assert_frame_equal(self.first_df, returned_df)
        self.assertEqual(len(capture.records), 1)
        self.assertEqual(capture.records[0].getMessage(),
                         "[Conflict solver] The datasets have been merged.")
    
    def test_merge_conflict(self):
        """
        This method checks if the method `merge_two_datasets` shows an error
        message when there is a conflict.
        """
        # get data
        first_df_conf = self.first_df.rename(
            {"production_budget_usd": "box_office_gross_usd"})
        first_df_conf.loc[
            ("Inception", 2010), "box_office_gross_usd"] = 292576195
        final_df = self.df_merged.drop(("The Dark Knight", 2008), axis=0)
        # merge them
        with self.assertLogs() as capture:
            returned_df = self.conf_solv.merge_two_datasets(
                first_df_conf, self.second_df)
        # check if the method works properly
        returned_df=returned_df.astype({"box_office_gross_usd": "int64"})
        pd.testing.assert_frame_equal(final_df, returned_df)
        self.assertEqual(len(capture.records), 2)
        self.assertEqual(
            capture.records[0].getMessage(),
            "[Conflict solver] There are a conflict with the data"\
            " of film The Dark Knight. This row is deleted as it is not"\
            " possible to check which data is correct.")
        self.assertEqual(capture.records[1].getMessage(),
                         "[Conflict solver] The datasets have been merged.")
