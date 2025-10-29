import pandas as pd
from typing import Optional, Dict, List

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
        __transform(df, column_map): standarizes the given dataframe, `df`, by
        modifying the column names according to the `column_map`, if it is
        given, and setting the columns `movie_title` and `release_year` as index.
        __provider1(): returns the data given by the first provider in a pandas
        DataFrame.
        __provider2(): returns the data given by the second provider in a pandas
        DataFrame.
        __provider3(): returns the data given by the third provider in a pandas
        DataFrame.
        __ingest(): extracts data from the providers and returns a DataFrame that
        maintains a combination of the data, solving the possible conflicts.
        __combine(first_df, second_df): returns a combination of both pandas
        DataFrame provided as parameters. This method is used to combine the old
        version of the dataset with the new information given by the providers.
        update(): updates the dataset with the information given by the different
        providers.
        get(movie_title, release_year): returns the information about the movie
        with the title `movie_title` and released in the year `release_year`. 
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

    def __ingest(self) -> List[pd.DataFrame]:
        """
        This method extracts data from different providers and returns
        a DataFrame that maintains a combination of the data. Since
        there is a column that conflicts between two providers, care
        is taken to ensure that no errors occur.

        Returns:
            pandas.DataFrame: object containing all data obtained by
            different providers.
        """
        # ingest data from the different providers
        df_prov1: pd.DataFrame = self.__provider1()
        df_prov2: pd.DataFrame = self.__provider2()
        df_prov3: pd.DataFrame = self.__provider3()
        # solve the conflicts before merging all in one
        conflict_col: pd.Series = df_prov2["domestic_box_office_gross"].copy()
        for indx, elem in df_prov3["domestic_box_office_gross"].items():
            if indx not in df_prov2.index:
                conflict_col[indx] = [elem]
        # combine the datasets taking into account the conflict
        data: pd.DataFrame = df_prov1.join([
            df_prov2.drop("domestic_box_office_gross", axis=1), df_prov3.drop("domestic_box_office_gross", axis=1)
        ])
        # data = self.__transform(data)
        data["domestic_box_office_gross"] = conflict_col
        # return the resulted DataFrame cleaned
        return data

    def __combine(
        self, first_df: pd.DataFrame, second_df: pd.DataFrame) -> pd.DataFrame:
        """
        This method combines the elements that are in the first pandas.DataFrame
        with the second DataFrame, building a unique DataFrame that contains all
        the elements.
        
        Parameters:
            first_df (pandas.DataFrame): one of the pandas.DataFrame that must
            be combined with the other, making sure that the elements are not
            repeated.
            second_df (pandas.DataFrame): the other pandas.DataFrame that must
            be combined.
        
        Returns:
            pandas.DataFrame: object containing the information of both 
            DataFrames (`first_df` and `second_df`), by making sure that no
            elements are repeated. 
        """
        combined_df = first_df.copy()
        for indx, film_data in second_df.iterrows():
            if indx not in first_df.index:
                # film_data is not in the first dataframe
                combined_df.loc[indx, :] = film_data
            else:
                # film_data is in the first dataframe, check if there are any
                # empty field
                for indx_col_empty in first_df.columns[first_df.loc[indx].isna()]:
                    # fill the empty fields with the values of the second dataframe
                    combined_df.loc[indx, indx_col_empty] = second_df.loc[
                        indx, indx_col_empty]
        return combined_df

    def update(self):
        """
        This method updates the file in which the movie data is saved. For
        that, it first ingests the data from the different providers, combines
        it with the old version of the database into a pandas.DataFrames, and
        saves the new version into the file.
        """
        # ingest data
        new_data: pd.DataFrame = self.__ingest()
        try:
            # get data from memory and combines it with the ingested information
            old_data: pd.DataFrame = pd.read_csv(
                self.output_file_path, index_col=["movie_title", "release_year"]
            )
            new_data = self.__combine(old_data, new_data)
        except pd.errors.EmptyDataError:
            # the file is empty
            print("The file is empty, so it will be completely overwritten by"\
                  " the new data.")
        except FileNotFoundError:
            # the file does not exist
            print("The file does not exists, so a new file will be created "\
                  "with the new information.")
        finally:
            # save the new version into the output file
            new_data.to_csv(self.output_file_path)

    def get(self, movie_title: str, release_year: int) -> pd.Series:
        """
        This method returns the information of the movie with the title
        `movie_title` and released in the year `released_year`.

        Parameters:
            movie_title (str): name of the movie to look for.
            release_year (int): year in which the movie is released.
        
        Returns:
            pandas.Series: object containing the information related to the
            movie. If the movie does not exist in the database, an empty
            object is returned.
        """
        # get the information of the database
        try:
            data: pd.DataFrame = pd.read_csv("data/output.csv", index_col=["movie_title", "release_year"])
        except pd.errors.EmptyDataError:
            # the file is empty
            print("The file is empty.")
            return pd.Series([], dtype=float)
        except FileNotFoundError:
            # the file does not exist
            print("The file does not exists.")
            return pd.Series([], dtype=float)

        # check if the movie is there
        if (movie_title, release_year) in data.index:
            return data.loc[(movie_title, release_year), :]
        # return an empty object because the movie is not there
        return pd.Series([], dtype=float)
