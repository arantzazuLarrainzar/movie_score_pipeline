import logging
import pandas as pd
from typing import Optional


class FileIO:
    """
    """
    def read_file(self, path: str) -> Optional[bytes]:
        """
        This method returns the data that is inside the file in `path` in a
        bytes object.
        
        Parameters:
            path (str): route where the file is store.
        
        Returns:
            bytes: object that contains the information of the file that is
            found in `path`.
        """
        try:
            # read the file in `path`
            with open(path, "rb") as f:
                logging.info("The file in '{}' has been read.".format(path))
                return f.read()
        except FileNotFoundError:
            # the file does not exist
            logging.error("The file in '{}' does not exist.".format(path))
        except PermissionError:
            # the file can not be accessed
            logging.error("The file in '{}' can not be accessed.".format(path))
        
        return None
    
    def write_csv(self, path: str, data: pd.DataFrame):
        """
        This method saves the information in the pandas.DataFrame object into
        a csv in `path`.

        Parameters:
            path (str): route where `data` must be saved. The route must direct
            to a csv file.
            data (pandas.DataFrame): object containing the information to save
            in csv.
        """
        data.to_csv(path, index=False)
