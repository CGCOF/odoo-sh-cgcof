# -*- coding: utf-8 -*-
# Part of Aselcis. See LICENSE file for full copyright and licensing details.
import sys
import traceback
import base64
import datetime
import time
import dateutil
import dateutil.parser
import dateutil.relativedelta
import dateutil.rrule
import dateutil.tz
import ast
import pytz

from odoo import api, fields, models, exceptions, _
from odoo.tools.safe_eval import safe_eval, test_python_expr
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
from odoo.osv import expression


class APIEndpoint(models.Model):
    _name = 'api.endpoint'
    _description = 'API Endpoint'
    _rec_name = 'display_name'
    _order = 'name'

    name = fields.Char('Route', required=True)
    display_name = fields.Char(
        'Full path', compute='_compute_display_name', store=True)
    api_version = fields.Selection([
        ('v1', 'v1')
    ], required=True)
    method = fields.Selection([
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE')
    ], string='Method', required=True)
    active = fields.Boolean(default=True)
    request_code = fields.Text(required=True)
    record_code = fields.Text(required=True)
    response_code = fields.Text(required=True)
    need_auth = fields.Boolean('Need authentication?', default=True)

    _sql_constraints = [
        ('name_version_unique',
         'unique(name,api_version,method)',
         "Another endpoint already exists with this name and API version!"),
    ]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = default or {}
        default['name'] = self.name + _(' (copy)')
        return super(APIEndpoint, self).copy(default=default)

    @api.depends('name', 'api_version')
    def _compute_display_name(self):
        for record in self:
            record.display_name = '/api/{}/{}'.format(
                record.api_version,
                record.name
            )

    def _python_code_context(self):
        """ evaluation context to pass to safe_eval """
        def unslug_url(record_slug):
            if not record_slug:
                return None
            try:
                record_id = record_slug.split('-')[-1:][0]
                return int(record_id)
            except ValueError:
                return None
            
        return {
            'action': self,
            'ctx': self._context,
            'env': self.env,
            'uid': self._uid,
            'user': self.env.user,
            'time': time,
            'datetime': datetime,
            'fields': fields,
            'dateutil': dateutil,
            'pytz': pytz,
            'b64encode': base64.b64encode,
            'b64decode': base64.b64decode,
            'expr': expression,
            'list': list,
            'map': map,
            'filter': filter,
            'abs': abs,
            'range': range,
            'type': type,
            'isinstance': isinstance,
            'getattr': getattr,
            'hasattr': hasattr,
            'Warning': Warning,
            'exceptions': exceptions,
            'literal_eval': ast.literal_eval,
            'slug': slug,
            'unslug_url': unslug_url,
            'request': request
        }

    def run_endpoint(self, params):
        self.ensure_one()
        return self.run_request(params)

    def run_request(self, params):
        self.ensure_one()
        ctx = self._python_code_context()
        ctx.update({
            'data': None,
            'data_count': None,
            'params': params
        })
        safe_eval(self.request_code.strip(), ctx, mode="exec", nocopy=True)
        data = ctx.get('data')
        data_count = ctx.get('data_count')
        if type(data) == list or isinstance(data, models.Model):
            values = []
            for d in data:
                values.append(self.run_record(d))
        else:
            values = self.run_record(data)
        response = self.run_response(values)
        if data_count is not None:
            headers = response.get('headers')
            headers.append(('X-Total-Count', data_count))
            response.update({
                'headers': headers
            })
        return response

    def run_record(self, record):
        self.ensure_one()
        ctx = self._python_code_context()
        ctx.update({
            'record': record,
            'data': None
        })
        safe_eval(
            self.record_code.strip(),
            ctx,
            mode="exec",
            nocopy=True
        )
        return ctx.get('data')

    def run_response(self, values):
        self.ensure_one()
        ctx = self._python_code_context()
        ctx.update({
            'values': values,
            'data': {
                'content-type': 'application/json; charset=utf-8',
                'headers': [
                    ("Cache-Control", "no-store"),
                    ("Pragma", "no-cache")
                ],
                'response': None
            },
        })
        safe_eval(
            self.response_code.strip(),
            ctx,
            mode="exec",
            nocopy=True
        )
        return ctx.get('data')

    def _check_python_code_syntax(self, field_name):
        """
        Syntax check the python code
        """
        for record in self:
            code = getattr(record, field_name).strip()
            msg = test_python_expr(expr=code, mode='exec')
            if msg:
                raise exceptions.ValidationError(msg)

    @api.constrains('request_code')
    def _check_request_code_syntax(self):
        self._check_python_code_syntax('request_code')

    @api.constrains('record_code')
    def _check_record_code_syntax(self):
        self._check_python_code_syntax('record_code')

    @api.constrains('response_code')
    def _check_response_code_syntax(self):
        self._check_python_code_syntax('response_code')
