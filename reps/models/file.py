from odoo import models, fields


class FileDataTemplate(models.Model):

    _inherit = 'file.data.template'
    type = fields.Char()
