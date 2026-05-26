"""Interface layer for the IAM bounded context.

Exposes a Flask Blueprint (``iam_api``) and a shared authentication helper
(``authenticate_request``) used by other bounded contexts to guard their own
endpoints.  This layer owns no domain or business logic; it is concerned with
HTTP request handling and delegation to the application service.
"""
from flask import Blueprint, jsonify, request

from iam.application.services import AuthApplicationService


iam_api = Blueprint("iam_api", __name__)

# Module-level singleton instantiated once per worker process.
auth_service = AuthApplicationService()


def authenticate_request():
    """Validate the device identity for an incoming HTTP request.

    Extracts ``device_id`` from the JSON request body and ``X-API-Key`` from
    the request headers, then delegates to the IAM application service to
    verify the credentials against the local device registry.

    This helper is intended to be called at the start of any route handler in a
    bounded context that requires device authentication::

        auth_result = authenticate_request()
        if auth_result:
            return auth_result

    Expected request contract:
        - ``Content-Type: application/json`` with a body containing
          ``device_id``.
        - ``X-API-Key`` header carrying the device secret API key.

    Returns:
        tuple[flask.Response, int] | None: ``(JSON response, 401)`` when
        authentication fails; ``None`` when the request is authenticated.
    """
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")

    if not device_id or not api_key:
        return jsonify({"error": "Missing device_id or X-API-Key"}), 401

    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401

    return None
