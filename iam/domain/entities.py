"""Domain entities for the IAM bounded context.

This module defines the aggregate root used by the edge service to represent a
registered Restock IoT device.  Entities carry identity across their lifetime
and encapsulate state that is only modified by services enforcing domain
invariants.
"""
from datetime import datetime


class Device:
    """Aggregate root representing a registered Restock IoT device.

    A ``Device`` is the core identity object in the IAM bounded context.  It is
    identified by a unique ``device_id`` and authenticated through its paired
    ``api_key``.  Device registration and lookup are managed by the
    :class:`~iam.infrastructure.repositories.DeviceRepository`.

    Attributes:
        device_id (str): Immutable, unique identifier for the physical device
            (for example, ``'restock-scale-001'``).
        api_key (str): Secret key used to authenticate HTTP requests generated
            by the device.  The key is expected in the ``X-API-Key`` header.
        created_at (datetime): UTC timestamp recording when the device was
            first registered in the local edge database.
    """

    def __init__(self, device_id: str, api_key: str, created_at: datetime):
        """Initialize a Device aggregate root.

        Args:
            device_id (str): Unique identifier for the Restock IoT device.
            api_key (str): Secret API key paired with the device.
            created_at (datetime): UTC timestamp of device registration.
        """
        self.device_id = device_id
        self.api_key = api_key
        self.created_at = created_at
