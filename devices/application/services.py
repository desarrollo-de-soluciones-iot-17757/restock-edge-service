from devices.domain.entities import DeviceThreshold
from devices.domain.services import DeviceThresholdService
from devices.infrastructure.repositories import DeviceThresholdRepository
from iam.infrastructure.repositories import DeviceRepository


class DeviceThresholdApplicationService:
    """
    Application service that orchestrates the registering of a device threshold use-case.

    Attributes:
        device_threshold_repository: (DeviceThresholdRepository) The device threshold repository.
        device_threshold_service: (DeviceThresholdService) The device threshold service.
    """

    def __init__(self):
        """ Initialize the device threshold application service. """
        self.device_threshold_repository = DeviceThresholdRepository()
        self.device_threshold_service = DeviceThresholdService()
        self.device_repository = DeviceRepository()

    def create_device_threshold(
        self,
        device_id: str,
        assigned_batch_id: str,
        custom_supply_unit_measurement: str | None,
        minimum_humidity_percentage: float,
        maximum_humidity_percentage: float,
        minimum_temperature_in_celsius: float,
        maximum_temperature_in_celsius: float,
        custom_supply_weight: float | None = 100.0,
        anomaly_threshold: float | None = None,
    ) -> DeviceThreshold:
        record = self.device_threshold_service.create_threshold_for_device(
            device_id=device_id,
            assigned_batch_id=assigned_batch_id,
            custom_supply_unit_measurement=custom_supply_unit_measurement,
            minimum_humidity_percentage=minimum_humidity_percentage,
            maximum_humidity_percentage=maximum_humidity_percentage,
            minimum_temperature_in_celsius=minimum_temperature_in_celsius,
            maximum_temperature_in_celsius=maximum_temperature_in_celsius,
            custom_supply_weight=custom_supply_weight,
            anomaly_threshold=anomaly_threshold,
        )

        return self.device_threshold_repository.save(record)

    def calibrate_custom_supply_weight(
            self,
            device_id: str,
            custom_supply_weight: float,
    ) -> DeviceThreshold:
        return self.device_threshold_repository.calibrate_custom_supply_weight(
            device_id,
            custom_supply_weight
        )

    def update_device_threshold(
            self,
            device_id: str,
            assigned_batch_id: str,
            custom_supply_unit_measurement: str | None,
            minimum_humidity_percentage: float,
            maximum_humidity_percentage: float,
            minimum_temperature_in_celsius: float,
            maximum_temperature_in_celsius: float,
            custom_supply_weight: float | None = None,
            anomaly_threshold: float | None = None,
    ) -> DeviceThreshold:
        try:
            record = self.device_threshold_repository.get_by_device_id(device_id)
            threshold_id = record.threshold_id
            if custom_supply_weight is None:
                custom_supply_weight = record.custom_supply_weight
            if anomaly_threshold is None:
                anomaly_threshold = getattr(record, "anomaly_threshold", None)
        except Exception:
            threshold_id = 0

        updated_threshold = self.device_threshold_service.create_threshold_for_device(
            threshold_id=threshold_id,
            device_id=device_id,
            assigned_batch_id=assigned_batch_id,
            custom_supply_weight=custom_supply_weight,
            custom_supply_unit_measurement=custom_supply_unit_measurement,
            minimum_humidity_percentage=minimum_humidity_percentage,
            maximum_humidity_percentage=maximum_humidity_percentage,
            minimum_temperature_in_celsius=minimum_temperature_in_celsius,
            maximum_temperature_in_celsius=maximum_temperature_in_celsius,
            anomaly_threshold=anomaly_threshold,
        )

        return self.device_threshold_repository.update(updated_threshold)
