from odoo import models, fields

class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instruments'

    name = fields.Char(string = "Name", required=True)
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
    maintenance_date = fields.Date(string="Last Maintenance Date")

    def action_set_maintenance_date(self):
        for record in self:
            record.maintenance_date = fields.Date.today()