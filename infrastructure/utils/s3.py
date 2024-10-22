import logging
from typing import Tuple

import boto3
from botocore.exceptions import ClientError

from config import settings


def upload_file(file_name: str, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    config = settings.aws_config
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, config.bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        raise e
    return object_name


def download_file(file_name: str) -> Tuple[str, str]:
    config = settings.aws_config
    s3_client = boto3.client('s3')
    file_path = "./resources/reports/"
    s3_client.download_file(config.bucket_name, file_name, f"{file_path}{file_name}")
    return file_path, file_name
