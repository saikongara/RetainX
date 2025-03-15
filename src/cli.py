import argparse
from azure_archival import AzureArchival
from aws_archival import AWSArchival

def main():
    parser = argparse.ArgumentParser(description='Data Archival Script')
    parser.add_argument('--azure', action='store_true', help='Manage archival for Azure ADLS')
    parser.add_argument('--aws', action='store_true', help='Manage archival for AWS S3')
    parser.add_argument('--file-system', help='ADLS file system name (required for Azure)')
    parser.add_argument('--bucket', help='S3 bucket name (required for AWS)')
    parser.add_argument('--data-type', choices=['real_time', 'reference', 'archival'], required=True, help='Type of data to manage')
    args = parser.parse_args()

    if args.azure:
        if not args.file_system:
            parser.error('--file-system is required for Azure ADLS')
        archival = AzureArchival(file_system_name=args.file_system)
        if args.data_type == 'real_time':
            archival.archive_data('real_time')
        elif args.data_type == 'reference':
            archival.archive_data('reference')
        elif args.data_type == 'archival':
            archival.archive_data('archival')
    elif args.aws:
        if not args.bucket:
            parser.error('--bucket is required for AWS S3')
        archival = AWSArchival(bucket_name=args.bucket)
        if args.data_type == 'real_time':
            archival.archive_data('real_time')
        elif args.data_type == 'reference':
            archival.archive_data('reference')
        elif args.data_type == 'archival':
            archival.archive_data('archival')
    else:
        parser.error('Either --azure or --aws must be specified')

if __name__ == "__main__":
    main()