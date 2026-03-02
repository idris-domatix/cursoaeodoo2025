from odoo import models, fields

class MusicSchoolInstrumentFamily(models.Model):
    _name = 'music.school.instrument.family'
    _description = 'Instruments'

    name = fields.Char(string = "Name", required=True, translate=True)
    