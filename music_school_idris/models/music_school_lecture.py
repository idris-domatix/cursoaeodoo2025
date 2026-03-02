from odoo import models, fields

class MusicSchoolLecture(models.Model):
    _name = 'music.school.lecture'
    _description = 'Music School Lecture'

    name = fields.Char(string='Lecture Name')
    teacher_id = fields.Many2one('music.school.teacher', string='Teacher')
    course_id = fields.Many2one('music.school.course', string='Course')
    classroom_id = fields.Many2one('music.school.classroom', string='Classroom')
    date = fields.Datetime(string='Date')
    duration = fields.Float(string='Duration (hours)')
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        selection=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ],
    string='State',
    default='scheduled',
    group_expand='group_expand_state'
    )
    color = fields.Integer(string='Color', help='Color for kanban view')

    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]