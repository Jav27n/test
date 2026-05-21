from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.translate import _

class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _rec_names_search = ['name', 'room_num', 'student_ids.name']

    name = fields.Char(string="Room Name", required=True)
    room_num = fields.Integer(string="Room No.")
    floor_num = fields.Integer(string="Floor No.")
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month", currency_field='currency_id')
    # cost_price = fields.Float('Room Cost')
    hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")

    student_ids = fields.One2many("hostel.student", "room_id",
                                  string="Students", help="Enter students")

    hostel_amenities_ids = fields.Many2many("hostel.amenities",
                                            "hostel_room_amenities_rel", "room_id", "amenitiy_id",
                                            string="Amenities", domain="[('active', '=', True)]",
                                            help="Select hostel room amenities")

    student_per_room = fields.Integer("Student Per Room",
                                      required=True, help="Students allocated per room")

    availability = fields.Float(compute="_compute_check_availability", store=True, string="Availability",
                                help="Room availability in hostel")

    state = fields.Selection([ ('draft', 'Unavailable'), ('available', 'Available'),
                               ('closed', 'Closed')], 'State', default="draft")

    category_id = fields.Many2one('hostel.room.category')

    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')

    remarks = fields.Text('Remarks')

    _sql_constraints = [("room_no_unique", "unique(room_num)", "Room number must be unique!")]

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'), ('available', 'closed'), ('closed', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')

    def update_room_no(self):
        self.ensure_one()
        self.room_num = "10"

    def find_room(self):
        domain = [
            '|',
            '&', ('name', 'ilike', 'Room 1'),
            ('room_num', 'ilike', '1'),
            '&', ('name', 'ilike', 'room 4'),
            ('room_num', 'ilike', '2')
        ]
        rooms = self.search(domain)
        print(rooms)

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
            return False
        return all_rooms.filtered(predicate)

    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        print(filtered_rooms.name)

    def filter_members_1(self):
        all_rooms = self.search([])
        filtered_rooms = self.get_members_names(all_rooms)
        print(filtered_rooms)

    @api.model
    def get_members_names(self, rooms):
        return rooms.mapped('student_ids.name')

    def filter_members_2(self):
        all_rooms = self.search([])
        filtered_rooms = self.sort_rooms_by_roomnum(all_rooms)
        print(filtered_rooms)

    @api.model
    def sort_rooms_by_roomnum(self, rooms):
        return rooms.sorted(key='room_num')


    def create(self, vals):
        # vals.cost_price = vals.rent_amount
        res = super(HostelRoom, self).create(vals)
        return res

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('rent_amount', "!=", False)],  # Domain
            ['category_id', 'rent_amount:avg'],  # Fields to access
            ['category_id']  # group_by
        )
        print(grouped_result)
        return grouped_result

    def action_get_average_cost(self):
        return self._get_average_cost()

    # @api.depends('name')
    # def _compute_display_name(self):
    #     result = []
    #     for room in self:
    #         if room.student_ids and room.student_ids.mapped('name')[0] != False:
    #             students = room.student_ids.mapped('name')
    #             name = '%s (%s)' % (room.name, ', '.join(students))
    #             result.append((room.id, name))
    #         else:
    #             name = 'demo'
    #             self.display_name = 'demo'
    #             result.append((room.id, name))
    #     return result

    # @api.depends('name', 'student_ids.name')
    # def _compute_display_name(self):
    #     for room in self:
    #         students = [s.name for s in room.student_ids if s.name]
    #         if students:
    #             room.display_name = f"{room.name} ({', '.join(students)})"
    #         else:
    #             room.display_name = room.name

    @api.depends('name', 'student_ids.name')
    def _compute_display_name(self):
        for room in self:
            if room.student_ids:
                students = room.student_ids.mapped('name')
                name = '%s (%s)' % (room.name, ', '.join(students))
                room.display_name = name
            else:
                room.display_name = room.name

    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = [] if args is None else args.copy()
    #     if not (name == '' and operator == 'ilike'):
    #         args += ['|', '|',
    #                  ('name', operator, name),
    #                  ('room_num', operator, name),
    #                  ('student_ids.name', operator, name)
    #                  ]
    #     return super(HostelRoom, self)._name_search(
    #         name=name, args=args, operator=operator,
    #         limit=limit, name_get_uid=name_get_uid)

    @api.model_create_multi
    def create(self, values):
        if not self.env.user.has_groups('my_hostel.group_hostel_manager'):
            for val in values:
                if val.get('remarks'):
                    raise UserError(
                        'You are not allowed to modify '
                        'remarks'
                    )
        return super(HostelRoom, self).create(values)

    def write(self, values):
        if not self.env.user.has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )
        return super(HostelRoom, self).write(values)

    def action_remove_room_members(self):
        for student in self.student_ids:
            student.with_context(is_hostel_room=True).action_remove_room()
