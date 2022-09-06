import fiftyone as fo
import logging
import os
from typing import Type
import pathlib


class DataLoader:
    def __init__(self, volume_path: str, bucket_path_prefix: str) -> None:
        self.volume_path = volume_path
        self.bucket_path_prefix = bucket_path_prefix
        # Objective: fix known bug in gcsfuse 
        pathlib.Path(data_path := f"{self.volume_path}/{bucket_path_prefix}").mkdir(parents=True, exist_ok=True)
        logging.info(f"Data path: {data_path}")

    def load_data(self, demo: bool = True) -> Type[fo.Dataset]:
        """
        Env variables:
            - PROJECT_ID
            - BUCKET_NAME
        """

        # Stub
        if demo:
            import fiftyone.zoo as foz

            return foz.load_zoo_dataset("quickstart")
        else:
            return fo.Dataset.from_dir(
                dataset_dir=f"{self.volume_path}/${self.bucket_path_prefix}",
                dataset_type=fo.types.ImageDirectory,
                name="plants-raw"
            )


if __name__ == "__main__":

    # Using approved_log_levels to reduce risk of using an eval
    approved_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    log_level = (
        "INFO"
        if (env_result := os.environ.get("LOG_LEVEL")) not in approved_log_levels
        else env_result
    )
    logging.basicConfig(level=eval(f"logging.{log_level}"))

    # Get environment variable parameters
    data_path: str = os.environ.get("MNT_DIR")
    bucket_path_prefix: str = os.environ.get("BUCKET_PATH_PREFIX")
    is_demo: bool = bool(os.environ.get("IS_DEMO", False))


    logging.info(f"Objects in mount directory: {len(os.listdir(data_path + '/hist_load'))}")
    # Initiate DataLoader and create a FiftyOne set
    DL = DataLoader(volume_path=data_path, bucket_path_prefix=bucket_path_prefix)
    dataset = DL.load_data(demo=is_demo)

    # Start and maintain FiftyOne session
    session = fo.launch_app(dataset, remote=True, port=5151)
    session.wait()
