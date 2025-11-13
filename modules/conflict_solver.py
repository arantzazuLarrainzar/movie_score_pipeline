import logging
import pandas as pd
from typing import Optional, List


class ConflictSolver:
    """
    Class responsible for solving the conflicts to merge two datasets.

    Methods:
        merge_two_datasets: merge two datasets avoiding conflicts in the data.
    """
    def merge_two_datasets(
        self, first_df: Optional[pd.DataFrame],
        second_df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
        pass