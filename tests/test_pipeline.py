import unittest
import pandas as pd
from modules import DataPipeline


class TestDataPipeline(unittest.TestCase):
    """
    This class tests the methods implemented in DataPipeline class.
    """
    # attributes
    pipe: DataPipeline

    # methods
    def setUp(self):
        """"""
        self.pipe = DataPipeline()
        self.pipe.config.read("./config/config_test.ini")

    def test_run_provider(self):
        """
        This methods checks if the function `run_one_provider` saves correctly
        the information supplied by the Provider 1.
        """
        # data
        correct_data: pd.DataFrame = pd.read_csv("./tests/data/provider1.csv")
        correct_data = correct_data.astype({
            "movie_title": "string", "release_year": "uint16",
            "critic_score_percentage": "uint8", "top_critic_score": "float32",
            "total_critic_reviews_counted": "int32"})
        correct_data.set_index(["movie_title", "release_year"], inplace=True)
        # run method
        with self.assertLogs() as captured:
            self.pipe.run_one_provider("provider1")
        # check result
        saved_data = pd.read_csv("tests/data/output.csv")
        saved_data.set_index(["movie_title", "release_year"], inplace=True)

        print("\n\n")
        for col in correct_data.columns:
            print(col)
            pd.testing.assert_series_equal(correct_data[col], self.pipe.current_data[col])
            pd.testing.assert_series_equal(correct_data[col], saved_data[col])
        pd.testing.assert_index_equal(correct_data.index, self.pipe.current_data.index)
        pd.testing.assert_index_equal(correct_data.index, saved_data.index)
        # check logs
        self.assertEqual(len(captured.records), 6)
        self.assertEqual(
            captured.records[0].getMessage(),
            "[Data Pipeline] Running pipeline for provider: provider1")
        