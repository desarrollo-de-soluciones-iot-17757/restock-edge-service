"""Peewee ORM model for the IAM bounded context.

Defines the ``devices`` database table used to persist
:class:`~iam.domain.entities.Device` aggregate roots.  This module belongs to
the infrastructure layer; it must not be imported directly by the domain or
application layers.  Access is mediated through the repository.
"""
from peewee import CharField, DateTimeField, Model

from shared.infrastructure.database import db


class Device(Model):
    """ORM mapping for the ``devices`` table.

    Each row represents a registered Restock IoT device and its associated API
    key, which is used to authenticate inbound telemetry requests.

    Attributes:
        device_id (CharField): Natural primary key and human-readable hardware
            identifier, for example ``'restock-scale-001'``.
        api_key (CharField): Secret key paired with the device and checked on
            authenticated API calls.
        created_at (DateTimeField): UTC timestamp recording when the device was
            registered in the local edge database.
    """

    device_id = CharField(primary_key=True)
    api_key = CharField()
    created_at = DateTimeField()

    class Meta:
        """Peewee metadata that binds the model to the shared database."""

        database = db
        table_name = "devices"
