from odoo import models, fields

class MusicSchoolLectureAttendance(models.Model):
    _name = 'music.school.lecture.attendance'
    _description = 'Music School Lecture Attendance'
    order = 'sequence, name desc'

    sequence = fields.Integer(
        string='Sequence', 
        help='Sequence number for ordering attendance records'
    )
    
    student_id = fields.Many2one(
        comodel_name='music.school.student',
        string='Student',
        required=True
    )

    lecture_id = fields.Many2one(
        comodel_name='music.school.lecture',
        string='Lecture'
    )

    is_present = fields.Boolean(string='Present')

    date = fields.Date(string='Date', help='Date of the attendance record')

    notes = fields.Text(string='Notes', help='Additional notes about the attendance')
