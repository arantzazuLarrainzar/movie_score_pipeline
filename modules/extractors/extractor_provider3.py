from .base_extractor import BaseExtractor
from typing import Optional, Set, List
import pandas as pd
import io


class ExtractorProvider3(BaseExtractor):
    """"""
    __columns: Set[str] = {
        "film_name", "year_of_release", "box_office_gross_usd",
        "production_budget_usd", "marketing_spend_usd"
    }

    def __init__(self):
        super().__init__(provider_name="Provider3")
    
    def extract(self, raw_data: Optional[List[bytes]]) -> Optional[List[pd.DataFrame]]:
        # check if raw_data is None, any error has happen
        if raw_data is None:
            return None
        if len(raw_data) != 3:
            return None
        # raw_data contains information, turn it into a DataFrame
        res_dfs: List[pd.DataFrame] = [None, None, None]
        for indx in range(3):
            df = pd.read_csv(io.BytesIO(raw_data[indx]))
            if not (set(df.columns) <= self.__columns):
                # the data is not correct
                self.log_err(f"The data {indx} does not contain the proper"\
                              " columns.")
                res_dfs[indx] = None
            else:
                self.log_info(
                    f"The data {indx} has been turned into a dataframe object and "\
                    "contains the correct columns.")
                res_dfs[indx] = df
        return res_dfs
