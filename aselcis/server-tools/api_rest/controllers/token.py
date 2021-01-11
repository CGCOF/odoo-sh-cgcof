# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
import json
import logging

import werkzeug.wrappers

from odoo import http
from odoo.addons.api_rest.common import invalid_response, valid_response, msg_response
from odoo.http import request

_logger = logging.getLogger(__name__)


try:
    import jwt
except ImportError:
    _logger.warn('Module jwt cannot loaded.')


class AccessToken(http.Controller):

    @http.route(
        "/api/v1/auth/token",
        type='http',
        auth='public',
        methods=["POST"],
        csrf=False
    )
    def token(self):
        try:
            post = json.loads(request.httprequest.data)
        except Exception as e:
            return invalid_response(
                "invalid body",
                "Invalid body JSON format",
                400,
            )
        _token = request.env["api.access_token"]
        params = ["db", "login", "password"]
        params = {key: post.get(key) for key in params if post.get(key)}
        db, username, password = (
            params.get("db", request.db),
            params.get("login"),
            params.get("password"),
        )
        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            # The request post body is empty the credetials maybe passed via the headers.
            headers = request.httprequest.headers
            db = headers.get("db")
            username = headers.get("login")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                # Empty 'db' or 'username' or 'password:
                return invalid_response(
                    "missing error",
                    "either of the following are missing [db, username,password]",
                    403,
                )
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return invalid_response("wrong database name", error, 403)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            return invalid_response(401, error, info)

        # Generate tokens
        access_token = _token.find_one_or_create_token(user_id=uid, create=True)
        # Successful response:
        return werkzeug.wrappers.Response(
            status=200,
            content_type="text/plan",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=access_token
        )

    @http.route(
        "/api/v1/auth/token",
        methods=["DELETE"],
        type="http",
        auth="none",
        csrf=False
    )
    def delete(self, **post):
        """."""
        _token = request.env["api.access_token"]
        access_token = request.httprequest.headers.get("access_token")
        access_token = _token.sudo().search([("token", "=", access_token)])
        if not access_token:
            info = "No access token was provided in request!"
            error = "no_access_token"
            _logger.error(info)
            return invalid_response(400, error, info)
        access_token.unlink()
        # Successful response:
        return msg_response(
            {"desc": "token successfully deleted", "delete": True}, 200
        )
