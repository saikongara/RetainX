# RetainX

RetainX is a tool for managing archival operations for both AWS and Azure.

## Overview
The RetainX Module is designed to manage data lifecycle policies for Azure Data Lake Storage (ADLS) and AWS S3. It automates the process of moving, retaining, or deleting data based on predefined policies, optimizing costs and storage utilization. The module categorizes data into three levels:

1. **Real-Time Data**: Retained for 90 days. This includes any data accessed in the last 90 days.
2. **Reference Data**: Retained for 4 years. This includes any data accessed in the last 4 years.
3. **Archival Data**: Retained for 10 years and then cleaned up. This includes any data accessed in the last 10 years.

## Features
- Archive files to AWS S3
- Archive files to Azure Blob Storage
- Restore archived files
- Delete archived files
- Automated lifecycle management for Azure ADLS and AWS S3.
- Efficient data categorization and retention policies.
- Clear logging and error handling for all operations.
- Command-line interface for easy interaction.
- Secure access to credentials using AWS Secrets Manager and Azure Key Vault.
- Detailed traceability for all operations.

## Installation
To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### CLI Commands

RetainX provides a CLI for managing archival operations.

#### Archive to AWS

To archive a file to AWS S3, use the following command:

```bash
python src/cli.py archive_to_aws <file_path> <object_name>
```

#### Archive to Azure Blob Storage

To archive a file to Azure Blob Storage, use the following command:

```bash
python src/cli.py archive_to_azure <file_path> <blob_name>
```

#### Archive to Azure Data Lake Storage

To archive data in Azure Data Lake Storage, use the following command:

```bash
python src/cli.py archive_to_adls <file_system_name> <data_type>
```

### Command-Line Interface
The module provides a CLI for users to interact with the archival functionalities. You can run the CLI with the following command:

```bash
python src/cli.py [options]
```

### Options
- `--azure`: Manage archival for Azure ADLS.
- `--aws`: Manage archival for AWS S3.
- `--file-system`: Specify the ADLS file system name (required for Azure).
- `--bucket`: Specify the S3 bucket name (required for AWS).
- `--data-type`: Specify the type of data to manage (`real_time`, `reference`, `archival`).
- `--help`: Show help message and options.

### Examples
1. **Archiving Real-Time Data in Azure ADLS**:
   ```bash
   python src/cli.py --azure --file-system your-file-system-name --data-type real_time
   ```

2. **Archiving Reference Data in AWS S3**:
   ```bash
   python src/cli.py --aws --bucket your-bucket-name --data-type reference
   ```

3. **Archiving a File to Azure Blob Storage**:
   ```bash
   python src/cli.py archive_to_azure <file_path> <blob_name>
   ```

### Configuration

RetainX uses AWS Secrets Manager and Azure Key Vault to manage secrets. Ensure that the necessary secrets are stored in the respective services.

## Logging and Traceability
The module includes logging utilities to track operations. Logs are generated for:
- Information messages
- Warnings
- Errors

Logs can be found in the specified log file as defined in the `logger.py` utility.

The module also includes traceability features to log the movement of data across different storage tiers and operations. This ensures a detailed audit trail for all actions performed.

## Error Handling
The module implements robust error handling to ensure that any issues encountered during the archival process are logged and reported appropriately.

## References
- [Azure Data Lake Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/index.html)
- [Azure Key Vault Documentation](https://docs.microsoft.com/en-us/azure/key-vault/)

## Contribution
Contributions to the module are welcome. Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.