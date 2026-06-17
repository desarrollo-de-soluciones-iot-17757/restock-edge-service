"""Flask application entry point for the Restock Edge Service.

This module wires together the Flask application, registers the IAM and
Tracking bounded-context Blueprints, and ensures the SQLite database is
initialized exactly once before the first HTTP request is handled.

Typical usage::

    flask --app app run
    # or
    python app.py
"""
from flask import Flask

import iam.application.services
from devices.interfaces.services import devices_api
from iam.interfaces.services import iam_api
from shared.infrastructure.database import init_db
from tracking.interfaces.services import tracking_api

# The Flask application instance.
app = Flask(__name__)

# The IAM bounded-context Blueprint is registered first to ensure its authentication logic is available
app.register_blueprint(iam_api)

# The Tracking bounded-context Blueprint is registered next, followed by the Devices Blueprint.  This ordering allows the Tracking endpoints to delegate authentication to the IAM service before processing device-related requests.
app.register_blueprint(tracking_api)

# The Devices bounded-context Blueprint is registered last, as it may depend on authentication and tracking logic provided by the previously registered Blueprints.  This ordering ensures that all necessary services are available when handling device-related API requests.
app.register_blueprint(devices_api)

# Flag to track whether the database has been initialized.
first_request = True


@app.before_request
def setup():
    """Initialize the database and seed a test device on the first request.

    Uses a module-level flag (``first_request``) to ensure this one-time setup
    runs only once for the lifetime of the process.  Subsequent requests bypass
    this function entirely.

    Side effects:
        - Creates the SQLite database file (``restock_edge.db``) if absent.
        - Creates ``devices`` and ``weight_records`` tables when they do not
          exist yet.
        - Inserts the default test device (``restock-scale-001``) if it has not
          been created previously.
    """
    global first_request
    if first_request:
        first_request = False
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
