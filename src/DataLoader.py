from __future__ import annotations
import fiftyone as fo
import logging
from typing import Type
import pandas as pd
import pathlib
import time


class DataLoader:
    def __init__(self, volume_path: str, project_id: str = "") -> None:
        self.volume_path = volume_path
        self.project_id = project_id

    def _demo_dataset(self, demo_name: str = "quickstart") -> Type[fo.Dataset]:
        logging.info(f"Loading demo dataset: {demo_name}")
        import fiftyone.zoo as foz

        return foz.load_zoo_dataset(demo_name)

    def _load_bq(self, query: str, key: str) -> dict:
        df_bq = pd.read_gbq(query, project_id=self.project_id)
        return df_bq.set_index(key).T.to_dict()

    def load_dataset(self, config: dict, local: bool = True) -> Type[fo.Dataset]:
        ts = int(time.time())

        data_path = f"{self.volume_path}/{config['bucket_path_prefix']}"
        dataset_name = f"{config['name']}{'-{}'.format(ts) if local else '' }"
        logging.info(f"Data path: {data_path}, Dataset name: {dataset_name}")

        # patch fix: fix known bug in gcsfuse where you have to define a folder path before it is searchable in some cases.
        pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

        gt_annotations = {}
        for label_key, label_config in config.get("metadata_config").items():
            label_lookup = self._load_bq(
                query=label_config["query"],
                key=label_config["key"],
            )

            gt_annotations[label_key] = {
                f"{self.volume_path}/{k}": label_config["label_map"].get(
                    str(v[label_config["value"]]), ""
                )
                for k, v in label_lookup.items()
            }

        logging.debug(f"GT Annotations: {gt_annotations}")

        # Create samples for your data
        samples = []
        for filepath in [
            str(fp.absolute()) for fp in list(pathlib.Path(data_path).glob("**/*"))
        ]:
            sample = fo.Sample(filepath=filepath)

            for label_key, label_annotations in gt_annotations.items():
                # Store classification in a field name of your choice
                label = label_annotations.get(filepath, "")
                logging.debug(f"Label: {label}")
                sample[label_key] = fo.Classification(label=label)

            samples.append(sample)

        # Create dataset
        dataset = fo.Dataset(name=dataset_name, persistent=config["persistent"])
        dataset.add_samples(samples)

        return dataset
