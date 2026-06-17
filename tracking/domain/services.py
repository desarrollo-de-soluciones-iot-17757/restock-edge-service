"""Domain services for the Tracking bounded context.

Domain services encapsulate business logic that does not naturally belong to a
single entity.  ``WeightRecordService`` validates raw sensor input and creates a
well-formed: class:`~tracking.domain.entities.WeightRecord` aggregate,
enforcing the invariants of the Tracking bounded context.
"""
from datetime import datetime, timezone

from dateutil.parser import parse

from tracking.domain.entities import WeightRecord


class WeightRecordService:
    """Domain service responsible for the creation of valid weight records.

    This service enforces the current business invariants for Restock weight
    telemetry:

    - ``weight`` must be a numeric value.
    - ``weight`` must be in the range [0, 20000] grams for the initial smart
      scale prototype.
    - ``created_at``, when supplied, must be a valid ISO 8601 timestamp.
    - ``created_at`` is normalized to UTC before persistence.
    """

    MIN_WEIGHT_GRAMS = 0.0
    MAX_WEIGHT_GRAMS = 20000.0

    @classmethod
    def create_record(cls, device_id: str, weight: float, created_at: str | None) -> WeightRecord:
        """Validate raw sensor data and create a new WeightRecord entity.

        Applies domain invariants before constructing the aggregate:

        * ``weight`` is coerced to ``float`` and validated in the range
          [0, 20000].
        * ``created_at`` is parsed and converted to UTC; when ``None``, the
          current UTC timestamp is used.

        Args:
            device_id (str): Identifier of the originating device.
            weight (float): Weight reading expressed in grams.
            created_at (str | None): ISO 8601 timestamp of the reading, for
                example, ``'2026-05-25T12:00:00-05:00'``; or ``None`` to use
                the current UTC time.

        Returns:
            WeightRecord: New unsaved domain entity with a UTC-normalized
            ``created_at`` value.

        Raises:
            ValueError: If ``weight`` is not convertible to ``float``, falls
            outside the allowed range, or if ``created_at`` is not valid ISO
            8601.
        """
        try:
            parsed_weight = float(weight)
            if not (cls.MIN_WEIGHT_GRAMS <= parsed_weight <= cls.MAX_WEIGHT_GRAMS):
                raise ValueError("Invalid weight value")

            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid data format")

        return WeightRecord(device_id, parsed_weight, parsed_created_at)
