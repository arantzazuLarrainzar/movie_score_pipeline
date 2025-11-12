from .base_extractor import BaseExtractor
from typing import Optional, Set
import pandas as pd


class ExtractorProvider2(BaseExtractor):
    """"""
    __columns: Set[str] = {
        "title", "year", "audience_average_score",
        "total_audience_ratings", "domestic_box_office_gross"
    }

    def __init__(self):
        super().__init__(provider_name="Provider2")
    
    def extract(self, raw_data: Optional[bytes]) -> Optional[pd.DataFrame]:
        # check if raw_data is None, any error has happen
        if raw_data is None:
            return None
        # raw_data contains information, turn it into a DataFrame
        df = pd.read_json(raw_data.decode("utf-8"))
        if not (set(df.columns) <= self.__columns):
            # the data is not correct
            self.log_err("The data does not contain the proper columns.")
            return None
        
        self.log_info(
            "The data has been turned into a dataframe object and contains "\
            "the correct columns.")
        return df
