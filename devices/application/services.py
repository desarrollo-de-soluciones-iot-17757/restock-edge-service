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
        assigned_batch_id: str,
        custom_supply_unit_measurement: str,
        minimum_humidity_percentage: float,
        maximum_humidity_percentage: float,
        minimum_temperature_in_celsius: float,
        maximum_temperature_in_celsius: float,
    ) -> DeviceThreshold:
        """
        Create a new device threshold record.
        For the initial configuration, the custom supply weight won't be needed.
        It will be registered after, when the calibration process is done.

        :param device_id: The id of the device.
        :param assigned_batch_id: The id of the assigned batch.
        :param custom_supply_unit_measurement: The supply unit measurement.
        :param minimum_humidity_percentage: The minimum humidity percentage.
        :param maximum_humidity_percentage: The maximum humidity percentage.
        :param minimum_temperature_in_celsius: The minimum temperature in Celsius.
        :param maximum_temperature_in_celsius: The maximum temperature in Celsius.

        :return: The new device threshold record.
        """

        record = self.device_threshold_service.create_threshold_for_device(
            device_id,
            assigned_batch_id,
            custom_supply_unit_measurement,
            minimum_humidity_percentage,
            maximum_humidity_percentage,
            minimum_temperature_in_celsius,
            maximum_temperature_in_celsius,
        )

        return self.device_threshold_repository.save(record)

    def calibrate_custom_supply_weight(
            self,
            device_id: str,
            custom_supply_weight: float,
    ) -> DeviceThreshold:
        """
        Calibrate the custom supply weight of a device.

        :param device_id: The id of the device.
        :param custom_supply_weight: The custom supply weight.
        :return: The updated device threshold record.
        """

        device_threshold = self.device_threshold_repository.get(device_id)
        calibrated_device = (self.device_threshold_service
                             .calibrate_custom_supply_weight(device_threshold, custom_supply_weight))

        return self.device_threshold_repository.update(calibrated_device)

    def update_device_threshold(
            self,
            device_id: str,
            assigned_batch_id: str,
            custom_supply_unit_measurement: str,
            minimum_humidity_percentage: float,
            maximum_humidity_percentage: float,
            minimum_temperature_in_celsius: float,
            maximum_temperature_in_celsius: float,
    ) -> DeviceThreshold:
        """
        Update a device threshold record.
        It can be used to update the device threshold record or to assign a new batch to the device.

        :param device_id: The id of the device.
        :param assigned_batch_id: The id of the assigned batch.
        :param custom_supply_unit_measurement: The supply unit measurement.
        :param minimum_humidity_percentage: The minimum humidity percentage.
        :param maximum_humidity_percentage: The maximum humidity percentage.
        :param minimum_temperature_in_celsius: The minimum temperature in Celsius.
        :param maximum_temperature_in_celsius: The maximum temperature in Celsius.

        :return: The updated device threshold record.
        """

        updated_threshold = self.device_threshold_service.create_threshold_for_device(
            device_id,
            assigned_batch_id,
            custom_supply_unit_measurement,
            minimum_humidity_percentage,
            maximum_humidity_percentage,
            minimum_temperature_in_celsius,
            maximum_temperature_in_celsius,
        )

        return self.device_threshold_repository.update(updated_threshold)
