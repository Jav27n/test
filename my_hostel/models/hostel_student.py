from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class HostelStudent(models.Model):
    _name = 'hostel.student'
    # _inherits = {'res.partner': 'partner_id'}
    _description = 'Hostel Student'

    # partner_id = fields.Many2one('res.partner', default=1)

    name = fields.Char("Student Name", required=True)
    gender = fields.Selection([("male", "Male"),
                               ("female", "Female"), ("other", "Other")],
                              string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True,
                            help="Activate/Deactivate hostel record")

    room_id = fields.Many2one("hostel.room", "Room",
                              help="Select hostel room")

    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')

    # hostel_id = fields.Many2one("hostel.hostel", string="hostel")

    # hostel_id_1 = fields.Many2one("hostel.hostel", string="Select Hostel")

    admission_date = fields.Date("Admission Date",
                                 help="Date of admission in hostel",
                                 default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date",
                                 help="Date on which student discharge")
    # duration = fields.Integer("Duration", compute="_compute_check_duration",
    #                           inverse="_inverse_duration", help="Enter duration of living")
    duration = fields.Integer("Duration", inverse="_inverse_duration",
                   help="Enter duration of living")

    status = fields.Selection([("draft", "Draft"),
                               ("reservation", "Reservation"), ("pending", "Pending"),
                               ("paid", "Done"), ("discharge", "Discharge"), ("cancel", "Cancel")],
                              string="Status", copy=False, default="draft",
                              help="State of the student hostel")

    # @api.depends("admission_date", "discharge_date")
    # def _compute_check_duration(self):
    #     """Method to check duration"""
    #     for rec in self:
    #         if rec.discharge_date and rec.admission_date:
    #             rec.duration = (rec.discharge_date - rec.admission_date).days

    @api.onchange('admission_date', 'discharge_date')
    def onchange_duration(self):
        if self.discharge_date and self.admission_date:
            self.duration = (self.discharge_date.year - \
                             self.admission_date.year) * 12 + \
                            (self.discharge_date.month - \
                             self.admission_date.month)

    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')

    # def action_assign_room(self):
    #     self.ensure_one()
    #     if self.status != "paid":
    #         raise UserError(_("You can't assign a room if it's not paid."))
    #     room_as_superuser = self.env['hostel.room'].sudo()
    #
    #     category = self.env['hostel.room.category'].sudo().search([
    #         ('name', '=', 'Luxury')
    #     ])
    #
    #     room_rec = room_as_superuser.create({
    #         "name": "Room A-103",
    #         "room_num": "103",
    #         "floor_num": 1,
    #         "category_id": category.id,
    #         "hostel_id": self.hostel_id.id,
    #         "student_per_room": 1,
    #     })

    def action_remove_room(self):
        if self.env.context.get("is_hostel_room"):
            self.room_id = False
