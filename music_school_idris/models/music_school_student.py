from odoo import models, fields, api

class MusicSchoolStudent(models.Model):
    _name = "music.school.student"
    _description = "Students"

    def get_user(self):
        return self.env.user.id
    
    active = fields.Boolean(string ="Active")
    name = fields.Char(string = "Name", required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        help='The partner associated with this student',
        copy=False
    )
    
    email = fields.Char(
        string = "Email" 
        )
    phone = fields.Char(string="Phone", related='partner_id.phone', store=True, readonly=False, copy=False)
    birthdate = fields.Date(string="BirthDate")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string="Responsible",
        help="The user responsible for this student",
        default = lambda self: self.env.user
        )
    active = fields.Boolean(default=True)
    notes = fields.Html(
        string="Notes",
        help ="Additional information about the student, such as preferences or special needs.",
        copy=False
        )
    
    reference = fields.Char(
        string="Reference"
        )
    
    attendance_count = fields.Integer(
        string="Attendance Count",
        compute="_compute_attendance_count"
    )

    @api.onchange('partner_id')
    def _onchange_email(self):
        if self.partner_id:
            self.email =self.partner_id.email
        else:
            self.email = ' '
        
    def generate_reference(self):
        for record in self:
            record.reference = f"ESC-{record.id}{record.name}"
            
    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = fields.Date.today()
                age = today.year - record.birthdate.year - ((today.month, today.day) < (record.birthdate.month, record.birthdate.day))
                record.age = age
            else:
                record.age = 0

    def action_view_attendance(self):
        return {
            'name': 'Attendance',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.lecture.attendance',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }

    def _compute_attendance_count(self):
        for record in self:
            record.attendance_count = self.env['music.school.lecture.attendance'].search_count([('student_id', '=', record.id)])