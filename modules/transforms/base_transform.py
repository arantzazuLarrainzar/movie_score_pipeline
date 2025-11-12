from abc import ABC, abstractmethod
from typing import Optional, Dict
import pandas as pd
import logging


class BaseTransform(ABC):
    """
    Abstract base class for all provider transformers. This class defines the
    interface each transformer class must be shared.
    """
    # attributes
    provider_name: str
    
    # constructor
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    # methods
    @abstractmethod
    def transform(self, data: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        This method transforms the given data as parameter into the standard
        format. To do this, it renames the columns and ensures the data types.
        If an error happens or has occurred previously, resulting in `data`
        being None, this method returns an empty object, i.e., None.

        Parameters:
            data (pandas.DataFrame or None): object containing the data that 
            must be standarized. It is possible that `data` contains an empty
            object, it could happen if any error has happened in any previous
            step.
        
        Returns:
            pandas.DataFrame or None: the standard dataframe of `data` if it is
            different to None and no error occurs during the procedure.
        """
        pass
    
    def _rename(
        self, data: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
        """
        This method modifies the name of the columns as the parameter
        `column_map` establishes.

        Parameters:
            data (pandas.DataFrame): object containing the data that is
            analysed.
            column_map (dict): dictionary containing as keys the current names
            of the columns that must be renamed with the corresponding values
            of the dictionary.
        
        Returns:
            pandas.DataFrame: the dataframe after changing the names of some
            columns.
        """
        df_new = data.rename(columns=column_map, inplace=False)
        self.log_info("The columns of the data have been renamed.")
        return df_new

    def _set_data_types(
        self, data: pd.DataFrame, data_types: Dict[str, str]
    ) -> Optional[pd.DataFrame]:
        """
        This method changes the type of each column as the parameter
        `data_types` establishes.

        Parameters:
            data (pandas.DataFrame): object containing the data that is
            modified.
            column_map (dict): dictionary containing as keys the names of the
            columns that must be modified with the corresponding data types
            that are as values.
        
        Returns:
            pandas.DataFrame or None: the dataframe after changing the data
            types of some columns or None, if any error happens.
        """
        # get the name of the columns that their type is going to be set
        col_data_types = {
            col_name: dt for col_name, dt in data_types.items()
            if col_name in data.columns
        }
        # set the data types
        new_data: Optional[pd.DataFrame]
        try:
            new_data = data.astype(
                col_data_types, copy=True, errors="raise")
            self.log_info(
                "The data types have been established in the dataframe.")
        except ValueError:
            self.log_err(
                "Any of the data types for the columns of the data does not "\
                "correspond with its values.")
            new_data = None
        return new_data

    def _set_index(self, data: Optional[pd.DataFrame]) -> pd.DataFrame:
        """
        This method sets the columns `movie_title` and `release_year` as index
        of the dataframe.

        Parameters:
            data (pandas.DataFrame or None): object that contains the dataframe
            or None if any error has happened before.
        
        Returns:
            pandas.DataFrame or None: object with the new index or None if any
            error has happen or the parameter `data` has an incorrect value.
        """
        # empty object
        if data is None:
            return None
        # set index
        df_new_indx: Optional[pd.DataFrame]
        try:
            df_new_indx = data.set_index(["movie_title", "release_year"])
            self.log_info(
                "The columns `movie_title` and `release_year` have been set "\
                "as index in the givend data.")
        except KeyError:
            self.log_err(
                "The data does not contain any of the columns `movie_title` "\
                "or `release_year`, so it was not possible to set them as "\
                "index.")
            df_new_indx = None
        return df_new_indx

    def log_info(self, msg: str):
        """
        Logging the message that is required.

        Parameters:
            msg (str): message that must be logged.
        """
        logging.info("[{} transformer] {}".format(self.provider_name, msg))
    
    def log_err(self, msg: str):
        """
        Logging the error message that is required.

        Parameters:
            msg (str): message that must be logged.
        """
        logging.error("[{} transformer] {}".format(self.provider_name, msg))