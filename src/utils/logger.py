import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specified name and log file."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a file handler to log to a file
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    
    # Create a console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a logger for the archival module
log_file_path = os.path.join(os.path.dirname(__file__), 'storage_archival.log')
archival_logger = setup_logger('ArchivalModuleLogger', log_file_path)

def log_info(message):
    """Log an informational message."""
    archival_logger.info(message)

def log_warning(message):
    """Log a warning message."""
    archival_logger.warning(message)

def log_error(message):
    """Log an error message."""
    archival_logger.error(message)