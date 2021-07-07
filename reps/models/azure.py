# -*- coding: utf-8 -*-
# Part of Aselcis Consulting SL. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from azure.storage.blob import BlockBlobService, PublicAccess
from odoo.exceptions import ValidationError


class AzureBlobs(models.Model):
    _name = 'azure.blobs'
    _description = 'Azure blobls instance'

    name = fields.Char()
    account_name = fields.Char()
    account_key = fields.Char()
    container_ids = fields.One2many(
        'azure.blobs.container', 'blob_id', string='Containers')

    def get_block_blob_service(self):
        if self.account_name and self.account_key:
            return BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        return False

    @api.multi
    def list_containers(self):
        blob = self.get_block_blob_service()
        if blob:
            new_containers = [container.name for container in blob.list_containers()]
            for container in self.container_ids:
                if not blob.exists(container.name):
                    container.unlink()
                else:
                    new_containers.remove(container.name)
            if new_containers:
                vals = [(0, 0, {
                    'blob_id': self.id,
                    'name': container
                })for container in new_containers]
                self.write({'container_ids': vals})


class AzureBlobsContainer(models.Model):
    _name = 'azure.blobs.container'
    _description = 'Azure blobs container'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_compute_display_name')
    blob_id = fields.Many2one('azure.blobs')
    name = fields.Char()

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'{record.blob_id.name} / {record.name}'
