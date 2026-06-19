"""Domain entities for the Tracking bounded context.

This module defines the core aggregate used by the edge service to represent a
weight telemetry record.  Entities carry identity and encapsulate domain state;
they should only be created or mutated through domain services that enforce
business invariants.
"""
from datetime import datetime


class WeightRecord:
    """Aggregate root representing a single weight telemetry reading.

    A ``WeightRecord`` captures the measured weight submitted by a specific
    Restock smart scale at a given point in time.  Instances are created by
    :meth:`~tracking.domain.services.WeightRecordService.create_record`, which
    validates the raw sensor data before constructing this entity.

    Attributes:
        id (int | None): Surrogate identity assigned by the persistence layer
            after the record is saved. ``None`` for transient instances.
        device_id (str): Identifier of the device that produced the reading.
        weight (float): Weight measurement expressed in grams.
        created_at (datetime): UTC timestamp of when the reading was captured.
    """

    def __init__(self, device_id: str, weight: float, created_at: datetime, id: int = None):
        """Initialize a WeightRecord entity.

        Args:
            device_id (str): Identifier of the originating device.
            weight (float): Weight measurement expressed in grams.
            created_at (datetime): UTC timestamp of the reading.
            id (int, optional): Persistence identity. Defaults to ``None`` for
                transient entities that have not been saved yet.
        """
        self.id = id
        self.device_id = device_id
        self.weight = weight
        self.created_at = created_at


class EnvironmentRecord:
    """Aggregate root representing a single environment telemetry reading.

    An ``EnvironmentRecord`` captures the measured temperature and humidity
    submitted by a specific Restock smart scale at a given point in time.
    Instances are created by
    :meth:`~tracking.domain.services.EnvironmentRecordService.create_record`,
    which validates the raw sensor data before constructing this entity.

    Attributes:
        id (int | None): Surrogate identity assigned by the persistence layer
            after the record is saved. ``None`` for transient instances.
        device_id (str): Identifier of the device that produced the reading.
        temperature (float): Temperature measurement expressed in degrees
            Celsius.
        humidity (float): Relative humidity measurement expressed as a
            percentage.
        created_at (datetime): UTC timestamp of when the reading was captured.
    """

    def __init__(self, device_id: str, temperature: float, humidity: float,
                 created_at: datetime, id: int = None):
        """Initialize an EnvironmentRecord entity.

        Args:
            device_id (str): Identifier of the originating device.
            temperature (float): Temperature measurement expressed in degrees
                Celsius.
            humidity (float): Relative humidity measurement expressed as a
                percentage.
            created_at (datetime): UTC timestamp of the reading.
            id (int, optional): Persistence identity. Defaults to ``None`` for
                transient entities that have not been saved yet.
        """
        self.id = id
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.created_at = created_at
