from odoo import models, fields, api

class MusicSchoolStudent(models.Model):
    _name = "music.school.student"
    _description = "Students"

    active = fields.Boolean(string ="Active")
    name = fields.Char(string = "Name", required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        help='The partner associated with this student'
    )
    email = fields.Char(string = "Email")
    phone = fields.Char(string="Phone", related='partner_id.phone', store=True, readonly=False)
    birthdate = fields.Date(string="BirthDate")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string="Responsible",
        help="The user responsible for this student"
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
