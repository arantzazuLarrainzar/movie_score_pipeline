from .base_transform import BaseTransform
from typing import Optional, Dict
import pandas as pd


class TransformProvider2(BaseTransform):
    """
    Transform class that standarize the data that comes from the second
    provider.
    """
    # attributes
    __data_types: Dict[str, str] = {
        "movie_title": "string", "release_year": "uint16",
        "audience_average_score": "float32", "total_audience_ratings": "int32",
        "domestic_box_office_gross_usd": "int64"
    }
    __column_map: Dict[str, str] = {
        "title": "movie_title", "year": "release_year",
        "domestic_box_office_gross": "domestic_box_office_gross_usd"
    }

    # constructor
    def __init__(self):
        super().__init__(provider_name="Provider2")

    # method
    def transform(self, data: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
        if data is None:
            return None
        # rename columns
        new_df = self._rename(data, column_map=self.__column_map) 
        # set data types
        new_df = self._set_data_types(new_df, self.__data_types)
        # set index
        return self._set_index(new_df)
