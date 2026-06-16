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
    def create_or_get(mac_address: str) -> tuple[Device, bool]:
        """Create a device for the given MAC address, or return the existing one.

        ``device_id`` is assigned automatically by the database as an
        auto-incrementing integer; ``api_key`` stores ``mac_address``.

        Args:
            mac_address (str): MAC address of the device.

        Returns:
            tuple[Device, bool]: The domain entity, and ``True`` if it was
            newly created, ``False`` if it already existed.
        """
        device, created = DeviceModel.get_or_create(
            api_key=mac_address,
            defaults={"created_at": datetime.now(timezone.utc)},
        )
        return Device(device.device_id, device.api_key, device.created_at), created
