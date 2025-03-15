from azure_archival import AzureArchival
from aws_archival import AWSArchival

class ArchivalManager:
    def __init__(self, cloud_provider):
        self.cloud_provider = cloud_provider
        if cloud_provider == 'azure':
            self.archival = AzureArchival()
        elif cloud_provider == 'aws':
            self.archival = AWSArchival()

    def perform_action(self, action, data_type):
        if action == 'archive':
            self.archival.archive_data(data_type)
        elif action == 'restore':
            self.archival.restore_data(data_type)
        elif action == 'delete':
            self.archival.delete_data(data_type)
