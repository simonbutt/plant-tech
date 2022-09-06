from src.DataLoader import DataLoader
import os
import fiftyone as fo
import logging
from typing import Type
import yaml


def _set_log_level(log_env: str) -> None:
    # Using approved_log_levels to reduce risk of using an eval
    approved_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
    log_level = (
        "INFO" if (env_result := log_env) not in approved_log_levels else env_result
    )
    logging.basicConfig(level=eval(f"logging.{log_level}"))


def _get_dataset_config(path: str = ".") -> dict:
    with open(f"{path}/dataset-config.yml") as dataset_config_file:
        dataset_config = yaml.load(dataset_config_file, Loader=yaml.SafeLoader)
    logging.debug(f"Dataset config: {dataset_config}")
    return dataset_config


if __name__ == "__main__":

    # Get environment variable parameters
    data_path: str = os.environ.get("MNT_DIR")
    bucket_path_prefix: str = os.environ.get("BUCKET_PATH_PREFIX")
    is_demo: str = str(os.environ.get("IS_DEMO", "False"))
    log_level: str = os.environ.get("LOG_LEVEL")
    project_id: str = os.environ.get("PROJECT_ID")

    _set_log_level(log_level)

    # Log data directory size
    data_dir_size: int = len(os.listdir(f"{data_path}/{bucket_path_prefix}"))
    logging.info(f"Objects in data directory: {data_dir_size}")

    # Initiate DataLoader and create a FiftyOne set
    logging.info("Starting dataset load")
    dataset_config: dict = _get_dataset_config()

    DL: Type[DataLoader] = DataLoader(
        volume_path=data_path,
        project_id=project_id
    )
    dataset: fo.Dataset = (
        DL._demo_dataset()
        if is_demo.lower() == "true"
        else DL.load_dataset(config=dataset_config)
    )

    logging.info("Dataset created, starting fiftyone instance")
    # Start and maintain FiftyOne session
    # Port is hardcoded due to bug in fiftyone where changing the port breaks something internal
    session: fo.Session = fo.launch_app(dataset, remote=True, port=5151)
    session.wait()
