"""Application services for the Tracking bounded context.

Application services sit between the interface layer and the domain layer. They
orchestrate use-cases by coordinating domain services, domain entities and
repositories without containing domain logic themselves.
"""
from devices.domain.entities import DeviceThreshold
from devices.infrastructure.repositories import DeviceThresholdRepository
from tracking.domain.entities import WeightRecord
from tracking.domain.entities import EnvironmentRecord
from tracking.domain.services import WeightRecordService
from tracking.domain.services import EnvironmentRecordService
from tracking.infrastructure.repositories import WeightRecordRepository
from tracking.infrastructure.repositories import EnvironmentRecordRepository
from iam.infrastructure.repositories import DeviceRepository


class WeightRecordApplicationService:
    """Application service that orchestrates the creation of a weight record use-case.

    Responsibilities:

    1. Cross-context validation – delegates to the IAM
       :class:`~iam.infrastructure.repositories.DeviceRepository` to verify
       that the requesting device is registered and the supplied API key is
       valid.
    2. Domain logic – delegates to
       :class:`~tracking.domain.services.WeightRecordService` to validate raw
       sensor values and construct a
       :class:`~tracking.domain.entities.WeightRecord` entity.
    3. Persistence – delegates to
       :class:`~tracking.infrastructure.repositories.WeightRecordRepository` to
       persist the entity and return the saved aggregate with its assigned
       identity.
    """

    def __init__(self):
        """Initialize the service with its required collaborators."""
        self.weight_record_repository = WeightRecordRepository()
        self.weight_record_service = WeightRecordService()
        self.device_threshold_repository = DeviceThresholdRepository()
        self.device_repository = DeviceRepository()

    def create_weight_record(
        self,
        device_id: str,
        weight: float,
        created_at: str | None,
    ) -> tuple:
        """Execute the creation and processing of a weight record use-case.

        Args:
            device_id (str): Identifier of the device submitting the reading.
            weight (float): Weight measurement expressed in grams.
            created_at (str | None): ISO 8601 timestamp of the reading. Passed
                to the domain service; accepts ``None`` to default to the
                current UTC time.

        Returns:
            WeightRecord: Persisted domain entity populated with its assigned ``id``.

        Raises:
            ValueError: If no device matches the ``device_id``
        """
        if not self.device_repository.find_by_id(device_id):
            raise ValueError("Device not found")

        # Retrieves the custom supply weight for the device
        device_threshold: DeviceThreshold = self.device_threshold_repository.get_by_device_id(device_id)
        custom_supply_weight = device_threshold.custom_supply_weight

        # Calculates the physical stock based on the raw weight and custom supply weight
        physical_stock = float(self.weight_record_service.calculate_physical_stock(weight, custom_supply_weight))

        # Creates a new weight record using the calculated physical stock
        record = self.weight_record_service.create_record(device_id, weight, physical_stock, created_at)

        # Persists the record and computes updated averages
        saved_record = self.weight_record_repository.save(record)

        # Retrieves recent records from the configured interval and computes the average
        recent_records = self.weight_record_repository.find_by_device_in_interval(device_id)
        averages = self.weight_record_service.calculate_averages(recent_records)

        # Returns the saved record and updated averages
        return saved_record, averages


class EnvironmentRecordApplicationService:
    """Application service that orchestrates the create environment record
    use-case.

    Responsibilities:

    1. Cross-context validation – delegates to the IAM
       :class:`~iam.infrastructure.repositories.DeviceRepository` to verify
       that the requesting device is registered and the supplied API key is
       valid.
    2. Domain logic – delegates to
       :class:`~tracking.domain.services.EnvironmentRecordService` to validate
       raw sensor values and construct an
       :class:`~tracking.domain.entities.EnvironmentRecord` entity.
    3. Persistence – delegates to
       :class:`~tracking.infrastructure.repositories.EnvironmentRecordRepository`
       to persist the entity and return the saved aggregate with its assigned
       identity.
    4. Aggregation – retrieves recent records from the configured interval and
       computes the average temperature and humidity through the domain
       service.
    """

    def __init__(self):
        """Initialize the service with its required collaborators."""
        self.environment_record_repository = EnvironmentRecordRepository()
        self.environment_record_service = EnvironmentRecordService()
        self.device_repository = DeviceRepository()

    def create_environment_record(
        self,
        device_id: str,
        temperature: float,
        humidity: float,
        created_at: str | None,
    ) -> tuple:
        """Execute the creation and processing of an environment record use-case.

        Validates that the device identified by ``device_id`` is registered and
        that the supplied ``api_key`` matches the stored credential before
        delegating record creation to the domain service, persisting the
        result, and computing updated averages.

        Args:
            device_id (str): Identifier of the device submitting the reading.
            temperature (float): Temperature measurement expressed in degrees
                Celsius.
            humidity (float): Relative humidity measurement expressed as a
                percentage.
            created_at (str | None): ISO 8601 timestamp of the reading. Passed
                to the domain service; accepts ``None`` to default to the
                current UTC time.
            api_key (str): Value of the ``X-API-Key`` request header used to
                authenticate the device.

        Returns:
            tuple[EnvironmentRecord, dict]: A two-element tuple containing the
            persisted domain entity and a dictionary with
            ``average_temperature`` and ``average_humidity`` keys.

        Raises:
            ValueError: If no device matches the ``device_id`` / ``api_key``
            combination, or if the domain service rejects the sensor values.
        """
        if not self.device_repository.find_by_id(device_id):
            raise ValueError("Device not found")

        record = self.environment_record_service.create_record(
            device_id, temperature, humidity, created_at
        )
        saved_record = self.environment_record_repository.save(record)

        recent_records = self.environment_record_repository.find_by_device_in_interval(
            device_id
        )
        averages = self.environment_record_service.calculate_averages(recent_records)

        return saved_record, averages
