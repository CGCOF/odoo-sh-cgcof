# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import pytz


class RepsHistory(models.Model):
    _name = 'reps.history'
    _description = 'Reps history'

    college_id = fields.Many2one(
        'res.college', 'College')
    shipping_type = fields.Char()
    shipping_date = fields.Datetime()
    file = fields.Char()


class RepsAzureFile(models.Model):
    _name = 'reps.azure.file'
    _description = 'Logical reps azure file conection'

    name = fields.Char()
    container_id = fields.Many2one('azure.blobs.container')
    _active = fields.Boolean()
    container_path_ids = fields.One2many(
        'reps.container.path', 'azure_file_id')

    @api.multi
    def send_files(self):
        if self._active:
            block_blob_service = self.container_id.blob_id.get_block_blob_service()
            reps_history = self.env['reps.history']
            for path_generator in self.container_path_ids:
                for attachment_id in path_generator.generator_id.attachment_ids:
                    full_path = attachment_id._get_path(
                        None, attachment_id.checksum)[1]
                    vals = {
                        'college_id': attachment_id.res_id,
                        'file': attachment_id.datas_fname,
                        'shipping_type': path_generator.generator_id.data_template_id.type,
                        'shipping_date': datetime.now(pytz.timezone(self._context.get('tz') or 'UTC'))
                    }
                    try:
                        result = block_blob_service.create_blob_from_path(
                            f"{self.container_id.name}/{path_generator.path or ''}", attachment_id.datas_fname, full_path)
                        if result.etag:
                            reps_history.create(vals)
                            attachment_id.unlink()
                    except Exception as e:
                        raise UserError(_(e))
    @api.model
    def cron_send_files(self):
        if not self:
            self = self.search([('_active', '=', True)])
        for record in self:
            record.send_files()



class RepsContainerLogicalRoute(models.Model):
    _name = 'reps.container.path'
    _description = 'Azure Container path'

    azure_file_id = fields.Many2one('reps.azure.file')
    generator_id = fields.Many2one('file.generator.instance')
    path = fields.Char()

    @api.onchange('path')
    def onchange_logial_route(self):
        if self.path:
            blob_service = self.azure_file_id.container_id.blob_id.get_block_blob_service()
            blob_names = blob_service.list_blob_names(
                container_name=self.azure_file_id.container_id.name, prefix=self.path)
            if len(list(blob_names)) == 0:
                raise ValidationError(
                    _(f"Path {self.path} on container {self.azure_file_id.container_id.name} does not exit"))
