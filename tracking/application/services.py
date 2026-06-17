"""Application services for the Tracking bounded context.

Application services sit between the interface layer and the domain layer. They
orchestrate use-cases by coordinating domain services, domain entities, and
repositories without containing domain logic themselves.
"""
from datetime import datetime, timezone

from devices.infrastructure.repositories import DeviceThresholdRepository
from tracking.domain.entities import WeightRecord
from tracking.domain.services import WeightRecordService
from tracking.infrastructure.repositories import WeightRecordRepository


class WeightRecordApplicationService:
    """Application service that orchestrates the creation of a weight record use-case.

    Responsibilities:

    1. Domain logic – delegates to
       :class:`~tracking.domain.services.WeightRecordService` to validate raw
       sensor values and construct a
       :class:`~tracking.domain.entities.WeightRecord` entity.
    2. Validation - delegates to :class:`~devices.domain.services.DeviceThresholdService` to validate
       the thresholds configured for the device.
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

    def transform_and_save_weight_record(
        self,
        device_id: str,
        raw_weight: float,
    ) -> WeightRecord:
        """Execute the creation of a weight record use-case.

        Validates that the device identified by ``device_id`` is registered and
        that the supplied ``api_key`` matches the stored credential before
        delegating record creation to the domain service and persisting the
        result.

        Args:
            device_id (str): Identifier of the device submitting the reading.
            raw_weight (float): Weight measurement expressed in grams.

        Returns:
            WeightRecord: Persisted domain entity populated with its assigned ``id``.
        """
        threshold = self.device_threshold_repository.get(device_id)
        estimated_physical_stock = (self.weight_record_service
                                    .calculate_physical_stock(raw_weight, threshold.custom_supply_weight))
        created_at = datetime.now(timezone.utc)
        string_created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

        record = (self.weight_record_service
                  .create_record(device_id, raw_weight, estimated_physical_stock, string_created_at))
        return self.weight_record_repository.save(record)
