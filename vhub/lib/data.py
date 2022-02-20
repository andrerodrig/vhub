from pathlib import Path
from typing import Dict, List, Union
import pandas as pd
import numpy as np


class Data:

    @staticmethod
    def save_csv_data(
        file: Union[Path, str],
        save_func,
        sep: str = ",",
        **kwargs
    ) -> List[Dict]:
        """
        Get a file from a url, does some processing on the dataset
        and saves the data through a given function, passed in `save_func`.

        Args:
            - file (Union[Path, str]): The file url. It can be a literal string
            or a instance of Path.
            - save_func (Function): The save function. This function must give
            the columns of the dataset. as keyword arguments,
            for example: save_func(col1="col1", col2="col2").
            - sep (str, optional): The separator pattern to the dataset.
            Defaults to ",".
        """
        try:
            df = Data._preprocess_dataset(pd.read_csv(file, sep=sep))
            kwargs_csv_cols = {
                k: v for k, v in kwargs.items() if v in df.columns
            }
            kwargs_func_args = {
                k: v
                for k, v in kwargs.items() if k not in kwargs_csv_cols.keys()
            }
            for _, row in df.iterrows():
                dict_to_save = {
                    k: row_value
                    for k, row_value in zip(
                        kwargs_csv_cols.keys(), row.to_dict().values()
                    )
                }
                save_func(**kwargs_func_args, **dict_to_save)
        except ValueError as exc:
            if "Invalid file path" in str(exc):
                raise ValueError("Failed to save. Invalid dataset file path.")
            else:
                raise exc
        except Exception as exc:
            raise exc

    @staticmethod
    def _preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
        """Read the dataframe and realize some preprocessing,
        in order to make it readable by ORMs.

        Args:
            df (pd.DataFrame): DataFrame to be processed.

        Raises:
            AttributeError: Raised when the dataset argument is passed as None.

        Returns:
            pd.DataFrame: Preprocessed dataframe.
        """
        try:
            return df.replace(np.nan, None)
        except AttributeError as exc:
            if "NoneType" in str(exc):
                raise AttributeError(
                    "Processing failed. The dataset cannot be None."
                )
