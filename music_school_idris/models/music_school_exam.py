from odoo import models, fields, api

class MusicSchoolExam(models.Model):
    _name = 'music.school.exam'
    _description = 'Music School Exam'

    name = fields.Char(string='Exam Name')
    course_id = fields.Many2one('music.school.course', string='Course')
    date = fields.Datetime(
    string='Date & Time',
    required=True,
    default=fields.Datetime.now
    )   
    instrument_id = fields.Many2one('music.school.instrument', string='Instrument')
    teacher_id = fields.Many2one('music.school.teacher', string='Examiner')
    minimum_score = fields.Float(string='Minimum Score')
    maximum_score = fields.Float(string='Maximum Score')
    state = fields.Selection(
    selection=[
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('finished', 'Finished'),
    ],
    string='State',
    default='draft',
    group_expand='_expand_states',
    )

    def _expand_states(self, states, domain, order=None):
        return [key for key, _ in self._fields['state'].selection]


    result_ids = fields.One2many(
        comodel_name='music.school.exam.result',
        inverse_name='exam_id',
        string='Exam Results',
        help='Results of the exam for each student'
    )

    color = fields.Integer(string='Color Index', default=0, help='Color index for kanban view')

    def assign_students(self):
        students = self.course_id.student_ids
        self.result_ids = [(0, 0, {'student_id': student.id}) for student in students]

    def action_finish_exams(self):
        exams = self.env['music.school.exam'].search([('state', 'in', ['draft','scheduled'])])
        for exam in exams:
            if exam.date < fields.Datetime.now():
                exam.state = 'finished'
    