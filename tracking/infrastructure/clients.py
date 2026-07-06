import logging
import os
import requests

from dotenv import load_dotenv

from tracking.domain.entities import TelemetryRecord

# Load environment variables from .env file
load_dotenv()


class TelemetrySyncClient:
    """ A client for syncing telemetry data to a cloud API."""

    def __init__(self):
        """ Initialize the TelemetrySyncClient with the cloud API base URL and telemetry API URL from environment variables. """
        self.api_base_url = os.getenv('CLOUD_API_BASE_URL')
        self.telemetry_api_url = os.getenv('CLOUD_TELEMETRY_ULR')

    def sync(self, telemetry: TelemetryRecord) -> None:
        """ Sync telemetry data to the cloud API.

        :param telemetry: TelemetryRecord object containing the telemetry data to be synced.
        :exception ValueError: If the telemetry data is invalid.
        :exception requests.RequestException: If there is an error during the HTTP request.
        """

        payload = self._to_payload(telemetry)
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.telemetry_api_url, json=payload, headers=headers)
        except requests.RequestException as e:
            logging.error("Error syncing telemetry: %s", e)
            return

        if response.status_code == 200:
            logging.info("Telemetry synced successfully for device %s", telemetry.device_id)
            return

        logging.warning(
            "Failed to sync telemetry for device %s. Status code: %s, Response: %s",
            telemetry.device_id,
            response.status_code,
            response.text
        )

        return

    @staticmethod
    def _to_payload(telemetry: TelemetryRecord) -> dict:
        """Convert a TelemetryRecord to a payload for the telemetry API."""

        try:
            payload_physical_stock = float(telemetry.physical_stock)
            if payload_physical_stock < 0:
                raise ValueError("Physical stock must be a positive number")

            payload_temperature_in_celsius = float(telemetry.temperature_in_celsius)
            if payload_temperature_in_celsius < -273.15 or payload_temperature_in_celsius > 100:
                raise ValueError("Temperature must be a valid temperature in Celsius")

            payload_humidity_percentage = float(telemetry.humidity_percentage)
            if payload_humidity_percentage < 0 or payload_humidity_percentage > 100:
                raise ValueError("Humidity must be a valid percentage")

            payload_assigned_batch_id = str(telemetry.assigned_batch_id)

            payload_device_id = str(telemetry.device_id)

            payload_timestamp = telemetry.timestamp
            if not payload_timestamp:
                raise ValueError("Timestamp is required")

        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        payload = {
            "physicalStock": payload_physical_stock,
            "temperatureInCelsius": payload_temperature_in_celsius,
            "humidityPercentage": payload_humidity_percentage,
            "assignedBatchId": payload_assigned_batch_id,
            "deviceId": payload_device_id,
            "timestamp": payload_timestamp,
        }

        return payload