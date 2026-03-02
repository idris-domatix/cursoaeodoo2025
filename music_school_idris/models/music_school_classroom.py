from odoo import models, fields 

class MusicSchoolClassroom(models.Model):
    _name = 'music.school.classroom'
    _description = 'Music School Classroom'

    name = fields.Char(string='Classroom Name')
    capacity = fields.Integer(string='Capacity')
    location = fields.Char(string='Location')