from odoo import api, fields, models
from datetime import timedelta

class HostelRoom(models.Model):
    _inherit = 'hostel.room'

    date_terminate = fields.Date('Date of Termination')

    def make_closed(self):
        day_to_allocate = self.category_id.max_allow_days or 10
        self.date_terminate = fields.Date.today() + timedelta(days=day_to_allocate)
        return super(HostelRoom, self).make_closed()

    def make_available(self):
        self.date_terminate = False
        return super(HostelRoom, self).make_available()