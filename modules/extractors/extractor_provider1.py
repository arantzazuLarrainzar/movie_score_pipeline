from .base_extractor import BaseExtractor
from typing import Optional, Set
import pandas as pd
import io


class ExtractorProvider1(BaseExtractor):
    """"""
    __columns: Set[str] = {
        "movie_title", "release_year", "critic_score_percentage",
        "top_critic_score", "total_critic_reviews_counted"
    }

    def __init__(self):
        super().__init__(provider_name="Provider1")
    
    def extract(self, raw_data: Optional[bytes]) -> Optional[pd.DataFrame]:
        # check if raw_data is None, any error has happen
        if raw_data is None:
            return None
        # raw_data contains information, turn it into a DataFrame
        df = pd.read_csv(io.BytesIO(raw_data))
        if not (set(df.columns) <= self.__columns):
            # the data is not correct
            self.log_err("The data does not contain the proper columns.")
            return None
        
        self.log_info(
            "The data has been turned into a dataframe object and contains "\
            "the correct columns.")
        return df
