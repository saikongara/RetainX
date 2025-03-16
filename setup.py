from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='retainx',
    version='0.1.0',
    author='Kongara, Sai',
    author_email='sai.kongara@gmail.com',
    description='A module for managing storage archival in Azure ADLS and AWS EC2 with lifecycle management.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/saikongara/retainx',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'azure-storage-blob',  # Azure SDK for Blob Storage
        'boto3',               # AWS SDK for Python
        'click',               # For CLI
    ],
    entry_points={
        'console_scripts': [
            'retainx=src.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)