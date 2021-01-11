# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
import functools
import logging
import json
import werkzeug.wrappers

from odoo import http
from odoo.addons.api_rest.common import (
    process_params,
    invalid_response,
    valid_response,
)
from odoo.http import request
from odoo.osv import expression
from odoo.addons.web.controllers.main import _serialize_exception

_logger = logging.getLogger(__name__)


def validate_token(func):

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        '''.'''

        # If endpoint not need auth
        endpoint = request.env['api.endpoint'].search([
            ('api_version', '=', kwargs.get('version')),
            ('name', '=', kwargs.get('path_route')),
            ('method', '=', request.httprequest.method),
            ('need_auth', '=', False)
        ])
        if endpoint:
            return func(self, *args, **kwargs)

        # Check authentication
        access_token = request.httprequest.headers.get('Authorization')
        if not access_token:
            return invalid_response(
                'missing token', 'missing access token in request header.', 401
            )
        access_token = access_token.split(' ')
        if len(access_token) != 2:
            return invalid_response(
                'invalid token', 'token seems to be invalid.', 401
            )
        if access_token[0] != 'Bearer':
            return invalid_response(
                'invalid auth method ', 'token authentication method is invalid.', 401
            )
        access_token = access_token[1]
        access_token_data = (
            request.env['api.access_token']
            .sudo()
            .search([('token', '=', access_token)], order='id DESC', limit=1)
        )

        if access_token_data:
            saved_access_token = access_token_data.find_one_or_create_token(
                user_id=access_token_data.user_id.id)
            if saved_access_token != access_token:
                return invalid_response(
                    'expired token', 'token seems to have expired.', 401
                )
            request.session.uid = access_token_data.user_id.id
            request.uid = access_token_data.user_id.id
        else:
            user = request.env['res.users'].sudo().search([
                ('oauth_access_token', '=', access_token)
            ], limit=1)
            if not user:
                return invalid_response(
                    'expired token', 'token seems to have expired.', 401
                )
            request.session.uid = user.id
            request.uid = user.id
        return func(self, *args, **kwargs)

    return wrap


class APIController(http.Controller):

    def process_error(self, e, debug=False):
        error = _serialize_exception(e)
        if error.get('debug') and not debug:
            del error['debug']
        return error


    def process_request(self, method, version, path_route, **params):
        endpoint = request.env['api.endpoint'].search([
            ('api_version', '=', version),
            ('name', '=', path_route),
            ('method', '=', method)
        ])
        if not endpoint:
            return invalid_response(
                'missing error',
                'endpoint not found',
                404,
            )

        try:
            params = process_params(params)
            data = endpoint.run_endpoint(params)
        except Exception as e:
            result = json.dumps({'error': self.process_error(e)})
            return werkzeug.wrappers.Response(
                status=500,
                content_type='application/json; charset=utf-8',
                response=result
            )

        content_type = data.get('content-type')
        headers = data.get('headers')
        response = data.get('response')
        if 'application/json' in content_type:
            response = json.dumps(response)

        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json; charset=utf-8',
            headers=headers,
            response=response,
        )

    @validate_token
    @http.route(
        '/api/<string:version>/<path:path_route>',
        type='http',
        auth='none',
        methods=['GET'],
        csrf=False)
    def get(self, version, path_route, **params):
        return self.process_request('GET', version, path_route, **params)

    @validate_token
    @http.route(
        '/api/<string:version>/<path:path_route>',
        type='http',
        auth='none',
        methods=['POST'],
        csrf=False)
    def post(self, version, path_route, **params):
        try:
            post = json.loads(request.httprequest.data)
        except Exception:
            return invalid_response(
                "invalid body",
                "Invalid body JSON format",
                400,
            )
        params.update({'body': post})
        return self.process_request('POST', version, path_route, **params)

    @validate_token
    @http.route(
        '/api/<string:version>/<path:path_route>',
        type='http',
        auth='none',
        methods=['PUT'],
        csrf=False)
    def put(self, version, path_route, **params):
        try:
            post = json.loads(request.httprequest.data)
        except Exception:
            return invalid_response(
                "invalid body",
                "Invalid body JSON format",
                400,
            )
        params.update({'body': post})
        return self.process_request('PUT', version, path_route, **params)

    @validate_token
    @http.route(
        '/api/<string:version>/<path:path_route>',
        type='http',
        auth='none',
        methods=['DELETE'],
        csrf=False)
    def delete(self, version, path_route, **params):
        return self.process_request('DELETE', version, path_route, **params)
