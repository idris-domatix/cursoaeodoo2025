from multiprocessing import context

from odoo import models, fields, Command, api
from odoo.exceptions import ValidationError

class MusicSchoolCourse(models.Model):
    _name = 'music.school.course'
    _description = 'Music School Course'

    name = fields.Char(string='Course Name', copy=False)
    description = fields.Text(string='Course Description', company_dependent=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In progress'),
        ('done', 'Done'),
    ], 
    string='State',
    default='draft',
    group_expand='group_expand_state'
    )
    active = fields.Boolean(string='Active', default=True)
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
        relation='music_school_course_student_rel',
        column1='course_id',
        column2='student_id',
        string='Students',
        help='Students enrolled in the course',
    )

    course_ids = fields.Many2many(
        comodel_name='music.school.course',
        relation='music_school_course_student_rel',
        column1='student_id',
        column2='course_id',
        string='Courses',
        help='Courses the student is enrolled in'
    )

    duration_days = fields.Integer(
        string='Duration (days)',
        compute='_compute_duration_days',
        store=True,
    )
    exam_ids = fields.One2many(
    comodel_name='music.school.exam',
    inverse_name='course_id',
    string='Exams'
    )
    exam_count = fields.Integer(
        string='Exam Count',
        compute='_compute_exam_count',
        store=True,
    )
    lecture_ids = fields.One2many(
        comodel_name='music.school.lecture',
        inverse_name='course_id',
        string='Lectures'
    )
    lecture_count = fields.Integer(
        string='Lecture Count',
        compute='_compute_lecture_count',
        store=True,
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='The company associated with this course',
    )
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Course name must be unique.'),
    ]

    _sql_constraints = [
        ('classroom_name_unique', 'UNIQUE(name)', 'Course name must be unique.')]
    
    def action_view_lectures(self):
        return {
            'name': 'Lectures',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.lecture',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id},
        }

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

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days + 1
            else:
                record.duration_days = 0

    def action_finish_lecture(self):
        for record in self:
            record.state = 'done'
            lectures = self.env['music.school.lecture'].search([('course_id', '=', record.id)])
            lectures.write({'state': 'completed'})


    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError("Capacity must be a positive integer.")

    def action_view_exams(self):
        return {
            'name': 'Exams',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.exam',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id},
        }
    
    @api.depends('exam_ids')
    def _compute_exam_count(self):
        for record in self:
            record.exam_count = len(record.exam_ids)

    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise ValidationError("End date cannot be before start date.")
            
    @api.depends('lecture_ids')
    def _compute_lecture_count(self):
        for record in self:
            record.lecture_count = len(record.lecture_ids)

    def action_finish_courses(self):
        courses = self.env['music.school.course'].search([('state', 'in', ['draft','progress'])])
        for course in courses:
            if course.end_date and course.end_date < fields.Date.today():
                course.state = 'done'

    def action_print_report(self):
        return self.env.ref('music_school_idris.action_report_music_school_course').report_action(self)