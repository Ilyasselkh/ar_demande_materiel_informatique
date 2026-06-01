from odoo import models, fields

class ARITTraiteur(models.Model):
    _name = "ar.it.traiteur"
    _description = "Personnes qui traite"
    _rec_name = "employee_id"
    _order = "id desc"

    employee_id = fields.Many2one("hr.employee", string="Employé", required=True)

    is_available = fields.Boolean(string="Disponible", default=True)