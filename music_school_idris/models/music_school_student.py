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