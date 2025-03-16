import click
import logging
from src.archival_manager import ArchivalManager
from src.utils.secrets import SecretsManager
from utils.tracability import Traceability

class CLI:
    def __init__(self):
        self.traceability = Traceability()

    def run(self):
        try:
            cli()
            self.traceability.log_movement("CLI", "run", "path_placeholder")
        except Exception as e:
            self.traceability.log_movement("CLI", "run", "path_placeholder", status="failure", error_message=str(e))

@click.group()
def cli():
    """
    CLI group to hold archival commands.
    """
    pass

@click.command()
@click.argument('file_path')
@click.argument('object_name')
def archive_to_aws(file_path, object_name):
    """
    Command to archive a file to AWS S3.

    :param file_path: Path to the file to be archived.
    :param object_name: Name of the object in S3.
    """
    secrets_manager = SecretsManager()
    aws_secrets = secrets_manager.get_aws_secrets('my_aws_secret', 'us-west-2')
    archival_manager = ArchivalManager(aws_config=aws_secrets, azure_config={})
    archival_manager.archive_to_aws(file_path, object_name)

@click.command()
@click.argument('file_path')
@click.argument('blob_name')
def archive_to_azure(file_path, blob_name):
    """
    Command to archive a file to Azure Blob Storage.

    :param file_path: Path to the file to be archived.
    :param blob_name: Name of the blob in Azure Blob Storage.
    """
    secrets_manager = SecretsManager()
    azure_secrets = secrets_manager.get_azure_secrets('my_azure_secret', 'my_key_vault')
    archival_manager = ArchivalManager(aws_config={}, azure_config=azure_secrets)
    archival_manager.archive_to_azure(file_path, blob_name)

@click.command()
@click.argument('data_type')
def auto_archive(data_type):
    """
    Command to auto archive all qualifying blobs or buckets.

    :param data_type: Type of data to be archived (real_time, reference, archival).
    """
    secrets_manager = SecretsManager()
    aws_secrets = secrets_manager.get_aws_secrets('my_aws_secret', 'us-west-2')
    azure_secrets = secrets_manager.get_azure_secrets('my_azure_secret', 'my_key_vault')
    archival_manager = ArchivalManager(aws_config=aws_secrets, azure_config=azure_secrets)
    archival_manager.perform_action('archive', data_type)

cli.add_command(archive_to_aws)
cli.add_command(archive_to_azure)
cli.add_command(auto_archive)

if __name__ == '__main__':
    cli_instance = CLI()
    cli_instance.run()