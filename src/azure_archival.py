import logging
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime, timedelta
from utils.secrets import SecretsManager
import os
from azure.storage.blob import BlobServiceClient
from utils.traceability import Traceability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureArchival:
    """
    AzureArchival is responsible for archiving files to Azure Blob Storage.
    """

    def __init__(self, secret_name, key_vault_name):
        """
        Initialize AzureArchival with secret name and key vault name.

        :param secret_name: Name of the secret in Azure Key Vault.
        :param key_vault_name: Name of the Azure Key Vault.
        """
        self.secrets_manager = SecretsManager()
        self.secrets = self.secrets_manager.get_azure_secrets(secret_name, key_vault_name)
        self.connection_string = self.secrets["connection_string"]
        self.service_client = DataLakeServiceClient.from_connection_string(self.connection_string)
        self.file_system_name = file_system_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self.traceability = Traceability()

    def archive_data(self, data_type):
        """
        Archive data based on the data type.

        :param data_type: Type of data to be archived (real_time, reference, archival).
        """
        logger.info("Starting archival process.")
        paths = self.list_paths(self.file_system_name)
        for path in paths:
            file_client = self.service_client.get_file_system_client(self.file_system_name).get_file_client(path)
            properties = file_client.get_file_properties()
            last_modified = properties['last_modified']
            try:
                if data_type == 'real_time' and self.is_real_time_data(last_modified):
                    self.move_to_storage_tier(file_client, "real-time")
                elif data_type == 'reference' and self.is_reference_data(last_modified):
                    self.move_to_storage_tier(file_client, "reference")
                elif data_type == 'archival' and self.is_archival_data(last_modified):
                    self.move_to_storage_tier(file_client, "archival")
                self.traceability.log_movement("Azure", "archive", path, tier=data_type)
            except Exception as e:
                logger.error(f"Error archiving {path}: {str(e)}")
                self.traceability.log_movement("Azure", "archive", path, tier=data_type, status="failure", error_message=str(e))

    def restore_data(self, data_type):
        """
        Restore data based on the data type.

        :param data_type: Type of data to be restored (real_time, reference, archival).
        """
        logger.info("Starting restore process.")
        try:
            # Implement restore logic based on data_type
            logger.info(f"Restoring data of type {data_type}.")
            self.traceability.log_movement("Azure", "restore", "path_placeholder", tier=data_type)
        except Exception as e:
            logger.error(f"Error restoring data: {str(e)}")
            self.traceability.log_movement("Azure", "restore", "path_placeholder", tier=data_type, status="failure", error_message=str(e))

    def delete_data(self, data_type):
        """
        Delete data based on the data type.

        :param data_type: Type of data to be deleted (real_time, reference, archival).
        """
        logger.info("Starting delete process.")
        paths = self.list_paths(self.file_system_name)
        for path in paths:
            file_client = self.service_client.get_file_system_client(self.file_system_name).get_file_client(path)
            properties = file_client.get_file_properties()
            last_modified = properties['last_modified']
            try:
                if data_type == 'real_time' and self.is_real_time_data(last_modified):
                    file_client.delete_file()
                elif data_type == 'reference' and self.is_reference_data(last_modified):
                    file_client.delete_file()
                elif data_type == 'archival' and self.is_archival_data(last_modified):
                    file_client.delete_file()
                logger.info(f"Deleted {path} from {self.file_system_name}.")
                self.traceability.log_movement("Azure", "delete", path, tier=data_type)
            except Exception as e:
                logger.error(f"Error deleting {path}: {str(e)}")
                self.traceability.log_movement("Azure", "delete", path, tier=data_type, status="failure", error_message=str(e))

    def list_paths(self, file_system_name):
        """
        List all paths in the file system.

        :param file_system_name: Name of the file system.
        :return: List of paths in the file system.
        """
        file_system_client = self.service_client.get_file_system_client(file_system_name)
        paths = [path.name for path in file_system_client.get_paths()]
        return paths

    def is_real_time_data(self, last_modified):
        """
        Check if the data is real-time data.

        :param last_modified: Last modified date of the data.
        :return: True if the data is real-time data, False otherwise.
        """
        return datetime.utcnow() - last_modified < timedelta(days=90)

    def is_reference_data(self, last_modified):
        """
        Check if the data is reference data.

        :param last_modified: Last modified date of the data.
        :return: True if the data is reference data, False otherwise.
        """
        return datetime.utcnow() - last_modified < timedelta(days=1460)  # 4 years

    def is_archival_data(self, last_modified):
        """
        Check if the data is archival data.

        :param last_modified: Last modified date of the data.
        :return: True if the data is archival data, False otherwise.
        """
        return datetime.utcnow() - last_modified < timedelta(days=3650)  # 10 years

    def move_to_storage_tier(self, file_client, tier):
        """
        Move the file to the appropriate storage tier.

        :param file_client: File client for the file to be moved.
        :param tier: Storage tier to move the file to.
        """
        try:
            # Logic to move the file to the appropriate storage tier
            logger.info(f"Moving {file_client.path} to {tier} storage tier.")
            file_client.set_access_tier(tier)
            self.traceability.log_movement("Azure", "move", file_client.path, tier=tier)
        except Exception as e:
            logger.error(f"Error moving {file_client.path} to {tier} storage tier: {str(e)}")
            self.traceability.log_movement("Azure", "move", file_client.path, tier=tier, status="failure", error_message=str(e))

    def upload_file(self, file_path, blob_name):
        """
        Upload a file to Azure Blob Storage.

        :param file_path: Path to the file to be uploaded.
        :param blob_name: Name of the blob in Azure Blob Storage.
        """
        try:
            with open(file_path, "rb") as data:
                self.container_client.upload_blob(name=blob_name, data=data)
            logger.info(f"Uploaded file {file_path} to blob {blob_name}.")
            self.traceability.log_movement("Azure", "upload", file_path, tier="blob")
        except Exception as e:
            logger.error(f"Error uploading file {file_path} to blob {blob_name}: {str(e)}")
            self.traceability.log_movement("Azure", "upload", file_path, tier="blob", status="failure", error_message=str(e))