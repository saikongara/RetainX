import logging
from datetime import datetime
import csv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Traceability:
    """
    Traceability class to maintain all the movements for data archival.
    """

    def __init__(self, csv_file_path="./resources/tracker.csv"):
        self.movements = []
        self.csv_file_path = csv_file_path
        self._initialize_csv()

    def _initialize_csv(self):
        """
        Initialize the CSV file with headers if it does not exist.
        """
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "service", "action", "file_path", "tier", "status", "error_message"])

    def log_movement(self, service, action, file_path, tier=None, status="success", error_message=None):
        """
        Log a movement action.

        :param service: The service used (Azure or AWS).
        :param action: The action performed (archive, restore, delete, move).
        :param file_path: The path of the file involved.
        :param tier: The storage tier (if applicable).
        :param status: The status of the action (success or failure).
        :param error_message: The error message (if any).
        """
        movement = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": service,
            "action": action,
            "file_path": file_path,
            "tier": tier,
            "status": status,
            "error_message": error_message
        }
        self.movements.append(movement)
        logger.info(f"Logged movement: {movement}")
        self._log_to_csv(movement)

    def _log_to_csv(self, movement):
        """
        Log the movement to a CSV file.

        :param movement: The movement dictionary to log.
        """
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(movement.values())

    def get_movements(self):
        """
        Get all logged movements.

        :return: List of all movements.
        """
        return self.movements
