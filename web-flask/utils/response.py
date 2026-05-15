from flask import jsonify


def success_response(data=None, message="ok", http_status=200):
    return jsonify({"code": 0, "message": message, "data": {} if data is None else data}), http_status


def error_response(message="error", code=400, data=None, http_status=None):
    status = http_status or code or 400
    return jsonify({"code": code, "message": message, "data": data}), status
