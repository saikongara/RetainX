import boto3
import logging
from datetime import datetime, timedelta
from utils.secrets import SecretsManager
from utils.tracability import Traceability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSArchival:
    """
    AWSArchival is responsible for archiving files to AWS S3.
    """

    def __init__(self, secret_name, region_name):
        """
        Initialize AWSArchival with AWS credentials and bucket name.

        :param secret_name: Name of the secret in AWS Secrets Manager.
        :param region_name: AWS region name.
        """
        self.secrets_manager = SecretsManager()
        self.secrets = self.secrets_manager.get_aws_secrets(secret_name, region_name)
        self.aws_access_key_id = self.secrets["aws_access_key_id"]
        self.aws_secret_access_key = self.secrets["aws_secret_access_key"]
        self.bucket_name = self.secrets["bucket_name"]
        self.s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        self.traceability = Traceability()

    def move_to_archival(self, object_key, retention_period):
        """
        Move an object to the appropriate storage class based on its retention period.

        :param object_key: Key of the object in S3.
        :param retention_period: Retention period of the object in days.
        """
        try:
            if retention_period <= 90:
                logger.info(f"Moving {object_key} to Real-Time storage.")
                self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': object_key}, Key=object_key, StorageClass='STANDARD')
            elif retention_period <= 1460:  # 4 years
                logger.info(f"Moving {object_key} to Reference storage.")
                self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': object_key}, Key=object_key, StorageClass='STANDARD_IA')
            elif retention_period <= 3650:  # 10 years
                logger.info(f"Moving {object_key} to Archival storage.")
                self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': object_key}, Key=object_key, StorageClass='GLACIER')
            else:
                logger.warning(f"{object_key} exceeds maximum retention period and will be deleted.")
                self.delete_object(object_key)
            self.traceability.log_movement("AWS", "move", object_key, tier="archival")
        except Exception as e:
            logger.error(f"Error moving {object_key}: {str(e)}")
            self.traceability.log_movement("AWS", "move", object_key, tier="archival", status="failure", error_message=str(e))

    def delete_object(self, object_key):
        """
        Delete an object from the S3 bucket.

        :param object_key: Key of the object in S3.
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"Deleted {object_key} from {self.bucket_name}.")
            self.traceability.log_movement("AWS", "delete", object_key, tier="archival")
        except Exception as e:
            logger.error(f"Error deleting {object_key}: {str(e)}")
            self.traceability.log_movement("AWS", "delete", object_key, tier="archival", status="failure", error_message=str(e))

    def list_objects(self):
        """
        List all objects in the S3 bucket.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    logger.info(f"Found object: {obj['Key']} with last modified date: {obj['LastModified']}")
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error listing objects in {self.bucket_name}: {str(e)}")

    def archive_data(self, data_type):
        """
        Archive data based on its type.

        :param data_type: Type of data to be archived.
        """
        logger.info("Starting archival process.")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    object_key = obj['Key']
                    last_modified = obj['LastModified']
                    retention_period = (datetime.now(last_modified.tzinfo) - last_modified).days
                    self.move_to_archival(object_key, retention_period)
                    self.traceability.log_movement("AWS", "archive", object_key, tier=data_type)
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error during archival process: {str(e)}")
            self.traceability.log_movement("AWS", "archive", "path_placeholder", tier=data_type, status="failure", error_message=str(e))

    def restore_data(self, data_type):
        """
        Restore data based on its type.

        :param data_type: Type of data to be restored.
        """
        logger.info("Starting restore process.")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    object_key = obj['Key']
                    logger.info(f"Restoring object: {object_key}")
                    self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': object_key}, Key=object_key, StorageClass='STANDARD')
                    self.traceability.log_movement("AWS", "restore", object_key, tier=data_type)
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error restoring data: {str(e)}")
            self.traceability.log_movement("AWS", "restore", "path_placeholder", tier=data_type, status="failure", error_message=str(e))

    def delete_data(self, data_type):
        """
        Delete data based on its type.

        :param data_type: Type of data to be deleted.
        """
        logger.info("Starting delete process.")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    object_key = obj['Key']
                    last_modified = obj['LastModified']
                    retention_period = (datetime.now(last_modified.tzinfo) - last_modified).days
                    if data_type == 'real_time' and retention_period <= 90:
                        self.delete_object(object_key)
                    elif data_type == 'reference' and 90 < retention_period <= 1460:
                        self.delete_object(object_key)
                    elif data_type == 'archival' and 1460 < retention_period <= 3650:
                        self.delete_object(object_key)
                    logger.info(f"Deleted {object_key} from {self.bucket_name}.")
                    self.traceability.log_movement("AWS", "delete", object_key, tier=data_type)
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error during delete process: {str(e)}")
            self.traceability.log_movement("AWS", "delete", "path_placeholder", tier=data_type, status="failure", error_message=str(e))

    def upload_file(self, file_path, object_name):
        """
        Upload a file to AWS S3.

        :param file_path: Path to the file to be uploaded.
        :param object_name: Name of the object in S3.
        """
        try:
            self.s3.upload_file(file_path, self.bucket_name, object_name)
            logger.info(f"Uploaded file {file_path} to object {object_name}.")
            self.traceability.log_movement("AWS", "upload", file_path, tier="object")
        except Exception as e:
            logger.error(f"Error uploading file {file_path} to object {object_name}: {str(e)}")
            self.traceability.log_movement("AWS", "upload", file_path, tier="object", status="failure", error_message=str(e))