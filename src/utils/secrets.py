import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging
from utils.tracability import Traceability

class SecretsManager:
    """
    SecretsManager is responsible for retrieving secrets from AWS Secrets Manager and Azure Key Vault.
    """

    def __init__(self):
        self.traceability = Traceability()
        self.logger = logging.getLogger(__name__)

    def get_aws_secrets(self, secret_name, region_name):
        """
        Retrieve secrets from AWS Secrets Manager.

        :param secret_name: Name of the secret in AWS Secrets Manager.
        :param region_name: AWS region where the secret is stored.
        :return: Dictionary containing AWS secrets.
        """
        try:
            client = boto3.client('secretsmanager', region_name=region_name)
            response = client.get_secret_value(SecretId=secret_name)
            secret = eval(response['SecretString'])
            self.traceability.log_movement("AWS", "get_secrets", "path_placeholder")
            self.logger.info(f"Successfully retrieved AWS secrets for {secret_name}")
            return {
                "aws_access_key_id": secret.get("aws_access_key_id"),
                "aws_secret_access_key": secret.get("aws_secret_access_key"),
                "bucket_name": secret.get("bucket_name")
            }
        except Exception as e:
            self.traceability.log_movement("AWS", "get_secrets", "path_placeholder", status="failure", error_message=str(e))
            self.logger.error(f"Failed to retrieve AWS secrets for {secret_name}: {str(e)}")

    def get_azure_secrets(self, secret_name, key_vault_name):
        """
        Retrieve secrets from Azure Key Vault.

        :param secret_name: Name of the secret in Azure Key Vault.
        :param key_vault_name: Name of the Azure Key Vault.
        :return: Dictionary containing Azure secrets.
        """
        try:
            KVUri = f"https://{key_vault_name}.vault.azure.net"
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=KVUri, credential=credential)
            secret = client.get_secret(secret_name)
            self.traceability.log_movement("Azure", "get_secrets", "path_placeholder")
            self.logger.info(f"Successfully retrieved Azure secrets for {secret_name}")
            return {"connection_string": secret.value}
        except Exception as e:
            self.traceability.log_movement("Azure", "get_secrets", "path_placeholder", status="failure", error_message=str(e))
            self.logger.error(f"Failed to retrieve Azure secrets for {secret_name}: {str(e)}")
