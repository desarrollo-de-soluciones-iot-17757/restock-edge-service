from devices.domain.entities import DeviceThreshold


class DeviceThresholdService:
    """
    Domain service responsible for the creation of valid device threshold entities.
    """

    @classmethod
    def create_threshold_for_device(cls,
                         device_id: str,
                         assigned_batch_id: str,
                         custom_supply_unit_measurement: str,
                         minimum_humidity_percentage: float,
                         maximum_humidity_percentage: float,
                         minimum_temperature_in_celsius: float,
                         maximum_temperature_in_celsius: float,
                         ) -> DeviceThreshold:
        """
        Method to create a DeviceThreshold entity with validated data.

        :param device_id: The device id of the device
        :param assigned_batch_id: The assigned batch id of the device
        :param custom_supply_unit_measurement: The unit measurement of the device
        :param minimum_humidity_percentage: The minimum humidity percentage of the device
        :param maximum_humidity_percentage: The maximum humidity percentage of the device
        :param minimum_temperature_in_celsius: The minimum temperature in Celsius
        :param maximum_temperature_in_celsius: The maximum temperature in Celsius

        :return: A DeviceThreshold entity
        """
        try:
            parsed_custom_supply_unit_measurement = str(custom_supply_unit_measurement)
            parsed_assigned_batch_id = str(assigned_batch_id)
            parsed_minimum_humidity_percentage = float(minimum_humidity_percentage)
            parsed_maximum_humidity_percentage = float(maximum_humidity_percentage)
            parsed_minimum_temperature_in_celsius = float(minimum_temperature_in_celsius)
            parsed_maximum_temperature_in_celsius = float(maximum_temperature_in_celsius)

            if parsed_minimum_humidity_percentage >= parsed_maximum_humidity_percentage:
                raise ValueError("Minimum humidity percentage must be less than maximum humidity percentage")
            if parsed_minimum_humidity_percentage < 0:
                raise ValueError("Minimum humidity percentage must be greater than or equal to 0")
            if parsed_maximum_humidity_percentage > 100:
                raise ValueError("Maximum humidity percentage must be less than or equal to 100")

            if parsed_minimum_temperature_in_celsius >= parsed_maximum_temperature_in_celsius:
                raise ValueError("Minimum temperature must be less than maximum temperature")
            if parsed_minimum_temperature_in_celsius < -273.15:
                raise ValueError("Minimum temperature must be greater than or equal to -273.15")
            if parsed_maximum_temperature_in_celsius > 100:
                raise ValueError("Maximum temperature must be less than or equal to 100")

        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        return DeviceThreshold(
            device_id=device_id,
            assigned_batch_id=parsed_assigned_batch_id,
            custom_supply_weight=1.0,
            custom_supply_unit_measurement=parsed_custom_supply_unit_measurement,
            minimum_humidity_percentage=parsed_minimum_humidity_percentage,
            maximum_humidity_percentage=parsed_maximum_humidity_percentage,
            minimum_temperature_in_celsius=parsed_minimum_temperature_in_celsius,
            maximum_temperature_in_celsius=parsed_maximum_temperature_in_celsius,
        )

    @classmethod
    def calibrate_custom_supply_weight(cls,
                                       device_threshold: DeviceThreshold,
                                       custom_supply_weight: float,
                                       ) -> DeviceThreshold:
        """
        Assign the custom supply weight to the device threshold.

        :param device_threshold: The device threshold to be updated
        :param custom_supply_weight: The custom supply weight to be assigned to the device threshold
        :return: The updated device threshold with the assigned custom supply weight
        """

        try:
            parsed_custom_supply_weight = float(custom_supply_weight)
            if parsed_custom_supply_weight <= 0:
                raise ValueError("Invalid custom supply weight value")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format for custom supply weight")

        device_threshold.custom_supply_weight = parsed_custom_supply_weight
        return device_threshold