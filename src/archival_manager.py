import logging
from azure_archival import AzureArchival
from aws_archival import AWSArchival
from utils.secrets import SecretsManager
from utils.tracability import Traceability

class ArchivalManager:
    """
    ArchivalManager is responsible for managing archival operations for both AWS and Azure.
    """

    def __init__(self, aws_secret_name, aws_region_name, azure_secret_name, azure_key_vault_name):
        """
        Initialize ArchivalManager with AWS and Azure configurations.

        :param aws_secret_name: Name of the AWS secret.
        :param aws_region_name: Name of the AWS region.
        :param azure_secret_name: Name of the Azure secret.
        :param azure_key_vault_name: Name of the Azure key vault.
        """
        self.secrets_manager = SecretsManager()
        self.aws_secrets = self.secrets_manager.get_aws_secrets(aws_secret_name, aws_region_name)
        self.azure_secrets = self.secrets_manager.get_azure_secrets(azure_secret_name, azure_key_vault_name)
        self.cloud_provider = None
        self.traceability = Traceability()
        self.logger = logging.getLogger(__name__)
        if 'azure' in self.azure_secrets:
            self.cloud_provider = 'azure'
            self.archival = AzureArchival()
        elif 'aws' in self.aws_secrets:
            self.cloud_provider = 'aws'
            self.archival = AWSArchival()

    def perform_action(self, action, data_type):
        """
        Perform the specified action on the data.

        :param action: The action to be performed (archive, restore, delete).
        :param data_type: The type of data to be processed.
        """
        try:
            self.logger.info(f"Performing {action} on {data_type} for {self.cloud_provider}")
            if action == 'archive':
                self.archival.archive_data(data_type)
            elif action == 'restore':
                self.archival.restore_data(data_type)
            elif action == 'delete':
                self.archival.delete_data(data_type)
            self.traceability.log_movement(self.cloud_provider, action, "path_placeholder", tier=data_type)
            self.logger.info(f"Successfully performed {action} on {data_type} for {self.cloud_provider}")
        except Exception as e:
            self.logger.error(f"Failed to perform {action} on {data_type} for {self.cloud_provider}: {str(e)}")
            self.traceability.log_movement(self.cloud_provider, action, "path_placeholder", tier=data_type, status="failure", error_message=str(e))
