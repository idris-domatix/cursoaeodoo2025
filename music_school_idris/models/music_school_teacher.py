from odoo import models, fields

class MusicSchoolTeacher(models.Model):
    _name = 'music.school.teacher'
    _description = 'Music School Teacher'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Integer(string='Phone Number')
    level = fields.Selection(
        selection=[
            ('none', 'None'),
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        string='Level',
        default='none',
    )