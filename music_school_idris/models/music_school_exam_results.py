from odoo import models, fields, api

class MusicSchoolExamResults(models.Model):
    _name = 'music.school.exam.result'
    _description = 'Music School Exam Result'

    student_id = fields.Many2one('music.school.student', string='Student')
    exam_id = fields.Many2one('music.school.exam', string='Exam')
    score = fields.Float(string='Score')
    
    passed = fields.Boolean(string='Passed', compute='_compute_passed', store=True)

    comments = fields.Text(string='Teacher Comments')

    student_ids = fields.Many2many(
        comodel_name='music.school.student',
        string='Students',
        help='Students associated with the exam result',
        related='exam_id.course_id.student_ids'
    )
    @api.depends('score', 'exam_id.minimum_score')
    def _compute_passed(self):
        for record in self:
            if record.exam_id:
                record.passed = (record.score or 0.0) >= (record.exam_id.minimum_score or 0.0)
            else:
                record.passed = False