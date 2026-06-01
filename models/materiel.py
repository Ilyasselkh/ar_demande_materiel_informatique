from odoo import models, fields, api, _

class ARMateriel(models.Model):
    _name = "ar.it.materiel"
    _description = "Matériel informatique"
    _rec_name = "description"
    _order = "id desc"

    description = fields.Char(string="Description", required=True)
    is_available = fields.Boolean(string="Disponible", default=True)

    def write(self, vals):
        res = super().write(vals)

        
        if "is_available" in vals and vals["is_available"] is False:
            lines = self.env["ar.it.demande.line"].search([
                ("materiel_id", "in", self.ids),
                ("demande_id.state", "=", "new"),   
            ])

            
            demandes = lines.mapped("demande_id")
            lines.unlink()

            
            for d in demandes:
                d.message_post(body=_("Une ligne a été supprimée car le matériel est devenu indisponible."))

        return res