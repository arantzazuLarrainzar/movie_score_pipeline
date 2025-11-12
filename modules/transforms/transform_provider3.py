from .base_transform import BaseTransform
from typing import Optional, Dict, List
import pandas as pd


class TransformProvider3(BaseTransform):
    """
    Transform class that standarize the data that comes from the third
    provider.
    """
    # attributes
    __data_types: Dict[str, str] = {
        "movie_title": "string", "release_year": "uint16",
        "domestic_box_office_gross": "int64",
        "international_box_office_gross": "int64",
        "production_budget_usd": "int64", "marketing_spend_usd": "int64"
    }
    __column_maps: List[Dict[str, str]] = [
        {
            "film_name": "movie_title", "year_of_release": "release_year",
            "box_office_gross_usd": "domestic_box_office_gross_usd"
        },
        {
            "film_name": "movie_title", "year_of_release": "release_year",
            "box_office_gross_usd": "international_box_office_gross_usd"
        },
        {
            "film_name": "movie_title", "year_of_release": "release_year"
        }
    ]

    # constructor
    def __init__(self):
        super().__init__(provider_name="Provider3")

    # method
    def transform(
        self, data: List[Optional[pd.DataFrame]]
    ) -> List[Optional[pd.DataFrame]]:
        # transform into the standard format each of the files that are given
        # by the third supplier
        new_dfs: List[Optional[pd.DataFrame]] = [None, None, None]
        if len(data) == 3:
            for indx in range(3):
                if data[indx] is not None:
                    # rename columns
                    new_df = self._rename(
                        data[indx], column_map=self.__column_maps[indx]) 
                    # set data types
                    new_df = self._set_data_types(new_df, self.__data_types)
                    # set index
                    new_dfs[indx] = self._set_index(new_df)
                    if new_dfs[indx] is not None:
                        # non error happened during the transformation phase
                        self.log_info(
                            f"Data of file {indx} has been turned into the "\
                            "standard format.")
        else:
            # not correct number of files
            self.log_err("All files that supplies provider 3 are not used.")
        
        return new_dfs
