import logging
import pandas as pd
from typing import Optional, List, Union


class ConflictSolver:
    """
    Class responsible for solving the conflicts to merge two datasets.

    Methods:
        merge_two_datasets: merge two datasets avoiding conflicts in the data.
    """
    def merge_two_datasets(
        self, first_df: Optional[pd.DataFrame],
        second_df: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        This method merges two dataframes. If there are any conflict, an error
        message is logged and the information is deleted from the merged
        dataframe since there is no way to know which of the entries are
        correct.
        
        Parameters:
            first_df (pandas.DataFrame): pandas dataframe object to merge.
            second_df (list of pandas.DataFrame or None): pandas dataframe
            object to merge.

        Returns:
            pandas.DataFrame: final pandas dataframe object that contains the
            data of both parameters (`first_df` and `second_df`).
        """
        # check if any of the parameters are an empty object
        if first_df is None:
            logging.info("[Conflict solver] The datasets have been merged.")
            return second_df.copy()
        if second_df is None:
            logging.info("[Conflict solver] The datasets have been merged.")
            return first_df.copy()
        #
        new_df = first_df.copy()
        indx_first_df = first_df.index
        # add columns of `second_df` that are not in `first_df` in `first_df`
        # and fill values of those columns with the object None
        col_df2 = second_df.columns
        diff_cols = list(set(col_df2) - set(first_df.columns))
        conflict_cols = [
            col_name for col_name in second_df.columns
            if col_name not in diff_cols]
        new_df.loc[:, diff_cols] = None
        # iterate over `second_df`
        for indx in second_df.index:
            # check if values of `second_df` are in `first_df`
            if indx in indx_first_df:
                # the movie is in first_df
                # fill values that do not cause conflict
                new_df.loc[indx, diff_cols] = second_df.loc[indx, diff_cols]
                # check if there are conflicts in the other columns
                for col in conflict_cols:
                    if new_df.loc[indx, col] is None or pd.isna(new_df.loc[indx, col]):
                        # no conflict, since the element of new_df is empty
                        new_df.loc[indx, col] = second_df.loc[indx, col]
                    elif new_df.loc[indx, col] != second_df.loc[indx, col]:
                        # conflict
                        logging.error(
                            "[Conflict solver] There are a conflict with the "\
                            f"data of film {indx[0]}. The element that causes"\
                            " the effect is removed, since it is not possible"\
                            " to check which data is correct.")
                        new_df.loc[indx, col] = None
            else:
                # movie is not in first_df, so add it completely
                new_df.loc[indx, col_df2] = second_df.loc[indx, :]
        # return the final dataframe with both parameters merged
        logging.info("[Conflict solver] The datasets have been merged.")
        return new_df
    
    def merge_entire_dataset(
        self, main_df: pd.DataFrame, dfs: Union[List[pd.DataFrame], pd.DataFrame]
    ) -> pd.DataFrame:
        """"""
        if isinstance(dfs, pd.DataFrame):
            main_df = self.merge_two_datasets(main_df, dfs)
        else:
            # different dfs
            for indx in range(len(dfs)):
                main_df = self.merge_two_datasets(main_df, dfs[indx])
        # return merged file
        return main_df
