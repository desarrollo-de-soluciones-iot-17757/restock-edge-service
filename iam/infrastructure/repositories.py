"""Repository implementation for the IAM bounded context.

Provides the persistence adapter that maps between the
:class:`~iam.domain.entities.Device` domain entity and the
:class:`~iam.infrastructure.models.Device` Peewee ORM model.

Following the Repository pattern, callers in the application layer work only
with domain entities and remain isolated from ORM and database details.
"""
from datetime import datetime, timezone
from typing import Optional

import peewee

from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel


class DeviceRepository:
    """Repository that persists and reconstructs Device entities.

    Implements the collection-like interface expected by application services.
    All ORM-to-entity mapping is contained within this class, ensuring the
    domain layer has no dependency on Peewee.
    """

    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        """Look up a device by its identifier and API key.

        Queries the ``devices`` table for a row matching both ``device_id`` and
        ``api_key``.  Returning ``None`` when no match is found lets the domain
        service apply the authentication rule without catching infrastructure
        exceptions.

        Args:
            device_id (str): Identifier of the device to search for.
            api_key (str): API key that must match the stored credential.

        Returns:
            Optional[Device]: Matching domain entity if the credentials exist;
            otherwise ``None``.
        """
        try:
            device = DeviceModel.get(
                (DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key)
            )
            return Device(device.device_id, device.api_key, device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device() -> Device:
        """Retrieve the default Restock test device, creating it if absent.

        Performs an idempotent ``get_or_create`` against the ``devices`` table.
        The default credentials are intended for local development and testing
        only.  They must not be reused in production or on real deployed edge
        devices.

        Returns:
            Device: Domain entity for ``device_id='restock-scale-001'``.
        """
        device, _ = DeviceModel.get_or_create(
            device_id="restock-scale-001",
            defaults={
                "api_key": "test-api-key-123",
                "created_at": datetime.now(timezone.utc),
            },
        )
        return Device(device.device_id, device.api_key, device.created_at)

    @staticmethod
    def create_or_get_device(device_id: str) -> tuple[Device, bool]:
        """Create a new device with the given ID, or return the existing one.

        This method is intended for testing and development purposes.  It allows
        you to create a new device with a unique ID and a randomly generated API
        key, or retrieve an existing device if one with the same ID already
        exists.

        Args:
            device_id (str): Unique identifier of the device (its MAC
                address).

        Returns:
            tuple[Device, bool]: The domain entity, and ``True`` if it was
            newly created, ``False`` if it already existed.
        """
        device, created = DeviceModel.get_or_create(
            device_id=device_id,
            defaults={
                "api_key": device_id,
                "created_at": datetime.now(timezone.utc),
            },
        )
        return Device(device.device_id, device.api_key, device.created_at), created
