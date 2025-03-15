import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_aws_secrets():
    client = boto3.client('secretsmanager')
    secret_name = "your-secret-name"
    response = client.get_secret_value(SecretId=secret_name)
    return eval(response['SecretString'])

def get_azure_secrets():
    key_vault_name = "your-key-vault-name"
    KVUri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    secret = client.get_secret("your-secret-name")
    return {"connection_string": secret.value}
