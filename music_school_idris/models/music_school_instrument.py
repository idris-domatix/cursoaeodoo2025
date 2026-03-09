from odoo import models, fields, api

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
        string = "Family Name",
        required=True,
    ) 
    description = fields.Text(string="Description")
    maintenance_date = fields.Date(string="Last Maintenance Date", help="The date when the instrument was last maintained")

    repaired = fields.Boolean(string="Repaired", compute="_compute_repaired", inverse="_set_is_repaired",store=True)

    def action_set_maintenance_date(self):
        for record in self:
            record.maintenance_date = fields.Date.today()
    @api.depends('maintenance_date')
    def _compute_repaired(self):
        for record in self:
            record.repaired = bool(record.maintenance_date)

    def _set_is_repaired(self):
        for record in self:
            if record.repaired:
                record.maintenance_date = fields.Date.today()
            else:
                record.maintenance_date = False
                    