# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
import logging
import datetime
import json
import ast

import werkzeug.wrappers

_logger = logging.getLogger(__name__)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def msg_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {
        'message': {'status': status, 'data': data}
    }
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )


def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {"count": len(data), "data": data}
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )


def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {
                'error': {
                    "type": typ,
                    "message": str(message)
                    if str(message)
                    else "wrong arguments (missing validation)",
                }
            },
            default=datetime.datetime.isoformat,
        ),
    )


def process_params(params, offset=0, limit=0, order=None):
    """Parse additional data sent along request."""
    new_params = params.copy()
    new_params.update({
        'domain': ast.literal_eval(params.get("domain", "[]")),
        'offset': int(params.get('offset', 0)),
        'limit': int(params.get('limit', 10)),
        'order': params.get('order'),
        'id': int(params.get('id', 0))
    })
    return new_params


def extract_arguments(payloads, offset=0, limit=0, order=None):
    """Parse additional data  sent along request."""
    fields, domain, payload = [], [], {}

    if payloads.get("domain", None):
        domain = ast.literal_eval(payloads.get("domain"))
    if payload.get("fields"):
        fields += payload.get("fields")
    if payload.get("offset"):
        offset = int(payload["offset"])
    if payload.get("limit"):
        limit = int(payload.get("limit"))
    if payload.get("order"):
        order = payload.get("order")
    return [domain, fields, offset, limit, order]
