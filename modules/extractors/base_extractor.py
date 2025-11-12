from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
import logging


class BaseExtractor(ABC):
    """
    Abstract base class for all provider extractors. This class defines the
    interface each extractor class must be shared.
    """
    # attributes
    provider_name: str
    
    # constructor
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    # methods
    @abstractmethod
    def extract(self, raw_data: Optional[bytes]) -> Optional[pd.DataFrame]:
        """
        This method turns the information in bytes into a pandas.DataFrame and
        checks if it has the correct columns. If `raw_data` is None or the
        final DataFrame has not the correct columns, the method returns None.

        Parameters:
            raw_data (bytes or None): object that contains the information that
            must be turned into a pandas.DataFrame. If `raw_data` is None, it
            means that the file where the data was could not been read.
        
        Returns:
            pandas.DataFrame or None: the result DataFrame after turning the
            bytes into a pandas.DataFrame if any exception does not arraise.
        """
        pass
    
    def log_info(self, msg: str):
        """
        Logging the message that is required.

        Parameters:
            msg (str): message that must be logged.
        """
        logging.info("[{} extractor] {}".format(self.provider_name, msg))
    
    def log_err(self, msg: str):
        """
        Logging the error message that is required.

        Parameters:
            msg (str): message that must be logged.
        """
        logging.error("[{} extractor] {}".format(self.provider_name, msg))