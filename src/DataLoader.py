import fiftyone as fo
import logging
import os
from typing import Type
import pathlib


class DataLoader:
    def __init__(self, volume_path: str) -> None:
        self.volume_path = volume_path

    def _demo_dataset(self, demo_name: str="quickstart") -> Type[fo.Dataset]:
        logging.info(f"Loading demo dataset: {demo_name}")
        import fiftyone.zoo as foz
        return foz.load_zoo_dataset(demo_name)

    def load_data(self, config: dict) -> Type[fo.Dataset]:
        
        # patch fix: fix known bug in gcsfuse where you have to define a folder path before it is searchable in some cases.
        data_path = f"{self.volume_path}/{config['bucket_path_prefix']}"
        pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
        logging.info(f"Data path: {data_path}")



        # Load Data
        dataset_raw = fo.Dataset.from_dir(
            dataset_dir=data_path,
            dataset_type=fo.types.ImageDirectory,
            name=config["name"]
        )



        return dataset_raw