from odoo import models, fields

class MusicSchoolStudent(models.Model):
    _name = "music.school.student"
    _description = "Students"

    active = fields.Boolean(string ="Active")
    name = fields.Char(string = "Name", required=True)
    email = fields.Char(string = "Email")
    phone = fields.Char(string="Phone")
    birthdate = fields.Date(string="BirthDate")
    age = fields.Integer(string="Age")
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string="Responsible",
        help="The user responsible for this student"
        )
    active = fields.Boolean(default=True)
    notes = fields.Html(
        string="Notes",
        help ="Additional information about the student, such as preferences or special needs."
        )
    
    reference = fields.Char(
        string="Reference"
        
        )
    def generate_reference(self):
        for record in self:
            record.reference = f"ESC-{record.id}{record.name}"
