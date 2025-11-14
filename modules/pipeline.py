# import modules
from .fileio import FileIO
from .extractors import BaseExtractor
from .extractors import ExtractorProvider1
from .extractors import ExtractorProvider2
from .extractors import ExtractorProvider3
from .transforms import BaseTransform
from .transforms import TransformProvider1
from .transforms import TransformProvider2
from .transforms import TransformProvider3
from .conflict_solver import ConflictSolver
# other libraries
import os.path
import logging
import pandas as pd
import configparser
from typing import Dict, List


class DataPipeline:
    """"""
    # attributes
    config: Dict[str, str]
    file_io: FileIO
    extractors: List[BaseExtractor]
    transformers: List[BaseTransform]
    conflict_solver: ConflictSolver
    current_data: pd.DataFrame

    # constructor
    def __init__(self):
        # set attributes
        ### configuration
        self.config = configparser.ConfigParser()
        self.config.read("./config/config.ini")
        ### pipeline
        if os.path.isfile(self.config["output_path"]["output"]):
            # file exists with previous data
            self.current_data = pd.read_csv(self.config["output_path"]["output"])
            self.current_data.set_index(["movie_title", "release_year"], inplace=True)
        else:
            # file does not exist
            self.current_data = pd.DataFrame(columns=["movie_title", "release_year"]).astype({"movie_title": "string", "release_year": "uint16"})
            self.current_data.set_index(["movie_title", "release_year"], inplace=True)
        self.file_io = FileIO()
        self.extractors = {
            "provider1": ExtractorProvider1(),
            "provider2": ExtractorProvider2(),
            "provider3": ExtractorProvider3()
        }
        self.transformers = {
            "provider1": TransformProvider1(),
            "provider2": TransformProvider2(),
            "provider3": TransformProvider3()
        }
        self.conflict_solver = ConflictSolver()
    
    # methods
    def run_one_provider(self, provider_name: str):
        """
        This method updates the database with the information given by the
        provider `provider_name`.
        
        Parameters:
            provider_name (str): name of the provider to get the data.
        """
        if provider_name not in self.config["paths"].keys():
            logging.error(
                f"[Data Pipeline] The provider `{provider_name}` is incorrect"\
                ", it will not be possible to update the database.")
            return None
        # correct provider
        logging.info(
            f"[Data Pipeline] Running pipeline for provider: {provider_name}")
        # start pipeline
        path = self.config["paths"][provider_name].split(',')
        if len(path) == 1:
            path = path[0]
        raw_data = self.file_io.read_file(path)
        extr_data = self.extractors[provider_name].extract(raw_data)
        trans_data = self.transformers[provider_name].transform(extr_data)
        conf_solve_data = self.conflict_solver.merge_entire_dataset(
            self.current_data, trans_data)
        # save new data into 
        if conf_solve_data is not None:
            self.current_data = conf_solve_data
            self.file_io.write_csv(self.config["output_path"]["output"], conf_solve_data)
    
    def run_all_providers(self):
        """
        This method updates the information of the database with all the data
        given by the different providers.
        """
        for provider_name in self.config["paths"].keys():
            self.run_one_provider(provider_name=provider_name)
        logging.info(
            "[Data Pipeline] The database has been completely updated by the "\
            "data of all the providers.")

    def get(self, movie_title: str, release_year: int) -> pd.Series:
        """
        This method returns the information related to the film that is queried.
        
        Parameters:
            movie_title (str): name of the movie.
            release_year (int): year of release of the movie.
        
        Returns:
            pandas.Series: a pandas series object containing the data related
            with the queried movie. If the movie does not exist in the
            database, the object is empty.
        """
        movie_info: pd.Series
        if (movie_title, release_year) in self.current_data.index:
            movie_info = self.current_data.loc[(movie_title, release_year)]
            logging.info(
                f"[Data Pipeline] The movie `{movie_title}` was saved in the "\
                "database, so its information has been obtained.")
        else:
            movie_info = pd.Series()
            logging.info(
                f"[Data Pipeline] The movie `{movie_title}` was not in the "\
                "database")
        return movie_info