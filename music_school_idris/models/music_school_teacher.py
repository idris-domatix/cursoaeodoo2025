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

    courses_count = fields.Integer(
        string="Courses Count",
        compute="get_courses_count"
    )

    def get_courses_count(self):
        for teacher in self:
            teacher.courses_count = self.env['music.school.course'].search_count([('teacher_id', '=', teacher.id)])

    def action_view_courses(self):
        return {
        'name': 'Courses',
        'type': 'ir.actions.act_window',
        'res_model': 'music.school.course',
        'view_mode': 'list,form',
        'domain': [('teacher_id', '=', self.id)],
        }