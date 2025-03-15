import logging
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime, timedelta
from utils.secrets import get_azure_secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureArchival:
    def __init__(self, file_system_name):
        secrets = get_azure_secrets()
        self.service_client = DataLakeServiceClient.from_connection_string(secrets['connection_string'])
        self.file_system_name = file_system_name

    def archive_data(self, data_type):
        logger.info("Starting archival process.")
        paths = self.list_paths(self.file_system_name)
        for path in paths:
            file_client = self.service_client.get_file_system_client(self.file_system_name).get_file_client(path)
            properties = file_client.get_file_properties()
            last_modified = properties['last_modified']
            if data_type == 'real_time' and self.is_real_time_data(last_modified):
                self.move_to_storage_tier(file_client, "real-time")
            elif data_type == 'reference' and self.is_reference_data(last_modified):
                self.move_to_storage_tier(file_client, "reference")
            elif data_type == 'archival' and self.is_archival_data(last_modified):
                self.move_to_storage_tier(file_client, "archival")

    def restore_data(self, data_type):
        logger.info("Starting restore process.")
        # Implement restore logic based on data_type
        pass

    def delete_data(self, data_type):
        logger.info("Starting delete process.")
        paths = self.list_paths(self.file_system_name)
        for path in paths:
            file_client = self.service_client.get_file_system_client(self.file_system_name).get_file_client(path)
            properties = file_client.get_file_properties()
            last_modified = properties['last_modified']
            if data_type == 'real_time' and self.is_real_time_data(last_modified):
                file_client.delete_file()
                logger.info(f"Deleted {path} from {self.file_system_name}.")
            elif data_type == 'reference' and self.is_reference_data(last_modified):
                file_client.delete_file()
                logger.info(f"Deleted {path} from {self.file_system_name}.")
            elif data_type == 'archival' and self.is_archival_data(last_modified):
                file_client.delete_file()
                logger.info(f"Deleted {path} from {self.file_system_name}.")

    def list_paths(self, file_system_name):
        file_system_client = self.service_client.get_file_system_client(file_system_name)
        paths = [path.name for path in file_system_client.get_paths()]
        return paths

    def is_real_time_data(self, last_modified):
        return datetime.utcnow() - last_modified < timedelta(days=90)

    def is_reference_data(self, last_modified):
        return datetime.utcnow() - last_modified < timedelta(days=1460)  # 4 years

    def is_archival_data(self, last_modified):
        return datetime.utcnow() - last_modified < timedelta(days=3650)  # 10 years

    def move_to_storage_tier(self, file_client, tier):
        try:
            # Logic to move the file to the appropriate storage tier
            logger.info(f"Moving {file_client.path} to {tier} storage tier.")
            file_client.set_access_tier(tier)
        except Exception as e:
            logger.error(f"Error moving {file_client.path} to {tier} storage tier: {str(e)}")