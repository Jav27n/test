from odoo import api, fields, models

class HostelRoom(models.Model):
    _inherit = 'hostel.room'

    date_terminate = fields.Date('Date of Termination')