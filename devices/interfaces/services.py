"""
Interface layer for the Devices bounded context.

Exposes a Flask Blueprint (``devices_api``) that translates incoming HTTP
requests into calls to the application service and maps the results back to
JSON responses.  This layer owns no domain logic; it is responsible for I/O
concerns such as request parsing, authentication delegation, and HTTP status
code selection.
"""
from flask import Blueprint, jsonify, request

from devices.application.services import DeviceThresholdApplicationService
from iam.interfaces.services import authenticate_request

# This module defines the Flask Blueprint for device-related API endpoints and initializes
devices_api = Blueprint("devices_api", __name__)

# Module-level singleton; it contains no request-specific mutable state.
device_threshold_service = DeviceThresholdApplicationService()

@devices_api.route("/api/v1/devices/<device_id>/thresholds", methods=["POST"])
def create_threshold_for_device(device_id: str):
    """
    Endpoint to create a new device threshold.

    :param device_id: The id of the device.

    :return: JSON response with a success message and HTTP status code.
    :except: KeyError if required fields are missing or ValueError if invalid data is provided.
    """

    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json

    try:
        custom_supply_weight = data["custom_supply_weight"]
        custom_supply_unit_measurement = data["custom_supply_unit_measurement"]
        minimum_humidity_percentage = data["minimum_humidity_percentage"]
        maximum_humidity_percentage = data["maximum_humidity_percentage"]
        minimum_temperature_in_celsius = data["minimum_temperature_in_celsius"]
        maximum_temperature_in_celsius = data["maximum_temperature_in_celsius"]

        record = device_threshold_service.create_device_threshold(
            device_id,
            custom_supply_weight,
            custom_supply_unit_measurement,
            minimum_humidity_percentage,
            maximum_humidity_percentage,
            minimum_temperature_in_celsius,
            maximum_temperature_in_celsius,
        )

        return jsonify({
            "success": "Threshold registered successfully in edge service for device: " + record.device_id + ""
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@devices_api.route("/api/v1/devices/<device_id>/thresholds", methods=["PUT"])
def update_threshold_for_device(device_id: str):
    """
    Endpoint to update an existing device threshold or to assign a new batch to a device.

    :param device_id: The id of the device.
    :return: JSON response with a success message and HTTP status code.
    """

    auth_result = authenticate_request()
    if auth_result:
        return auth_result

    data = request.json

    try:
        assigned_batch_id = data["assigned_batch_id"]
        custom_supply_weight = data["custom_supply_weight"]
        custom_supply_unit_measurement = data["custom_supply_unit_measurement"]
        minimum_humidity_percentage = data["minimum_humidity_percentage"]
        maximum_humidity_percentage = data["maximum_humidity_percentage"]
        minimum_temperature_in_celsius = data["minimum_temperature_in_celsius"]
        maximum_temperature_in_celsius = data["maximum_temperature_in_celsius"]

        record = device_threshold_service.update_device_threshold(
            device_id,
            assigned_batch_id,
            custom_supply_weight,
            custom_supply_unit_measurement,
            minimum_humidity_percentage,
            maximum_humidity_percentage,
            minimum_temperature_in_celsius,
            maximum_temperature_in_celsius,
        )

        return jsonify({
            "success": "Threshold updated successfully in edge service for device: " + record.device_id + ""
        }), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as error:
        return jsonify({"error": str(error)}), 400