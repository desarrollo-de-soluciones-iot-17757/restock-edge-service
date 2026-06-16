from devices.domain.entities import DeviceThreshold
from devices.domain.services import DeviceThresholdService
from devices.infrastructure.repositories import DeviceThresholdRepository


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

    def create_device_threshold(
        self,
        device_id: str,
        custom_supply_weight: float,
        custom_supply_unit_measurement: str,
        minimum_humidity_percentage: float,
        maximum_humidity_percentage: float,
        minimum_temperature_in_celsius: float,
        maximum_temperature_in_celsius: float,
    ) -> DeviceThreshold:
        """
        Create a new device threshold record.

        :param device_id: The id of the device.
        :param custom_supply_weight: The supply weight.
        :param custom_supply_unit_measurement: The supply unit measurement.
        :param minimum_humidity_percentage: The minimum humidity percentage.
        :param maximum_humidity_percentage: The maximum humidity percentage.
        :param minimum_temperature_in_celsius: The minimum temperature in Celsius.
        :param maximum_temperature_in_celsius: The maximum temperature in Celsius.

        :return: The new device threshold record.
        """

        record = self.device_threshold_service.create_threshold_for_device(
            device_id,
            custom_supply_weight,
            custom_supply_unit_measurement,
            minimum_humidity_percentage,
            maximum_humidity_percentage,
            minimum_temperature_in_celsius,
            maximum_temperature_in_celsius,
        )

        return self.device_threshold_repository.save(record)