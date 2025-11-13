import logging
import pandas as pd
from typing import Optional, Union, List


class FileIO:
    """
    Class responsible for reading and writing files.

    Methods:
        read_file: this method reads files and transforms the data into bytes.
        If any error happens, it returns an empty object, i.e., a None object.
        write_csv: this method writes down the dataframe object that is passed
        as a parameter into a csv file.
    """
    # methods
    def read_file(
        self, path: Union[List[str], str]
    ) -> Union[Optional[bytes], List[Optional[bytes]]]:
        """
        This method returns the data that is inside the file in `path` in a
        bytes object.
        
        Parameters:
            path (list of str or str): list of routes where different file are
            stored and must be read or a string if there is only one file to
            read.
        
        Returns:
            list of bytes or bytes: object that contains the information of the
            file(s) that were read. If any error happens, the bytes object of
            the file being read is equal to None.
        """
        res: Union[List[Optional[bytes]], bytes]
        if isinstance(path, list):
            # the given data as parameters is a list, so it contains different
            # files to read
            res = [None] * len(path)
            for indx in range(len(path)):
                res[indx] = self.__read_one_file(path[indx])
        else:
            # read only one file
            res = self.__read_one_file(path)
        return res
    
    def __read_one_file(self, path: str) -> Optional[bytes]:
        """
        This method reads the file that is given as parameters and returns a
        bytes object.
        
        Parameters:
            path (str): place where the file is saved in memory.
        
        Returns:
            bytes or None: bytes object containing the information that was
            read from the file or None if any error happened. 
        """
        try:
            # read the file in `path`
            with open(path, "rb") as f:
                logging.info("[File IO] The file in '{}' has been read.".format(path))
                return f.read()
        except FileNotFoundError:
            # the file does not exist
            logging.error("[File IO] The file in '{}' does not exist.".format(path))
        except PermissionError:
            # the file can not be accessed
            logging.error("[File IO] The file in '{}' can not be accessed.".format(path))
    
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
        try:
            data.to_csv(path)
            logging.info(
                "[File IO] The data has been saved into the CSV file in "\
                f"'{path}'")
        except PermissionError:
            # there are no permissions to write in `path`
            logging.error("[File IO] There are no permissions to write in "\
                          "'{}'.".format(path))
