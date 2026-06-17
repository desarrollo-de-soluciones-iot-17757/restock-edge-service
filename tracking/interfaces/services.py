"""Interface layer for the Tracking bounded context.

Exposes a Flask Blueprint (``tracking_api``) that translates incoming HTTP
requests into calls to the application service and maps the results back to
JSON responses.  This layer owns no domain logic; it is responsible for I/O
concerns such as request parsing, authentication delegation and HTTP status
code selection.
"""
from flask import Blueprint, jsonify, request

from iam.interfaces.services import authenticate_request
from tracking.application.services import WeightRecordApplicationService


tracking_api = Blueprint("tracking_api", __name__)

# Module-level singleton; it contains no request-specific mutable state.
weight_record_service = WeightRecordApplicationService()


@tracking_api.route("/api/v1/tracking/weight-records", methods=["POST"])
def create_weight_record():
    """Create a new weight telemetry record.

    Validates device identity through the ``X-API-Key`` header and the
    ``device_id`` field in the request body before delegating to the
    application service to apply domain rules and persist the record.

    Request headers:
        X-API-Key: API key paired with the device.
        Content-Type: Must be ``application/json``.

    Request body:
        ``device_id`` (str): Identifier of the submitting device.
        ``weight`` (float): Weight reading expressed in grams.
        ``created_at`` (str, optional): ISO 8601 timestamp. Defaults to the
        current UTC time when omitted.

    Responses:
        201 Created: Record saved successfully. Body contains the persisted
        record with its assigned ``id`` and UTC ``created_at``.
        400 Bad Request: A required field is missing or a value is invalid.
        401 Unauthorized: ``device_id`` or ``X-API-Key`` is absent or invalid.

    Returns:
        tuple[flask.Response, int]: JSON response body paired with the
        appropriate HTTP status code.
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json
    try:
        device_id = data["device_id"]
        weight = data["weight"]
        created_at = data.get("created_at")
        record = weight_record_service.create_weight_record(
            device_id,
            weight,
            created_at,
            request.headers.get("X-API-Key"),
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "weight": record.weight,
            "created_at": record.created_at.isoformat(),
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
