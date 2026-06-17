"""Shared database infrastructure for the Restock Edge Service.

Provides a single :class:`peewee.SqliteDatabase` instance (``db``) that is
imported by ORM models across all bounded contexts, ensuring every model
operates on the same physical database file.

The :func:`init_db` helper is called once at application start-up to open a
connection and create any missing tables without affecting existing data
(``safe=True``).

Note:
    The ``db`` object itself is not connected until :func:`init_db` is called.
    Peewee's ``SqliteDatabase`` manages the connection lifecycle through its
    own thread-local storage.
"""
from peewee import SqliteDatabase

# Shared SQLite database instance used by all bounded-context ORM models.
db = SqliteDatabase("restock_edge.db")


def init_db() -> None:
    """Open the database connection and create all required tables.

    Imports ORM models from the IAM and Tracking bounded contexts at call time
    through deferred imports.  This avoids circular dependencies during module
    loading and keeps table creation centralized in the shared infrastructure.

    This function is idempotent: calling it when the tables already exist is
    safe and has no side effects because ``safe=True`` suppresses create-table
    errors for pre-existing tables.

    Side effects:
        - Opens a connection to ``restock_edge.db`` when needed.
        - Creates the ``devices`` table if absent.
        - Creates the ``weight_records`` table if absent.
        - Creates the ``device_thresholds`` table if absent.
        - Closes the connection after table creation.
    """
    should_close = db.is_closed()
    if should_close:
        db.connect()

    from iam.infrastructure.models import Device
    from tracking.infrastructure.models import WeightRecord
    from devices.infrastructure.models import DeviceThresholdModel

    db.create_tables([
        Device,
        WeightRecord,
        DeviceThresholdModel
    ], safe=True)

    if should_close and not db.is_closed():
        db.close()
