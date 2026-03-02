from odoo import models, fields

class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instruments'

    name = fields.Char(string = "Name", required=True)
    family_id = fields.Many2one(
        comodel_name='music.school.instrument.family',
        string='Family',
        help='The family to which the instrument belongs'
    )
    family = fields.Selection(
        selection =[
            ('string', 'String'),
            ('wind', 'Wind'),
            ('percussion', 'Percussion'),
            ('keyboard', 'Keyboard'),
        ],
        string = "Family",
        required=True,
    ) 
    description = fields.Text(string="Description")
    maintenance_date = fields.Date(string="Last Maintenance Date", help="The date when the instrument was last maintained")

    def action_set_maintenance_date(self):
        for record in self:
            record.maintenance_date = fields.Date.today()