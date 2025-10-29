import unittest
from pipeline import DataPipeline

import pandas as pd


class TestPipeline(unittest.TestCase):
    # attributes
    df_provider1: pd.DataFrame
    df_provider2: pd.DataFrame
    df_provider3: pd.DataFrame
    df_comb: pd.DataFrame

    # methods
    def setUp(cls):
        """
        Declaration of the DataFrames that are going to be used in the
        different methods.
        """
        # data given by the first provider
        cls.df_provider1 = pd.DataFrame({
            "movie_title": ["Inception", "The Dark Knight", "Parasite"],
            "release_year": [2010, 2008, 2019],
            "critic_score_percentage": [87, 94, 99],
            "top_critic_score": [8.1, 8.6, 9.5],
            "total_critic_reviews_counted": [450, 350, 475]})
        cls.df_provider1.set_index(["movie_title", "release_year"], inplace=True)
        # second provider
        cls.df_provider2 = pd.DataFrame({
            "movie_title": ["Inception", "The Dark Knight", "Parasite"],
            "release_year": [2010, 2008, 2019],
            "audience_average_score": [9.1, 9.4, 9.0],
            "total_audience_ratings": [1500000, 2200000, 800000],
            "domestic_box_office_gross": [292576195, 533345358, 53369749]})
        cls.df_provider2.set_index(["movie_title", "release_year"], inplace=True)
        # third provider
        cls.df_provider3 = pd.DataFrame({
            "movie_title": ["Inception", "The Dark Knight"],
            "release_year": [2010, 2008],
            "domestic_box_office_gross": [292576195, 533345358],
            "international_box_office_gross": [535700000, 469700000],
            "production_budget_usd": [160000000, 185000000],
            "marketing_spend_usd": [100000000, 150000000]})
        cls.df_provider3.set_index(["movie_title", "release_year"], inplace=True)
        # combination of the three datasets
        cls.df_comb = pd.DataFrame({
            "movie_title": ["Inception", "The Dark Knight", "Parasite"],
            "release_year": [2010, 2008, 2019],
            "critic_score_percentage": [87.0, 94.0, 99.0],
            "top_critic_score": [8.1, 8.6, 9.5],
            "total_critic_reviews_counted": [450.0, 350.0, 475.0],
            "audience_average_score": [9.1, 9.4, 9.0],
            "total_audience_ratings": [1500000.0, 2200000.0, 800000.0],
            "international_box_office_gross": [535700000, 469700000, None],
            "production_budget_usd": [160000000, 185000000, None],
            "marketing_spend_usd": [100000000, 150000000, None],
            "domestic_box_office_gross": [292576195.0, 533345358.0, 53369749.0]
        })
        cls.df_comb.set_index(["movie_title", "release_year"], inplace=True)

    def test_transform(self):
        """
        Testing the method `__transform` without specifying a change in the
        name of the columns of the given dataframe.
        """
        # get the data on which the transformations are to be performed
        df: pd.DataFrame = pd.read_csv("data/provider1.csv")
        # get the expected results from the transform method
        pipe = DataPipeline()
        df_transformed = pipe._DataPipeline__transform(df)
        # check if the results are equal
        pd.testing.assert_frame_equal(self.df_provider1, df_transformed)
    
    def test_transform_rename(self):
        """
        Testing the method `__transform` by specifying a change in the name of
        the columns of the given data, as it must be done with the data that
        the second provider gives.
        """
        # get the data on which the transformations are to be performed
        df = pd.read_json("data/provider2.json", orient='records', typ='frame')
        # get the expected results from the transform method
        pipe = DataPipeline()
        df_transformed = pipe._DataPipeline__transform(df, column_map={
            "title": "movie_title", "year": "release_year"
        })
        # check if the results are equal
        pd.testing.assert_frame_equal(self.df_provider2, df_transformed)

    def test_provider1(self):
        """
        Testing the method `__provider1` that is in charge of extracting the
        data from the first provider and standarize it into the correct format.
        """
        # get df from method provider1
        pipe = DataPipeline()
        df_returned = pipe._DataPipeline__provider1()
        # check if both dfs are equal
        pd.testing.assert_frame_equal(self.df_provider1, df_returned)

    def test_provider2(self):
        """
        Testing the method `__provider2` that is in charge of extracting the
        data from the second provider and standarize it into the correct format.
        """
        # get df from method provider2
        pipe = DataPipeline()
        df_returned = pipe._DataPipeline__provider2()
        # check if both dfs are equal
        pd.testing.assert_frame_equal(self.df_provider2, df_returned)

    def test_provider3(self):
        """
        Testing the method `__provider3` that is in charge of extracting the
        data from the third provider and standarize it into the correct format.
        """
        # get df from method provider3
        pipe = DataPipeline()
        df_returned = pipe._DataPipeline__provider3()
        # check if both dfs are equal
        pd.testing.assert_frame_equal(self.df_provider3, df_returned)

    def test_ingest(self):
        """
        Testing the method `__ingest` that extracts the information of the
        different providers and returns a pandas DataFrame with all the data.
        """
        # expected result
        df_expected = pd.DataFrame({
            "movie_title": ["Inception", "The Dark Knight", "Parasite"],
            "release_year": [2010, 2008, 2019],
            "critic_score_percentage": [87, 94, 99],
            "top_critic_score": [8.1, 8.6, 9.5],
            "total_critic_reviews_counted": [450, 350, 475],
            "audience_average_score": [9.1, 9.4, 9.0],
            "total_audience_ratings": [1500000, 2200000, 800000],
            "international_box_office_gross": [535700000, 469700000, None],
            "production_budget_usd": [160000000, 185000000, None],
            "marketing_spend_usd": [100000000, 150000000, None],
            "domestic_box_office_gross": [292576195, 533345358, 53369749]
        })
        df_expected.set_index(["movie_title", "release_year"], inplace=True)
        # get the result after processing the ingest method
        pipe = DataPipeline()
        df_returned = pipe._DataPipeline__ingest()
        # check if each of the elements are equal
        pd.testing.assert_frame_equal(df_expected, df_returned)

    def test_update(self):
        """
        Testing the method `update` which must update the database with the new
        information given by the different providers.
        """
        # update the file in memory (output.csv)
        pipe = DataPipeline()
        pipe.update()
        # check if the result saved in `output.csv` file is equal to the expected
        df_saved = pd.read_csv("data/output.csv", index_col=["movie_title", "release_year"])
        pd.testing.assert_frame_equal(self.df_comb, df_saved)

    def test_get(self):
        """
        Testing the method `get` with different queries, since this method must return a pandas series when a film inside the database is asked, and an empty pandas series when it does not exist."""
        # test the different combinations saved in memory
        ### make sure the results are in memory
        pipe = DataPipeline()
        pipe.update()
        ### combinations of data to check
        check = [
            {"title": "Inception", "release_year": 2010, "output": pd.Series(
                [87, 8.1, 450, 9.1, 1500000, 535700000.0,
                 160000000.0, 100000000.0, 292576195],
                index=["critic_score_percentage", "top_critic_score",
                "total_critic_reviews_counted", "audience_average_score",
                "total_audience_ratings", "international_box_office_gross",
                "production_budget_usd", "marketing_spend_usd",
                "domestic_box_office_gross"], name=("Inception", 2010))},
            {"title": "The Dark Knight", "release_year": 2008, "output": pd.Series(
                [94, 8.6, 350, 9.4, 2200000, 469700000.0,
                 185000000.0, 150000000.0, 533345358],
                index=["critic_score_percentage", "top_critic_score",
                "total_critic_reviews_counted", "audience_average_score",
                "total_audience_ratings", "international_box_office_gross",
                "production_budget_usd", "marketing_spend_usd",
                "domestic_box_office_gross"], name=("The Dark Knight", 2008))},
            {"title": "Parasite", "release_year": 2019, "output": pd.Series(
                [99, 9.5, 475, 9.0, 800000, None, None, None, 53369749],
                index=["critic_score_percentage", "top_critic_score",
                "total_critic_reviews_counted", "audience_average_score",
                "total_audience_ratings", "international_box_office_gross",
                "production_budget_usd", "marketing_spend_usd",
                "domestic_box_office_gross"], name=("Parasite", 2019))},
            {"title": "Toy Story 2", "release_year": 1999,
             "output": pd.Series([], dtype=float)}
        ]
        ### check the different queries
        for test in check:
            result = pipe.get(test["title"], test["release_year"])
            pd.testing.assert_series_equal(test["output"], result)


if __name__ == '__main__':
    unittest.main()
