import pandas as pd
from typing import Optional, Dict

class DataPipeline:
    """Movie Score Data Pipeline

    This class contains methods to ingest, clean, standarize and combine movie
    data from three different providers.

    Attributes:
        output_file_path (str): path where the file where the movie score data
        is saved.
        provider1_file_path (str): CSV file path where the first provider
        uploads the critics' scores weekly.
        provider2_file_path (str): JSON file path where the second provider
        uploads the audience ratings and box office data of the movies every 15
        days.
        provider3_dom_file_path (str): CSV file path where the third provider
        uploads the domestic box office data monthly.
        provider3_int_file_path (str): CSV file path where the third provider
        uploads the international box office data monthly. 
        provider3_fin_file_path (str): CSV file path where the third provider
        uploads the financial data of the movies monthly. 
    
    Methods:
    __transform(df, column_map): this method standarizes the given dataframe,
    `df`, by modifying the column names according to the `column_map`, if it is
    given, and setting the columns `movie_title` and `release_year` as index.
    __provider1(): returns the data given by the first provider in a pandas
    DataFrame.
    __provider2(): returns the data given by the second provider in a pandas
    DataFrame.
    __provider3(): returns the data given by the third provider in a pandas
    DataFrame.
    """
    # attributes
    output_file_path: str = "data/output.csv"
    provider1_file_path: str = "data/provider1.csv"
    provider2_file_path: str = "data/provider2.json"
    provider3_dom_file_path: str = "data/provider3_domestic.csv"
    provider3_int_file_path: str = "data/provider3_international.csv"
    provider3_fin_file_path: str = "data/provider3_financials.csv"

    # methods
    def __transform(
        self, df: pd.DataFrame, column_map: Optional[Dict[str, str]] = None
        ) -> pd.DataFrame:
        """
        This method performs the necessary transformation for the given data,
        `df`. It changes the names of some columns if it is necessary, and sets
        as index of the data the columns `movie_title` and `release_year`.
        
        Parameters:
            df (pandas.DataFrames): object containing the data that must be
            standarized.
            column_map (dictionary, optional): object that contains as keys the
            names of the columns that must be renamed from `df`, and as values
            the new names.

        Returns:
            pandas.DataFrame: object containing the standarized data. 
        """
        # clean and standarize the data
        cleaned_df: pd.DataFrame
        if(column_map is not None):
            cleaned_df = df.rename(columns=column_map, inplace=False)
            cleaned_df.set_index(["movie_title", "release_year"], inplace=True)
        else:
            cleaned_df = df.set_index(
                ["movie_title", "release_year"], inplace=False)
        # return the new version of the data
        return cleaned_df

    def __provider1(self) -> pd.DataFrame:
        """
        This function reads the file `provider1.csv` and returns the data in a
        pandas DataFrame with the correct structure.

        Returns:
            pandas.DataFrame: data structure maintaining the data in
            `provider1.csv`.
        """
        # extract and transform
        data: pd.DataFrame = pd.read_csv(self.provider1_file_path)
        data = self.__transform(data)
        # load
        return data
    
    def __provider2(self) -> pd.DataFrame:
        """
        This function reads the file `provider2.json` and returns the data in a
        pandas DataFrame with the correct structure.

        Returns:
            pandas.DataFrame: data structure maintaining the data in
            `provider2.csv`.
        """
        # extract and transform
        data: pd.DataFrame = pd.read_json(
            self.provider2_file_path, orient='records', typ='frame')
        data = self.__transform(
            data, column_map={"title": "movie_title", "year": "release_year"})
        # load
        return data

    def __provider3(self) -> pd.DataFrame:
        """
        This function reads from three different files and returns the data in a
        pandas DataFrame with the correct structure. Each of the files contain
        different information, and those files are: `provider3_domenstic.csv`,
        `provider3_international.csv`, and `provider3_financials.csv`.

        Returns:
            pandas.DataFrame: data structure maintaining the data of three
            different files.
        """
        # extract and transform data
        ### first file
        df_file1: pd.DataFrame = pd.read_csv(self.provider3_dom_file_path)
        df_file1 = self.__transform(df_file1, column_map={
            "film_name": "movie_title", "year_of_release": "release_year",
            "box_office_gross_usd": "domestic_box_office_gross"})
        ### second file
        df_file2: pd.DataFrame = pd.read_csv(self.provider3_int_file_path)
        df_file2 = self.__transform(df_file2, column_map={
            "film_name": "movie_title", "year_of_release": "release_year",
            "box_office_gross_usd": "international_box_office_gross"})
        ### third file
        df_file3: pd.DataFrame = pd.read_csv(self.provider3_fin_file_path)
        df_file3 = self.__transform(df_file3, column_map={
            "film_name": "movie_title", "year_of_release": "release_year"})
        ### combine data into one dataframe
        data: pd.DataFrame = df_file1.join([df_file2, df_file3])
        # load
        return data
