from odoo import models, fields, api
from datetime import timedelta

class MusicSchoolLectureBatch(models.TransientModel):
    _name = 'music.school.lecture.batch'
    _description = 'Batch Lecture Creation'

    course_id = fields.Many2one(
        comodel_name='music.school.course',
        string='Course',
        required=True,
    )
    start_date = fields.Datetime(
        string='Starting Date',
        required=True
    )
    end_date = fields.Datetime(
        string='End Date',
        required=True   
    )

    def action_create_lectures(self):
        lecture_obj = self.env['music.school.lecture']
        current_date = self.start_date
        lecture = self.env['music.school.lecture']
        while current_date <= self.end_date:
            lecture |= lecture_obj.create({
                'course_id': self.course_id.id,
                'date': current_date,
            })
            current_date += timedelta(days=1)

        return {
            'name': 'Created Lectures',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.lecture',
            'view_mode': 'list,form',
            'domain': [('id', 'in', lecture.ids)],
            'target': 'current',
        }