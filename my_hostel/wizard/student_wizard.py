from odoo import api, fields, models

class StudentWizard(models.TransientModel):
    _name = "student.wizard"

    name = fields.Char("Name", help="Provided Hostel Amenity")

    def action_print_report(self):
        print("Clicked..........!!!!")
