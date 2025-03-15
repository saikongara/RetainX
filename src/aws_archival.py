import boto3
import logging
from datetime import datetime, timedelta
from utils.secrets import get_aws_secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSArchival:
    def __init__(self, bucket_name):
        secrets = get_aws_secrets()
        self.s3 = boto3.client('s3', aws_access_key_id=secrets['aws_access_key_id'], aws_secret_access_key=secrets['aws_secret_access_key'])
        self.bucket_name = bucket_name

    def move_to_archival(self, object_key, retention_period):
        try:
            # Determine the archival status based on retention period
            if retention_period <= 90:
                logger.info(f"Moving {object_key} to Real-Time storage.")
                # Logic to move to Real-Time storage
            elif retention_period <= 1460:  # 4 years
                logger.info(f"Moving {object_key} to Reference storage.")
                # Logic to move to Reference storage
            elif retention_period <= 3650:  # 10 years
                logger.info(f"Moving {object_key} to Archival storage.")
                # Logic to move to Archival storage
            else:
                logger.warning(f"{object_key} exceeds maximum retention period and will be deleted.")
                self.delete_object(object_key)

        except Exception as e:
            logger.error(f"Error moving {object_key}: {str(e)}")

    def delete_object(self, object_key):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info(f"Deleted {object_key} from {self.bucket_name}.")
        except Exception as e:
            logger.error(f"Error deleting {object_key}: {str(e)}")

    def list_objects(self):
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
        logger.info("Starting archival process.")
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    object_key = obj['Key']
                    last_modified = obj['LastModified']
                    retention_period = (datetime.now(last_modified.tzinfo) - last_modified).days
                    self.move_to_archival(object_key, retention_period)
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error during archival process: {str(e)}")

    def restore_data(self, data_type):
        logger.info("Starting restore process.")
        # Implement restore logic based on data_type
        pass

    def delete_data(self, data_type):
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
            else:
                logger.info("No objects found in the bucket.")
        except Exception as e:
            logger.error(f"Error during delete process: {str(e)}")