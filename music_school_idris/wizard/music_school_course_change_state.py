from odoo import models, fields, api

class MusicSchoolCourseChangeState(models.TransientModel):
    _name = 'music.school.course.change.state'
    _description = 'Wizard to change the state of a music school course'
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In progress'),
        ('done', 'Done'),
    ], 
    string='State',
    )

    def action_change_state(self):
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            course = self.env['music.school.course'].browse(active_ids)
            course.write({'state': self.state})