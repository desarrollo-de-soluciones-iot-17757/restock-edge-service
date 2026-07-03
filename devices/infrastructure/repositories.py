from devices.domain.entities import DeviceThreshold
from devices.infrastructure.models import DeviceThresholdModel


class DeviceThresholdRepository:
    """
    Repository for DeviceThreshold entities.
    This repository is responsible for storing DeviceThreshold entities.
    """

    @staticmethod
    def save(device_threshold: DeviceThreshold) -> DeviceThreshold:
        """
        Persists a DeviceThreshold entity to the database. Performs upsert if record exists.
        """
        existing = DeviceThresholdModel.select().where(DeviceThresholdModel.device_id == device_threshold.device_id).first()
        if existing:
            return DeviceThresholdRepository.update(device_threshold)

        anomaly_thresh = getattr(device_threshold, "anomaly_threshold", None)
        record = DeviceThresholdModel.create(
            device_id = device_threshold.device_id,
            assigned_batch_id = device_threshold.assigned_batch_id,
            custom_supply_weight = device_threshold.custom_supply_weight,
            custom_supply_unit_measurement = device_threshold.custom_supply_unit_measurement,
            minimum_humidity_percentage = device_threshold.minimum_humidity_percentage,
            maximum_humidity_percentage = device_threshold.maximum_humidity_percentage,
            minimum_temperature_in_celsius = device_threshold.minimum_temperature_in_celsius,
            maximum_temperature_in_celsius = device_threshold.maximum_temperature_in_celsius,
            anomaly_threshold = anomaly_thresh,
        )

        return DeviceThreshold(
            threshold_id = record.threshold_id,
            device_id = record.device_id,
            assigned_batch_id = record.assigned_batch_id,
            custom_supply_weight = record.custom_supply_weight,
            custom_supply_unit_measurement = record.custom_supply_unit_measurement,
            minimum_humidity_percentage = record.minimum_humidity_percentage,
            maximum_humidity_percentage = record.maximum_humidity_percentage,
            minimum_temperature_in_celsius = record.minimum_temperature_in_celsius,
            maximum_temperature_in_celsius = record.maximum_temperature_in_celsius,
            anomaly_threshold = getattr(record, "anomaly_threshold", None),
        )

    @staticmethod
    def update(device_threshold: DeviceThreshold) -> DeviceThreshold:
        """
        Updates a DeviceThreshold entity in the database.
        """
        anomaly_thresh = getattr(device_threshold, "anomaly_threshold", None)
        update_data = {
            "assigned_batch_id": device_threshold.assigned_batch_id,
            "custom_supply_weight": device_threshold.custom_supply_weight,
            "custom_supply_unit_measurement": device_threshold.custom_supply_unit_measurement,
            "minimum_humidity_percentage": device_threshold.minimum_humidity_percentage,
            "maximum_humidity_percentage": device_threshold.maximum_humidity_percentage,
            "minimum_temperature_in_celsius": device_threshold.minimum_temperature_in_celsius,
            "maximum_temperature_in_celsius": device_threshold.maximum_temperature_in_celsius,
        }
        if anomaly_thresh is not None:
            update_data["anomaly_threshold"] = anomaly_thresh

        DeviceThresholdModel.update(update_data).where(DeviceThresholdModel.device_id == device_threshold.device_id).execute()
        record = DeviceThresholdModel.get(device_id=device_threshold.device_id)

        return DeviceThreshold(
            threshold_id = record.threshold_id,
            device_id = record.device_id,
            assigned_batch_id = record.assigned_batch_id,
            custom_supply_weight = record.custom_supply_weight,
            custom_supply_unit_measurement = record.custom_supply_unit_measurement,
            minimum_humidity_percentage = record.minimum_humidity_percentage,
            maximum_humidity_percentage = record.maximum_humidity_percentage,
            minimum_temperature_in_celsius = record.minimum_temperature_in_celsius,
            maximum_temperature_in_celsius = record.maximum_temperature_in_celsius,
            anomaly_threshold = getattr(record, "anomaly_threshold", None),
        )

    @staticmethod
    def calibrate_custom_supply_weight(device_id: str, custom_supply_weight: float) -> DeviceThreshold:
        """
        Updates the custom_supply_weight of a DeviceThreshold entity in the database.
        """
        DeviceThresholdModel.update(
            custom_supply_weight = custom_supply_weight,
        ).where(DeviceThresholdModel.device_id == device_id).execute()

        record = DeviceThresholdModel.get(device_id=device_id)

        return DeviceThreshold(
            threshold_id = record.threshold_id,
            device_id = record.device_id,
            assigned_batch_id = record.assigned_batch_id,
            custom_supply_weight = record.custom_supply_weight,
            custom_supply_unit_measurement = record.custom_supply_unit_measurement,
            minimum_humidity_percentage = record.minimum_humidity_percentage,
            maximum_humidity_percentage = record.maximum_humidity_percentage,
            minimum_temperature_in_celsius = record.minimum_temperature_in_celsius,
            maximum_temperature_in_celsius = record.maximum_temperature_in_celsius,
            anomaly_threshold = getattr(record, "anomaly_threshold", None),
        )

    @staticmethod
    def get_by_device_id(device_id: str) -> DeviceThreshold:
        """
        Retrieves a DeviceThreshold entity from the database by device_id.
        """
        record = DeviceThresholdModel.get(device_id=device_id)

        return DeviceThreshold(
            threshold_id = record.threshold_id,
            device_id = record.device_id,
            assigned_batch_id = record.assigned_batch_id,
            custom_supply_weight = record.custom_supply_weight,
            custom_supply_unit_measurement = record.custom_supply_unit_measurement,
            minimum_humidity_percentage = record.minimum_humidity_percentage,
            maximum_humidity_percentage = record.maximum_humidity_percentage,
            minimum_temperature_in_celsius = record.minimum_temperature_in_celsius,
            maximum_temperature_in_celsius = record.maximum_temperature_in_celsius,
            anomaly_threshold = getattr(record, "anomaly_threshold", None),
        )
