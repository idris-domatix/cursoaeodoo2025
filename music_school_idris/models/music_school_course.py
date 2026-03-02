from odoo import models, fields, Command

class MusicSchoolCourse(models.Model):
    _name = 'music.school.course'
    _description = 'Music School Course'

    name = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In progress'),
        ('done', 'Done'),
    ], 
    string='State',
    default='draft',
    group_expand='group_expand_state'
    )

    teacher_id = fields.Many2one('music.school.teacher', string='Teacher')

    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument',
        string='Instrument',
        help='Instrument associated with the course',
    )
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
    start_date = fields.Date(
        string='Starting Date',
        default=fields.Date.context_today,
    )
    end_date = fields.Date(
        string='End Date',
    )
    capacity = fields.Integer(
        string='Capacity',
        help='Maximum number of students in the course',
    )

    color = fields.Integer(
        string='Color',
        help='Color for kanban view'
        )
    
    student_ids = fields.Many2many(
        comodel_name='music.school.student',
        string='Students',
        help='Students enrolled in the course',
    )

    def action_draft(self):
        self.state = 'draft'

    def action_in_progress(self):
        self.state = 'progress'
    
    def action_done(self):
        self.state = 'done'

    def group_expand_state(self, states, domain):
        return [key for key, val in type(self).state.selection]
    
    def create_lecture(self):
        vals = {
            'course_id': self.id,
            'teacher_id': self.teacher_id.id,
        }   
        lecture =self.env['music.school.lecture'].create(vals)

    def assign_students(self):
        for record in self:
            students = self.env['music.school.student'].search([])
            if students:
                record.student_ids = [(6, 0, students.ids)]