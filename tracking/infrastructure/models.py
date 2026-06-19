"""Peewee ORM model for the Tracking bounded context.

Defines the ``weight_records`` database table structure used to persist
:class:`~tracking.domain.entities.WeightRecord` domain entities.  This module
belongs to the infrastructure layer and must not be referenced directly from
the domain or application layers; access is mediated through the repository.
"""
from peewee import AutoField, CharField, DateTimeField, FloatField, Model

from shared.infrastructure.database import db


class WeightRecord(Model):
    """ORM mapping for the ``weight_records`` table.

    Each row represents a single weight reading submitted by a registered
    Restock smart scale device.

    Attributes:
        id (AutoField): Auto-incrementing integer primary key assigned by the
            database on insert.
        device_id (CharField): Device identifier that produced the reading.
            Stored as a plain string to keep bounded contexts loosely coupled.
        weight (FloatField): Weight measurement expressed in grams.
        created_at (DateTimeField): UTC timestamp of when the device captured
            the reading.
    """

    id = AutoField()
    device_id = CharField()
    weight = FloatField()
    created_at = DateTimeField()

    class Meta:
        """Peewee metadata that binds the model to the shared database."""

        database = db
        table_name = "weight_records"


class EnvironmentRecordModel(Model):
    """ORM mapping for the ``environment_records`` table.

    Each row represents a single environment reading (temperature and humidity)
    submitted by a registered Restock smart scale device.

    Attributes:
        id (AutoField): Auto-incrementing integer primary key assigned by the
            database on insert.
        device_id (CharField): Device identifier that produced the reading.
            Stored as a plain string to keep bounded contexts loosely coupled.
        temperature (FloatField): Temperature measurement expressed in degrees
            Celsius.
        humidity (FloatField): Relative humidity measurement expressed as a
            percentage.
        created_at (DateTimeField): UTC timestamp of when the device captured
            the reading.
    """

    id = AutoField()
    device_id = CharField()
    temperature = FloatField()
    humidity = FloatField()
    created_at = DateTimeField()

    class Meta:
        """Peewee metadata that binds the model to the shared database."""

        database = db
        table_name = "environment_records"
