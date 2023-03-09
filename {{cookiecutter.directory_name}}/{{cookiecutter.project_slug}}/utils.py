import io
import json
import pickle
import random
from typing import Any, Dict

import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_seeds(seed=420):
    """Set seeds for reproducibility."""
    np.random.seed(seed)
    random.seed(seed)


def load_dict(filepath: str) -> Dict:
    """Read dictionary from filepath.

    Parameters
    ----------
    filepath : str
        location of file.

    Returns
    -------
    Dict
        loaded JSON data.
    """
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def load_dict_s3(bucket_name: str, bucket_path: str) -> Dict:
    """Read dictionary from s3 bucket.

    Parameters
    ----------
    bucket_name : str
        s3 bucket name.
    bucket_path : str
        filepath within bucket.

    Returns
    -------
    data : Dict
        loaded JSON data.
    """
    s3 = boto3.resource("s3")
    s3_obj = s3.Object(bucket_name, bucket_path)
    data = json.loads(s3_obj.get()["Body"].read().decode("UTF-8"))
    return data


def save_dict(obj: Dict, filepath: str, **kwargs):
    """Save dictionary file to filepath.

    Parameters
    ----------
    obj : Dict
        object to save.
    filepath : str
        location of file.
    """
    with open(filepath, "w") as file:
        json.dump(obj, file, **kwargs)


def save_dict_s3(obj: Dict, bucket_name: str, bucket_path: str, **kwargs):
    """Save dictionary file to s3 bucket filepath.

    Parameters
    ----------
    obj : Dict
        object to save.
    bucket_name : str
        s3 bucket name.
    bucket_path : str
        filepath within bucket.
    """
    s3 = boto3.resource("s3")
    s3object = s3.Object(bucket_name, bucket_path)
    s3object.put(Body=(bytes(json.dumps(obj, **kwargs).encode("UTF-8"))))


def save_pkl(obj: Any, filepath: str):
    """Write pickle to filepath.

    Parameters
    ----------
    obj : Any
        object to be saved.
    filepath : str
        location of file.
    """
    with open(filepath, "wb") as file:
        pickle.dump(obj, file, protocol=-1)


def save_pkl_s3(obj: Any, bucket_name: str, bucket_path: str):
    """Write pickle to s3 bucket filepath.

    Parameters
    ----------
    obj : Any
        object to be saved.
    bucket_name : str
        s3 bucket name.
    bucket_path : str
        filepath within bucket.
    """
    s3 = boto3.resource("s3")
    s3object = s3.Object(bucket_name, bucket_path)
    s3object.put(Body=pickle.dumps(obj, protocol=-1))


def load_pkl_s3(bucket_name: str, bucket_path: str) -> Any:
    """Load object from pickle dfile in s3.

    Parameters
    ----------
    bucket_name : str
        s3 bucket name.
    bucket_path : str
        filepath within bucket.

    Returns
    -------
    obj : Any
        loaded object.
    """
    s3 = boto3.resource("s3")
    obj = pickle.loads(
        s3.Bucket(bucket_name).Object(bucket_path).get()["Body"].read()
    )
    return obj


def load_pkl(filepath: str) -> Any:
    """Load object from pickle file.

    Parameters
    ----------
    filepath : str
        location of file.

    Returns
    -------
    obj : Any
        loaded object.
    """
    with open(filepath, "rb") as file:
        obj = pickle.load(file)
    return obj


def get_s3_uri(prefix, bucket) -> list:
    """Returns all objects within an s3 bucket and its prefix, *including
    inner folder structures.*

    Example
    -------
    Say your bucket has the following structure:
    ```
    .
    └── my-bucket/
        └── processed_day=1/
            ├── IdClient=1/
            │   ├── file1.parquet
            │   └── file2.parquet
            └── IdClient=2/
                ├── file3.parquet
                └── file4.parquet
    ```
    And we want to get files 1-4 without having to independently list elements
    of `IdClient=1` and `IdClient=2`, we just want to get all files knowing
    they're within `processed_day=1`. We could do so by the following code:

    ```python
    bucket = "my-bucket"
    prefix = "processed_day=1"
    s3_list = get_s3_uri(prefix, bucket)
    ```
    Then `s3_list` would look like this
    ```python
    >>> print(s3_list)
    ['s3://my-bucket/processed_day=1/IdClient=1/file1.parquet',
    's3://my-bucket/processed_day=1/IdClient=1/file2.parquet',
    's3://my-bucket/processed_day=1/IdClient=2/file3.parquet',
    's3://my-bucket/processed_day=1/IdClient=2/file4.parquet']
    ```

    Parameters
    ----------
    prefix : str
    bucket : str
        bucket name

    Returns
    -------
    s3_files : list
        list of returned s3 objects
    """
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    try:
        s3_files = [
            f"s3://{bucket}/{obj['Key']}"
            for page in pages
            for obj in page["Contents"]
            if obj["Key"].endswith(".parquet")
        ]
        return s3_files
    except Exception:
        return None


def df_to_s3(
    df: pd.core.frame.DataFrame,
    bucket_name: str,
    bucket_path: str,
    file_name: str,
) -> None:
    """Saves dataframe as a csv or parquet to an s3 bucket given the object,
    bucket_name, bucket_path and file_name.

    Parameters
    ----------
    df : pd.core.frame.DataFrame
    bucket_name : str
    bucket_path : str
    file_name : str
    """
    assert bucket_path.startswith("/") and bucket_path.endswith(
        "/"
    ), "Bucket path is not valid"
    s3_uri = "s3://" + bucket_name + bucket_path + file_name
    if file_name.endswith(".csv"):
        df.to_csv(s3_uri, index=None)
    elif file_name.endswith(".parquet"):
        df.to_parquet(s3_uri)


def save_png_s3(bucket_name: str, bucket_path: str):
    """Saves an image to an S3 bucket."""
    # Save tmp img to BytesIO
    img_data = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_data, format="png")
    img_data.seek(0)

    # Connect to sS
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    # Save png object
    bucket.put_object(Body=img_data, ContentType="image/png", Key=bucket_path)


class NumpyEncoder(json.JSONEncoder):
    """Encoder to save numpy floats in args json files."""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
