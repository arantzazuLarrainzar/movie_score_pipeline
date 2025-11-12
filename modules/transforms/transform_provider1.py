from .base_transform import BaseTransform
from typing import Optional, Dict
import pandas as pd


class TransformProvider1(BaseTransform):
    """
    Transform class that standarize the data that comes from the first
    provider.
    """
    # attributes
    __data_types: Dict[str, str] = {
        "movie_title": "string", "release_year": "uint16",
        "critic_score_percentage": "uint8", "top_critic_score": "float32",
        "total_critic_reviews_counted": "int32"
    }

    # constructor
    def __init__(self):
        super().__init__(provider_name="Provider1")

    # method
    def transform(self, data: Optional[pd.DataFrame]) -> Optional[pd.DataFrame]:
        if data is None:
            return None
        # the names are correct, so only ensure data types and set index
        new_df = self._set_data_types(data, self.__data_types)
        return self._set_index(new_df)
