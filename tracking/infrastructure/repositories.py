"""Repository implementation for the Tracking bounded context.

Provides the persistence adapter that maps between the: class:`~tracking.domain.entities.WeightRecord` domain entity and
the: class:`~tracking.infrastructure.models.WeightRecord` Peewee ORM model.

Following the Repository pattern, callers in the application layer interact
only with domain entities and are shielded from ORM and database details.
"""
from tracking.domain.entities import WeightRecord
from tracking.infrastructure.models import WeightRecord as WeightRecordModel


class WeightRecordRepository:
    """Repository that persists and reconstructs WeightRecord entities.

    Acts as an in-process collection of domain entities backed by the local
    SQLite database.  Mapping between the ORM model and the domain entity is handled
    entirely within this class, keeping the domain layer free of infrastructure
    concerns.
    """

    @staticmethod
    def save(weight_record: WeightRecord) -> WeightRecord:
        """Persist a transient WeightRecord entity.

        Inserts a new row into the ``weight_records`` table using Peewee's
        ``create`` helper and returns a new domain entity instance populated
        with the database-assigned ``id``.

        Args:
            weight_record (WeightRecord): Transient entity to persist. Its
                ``id`` attribute is expected to be ``None`` at this point.

        Returns:
            WeightRecord: Copy of the input entity enriched with the assigned
            database ``id``.
        """
        record = WeightRecordModel.create(
            device_id=weight_record.device_id,
            weight=weight_record.weight,
        )

        return WeightRecord(
            weight_record.device_id,
            weight_record.weight,
            record.created_at,
            record.id,
        )
