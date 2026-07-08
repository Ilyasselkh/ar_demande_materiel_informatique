from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ARITDemandeConfirmWizard(models.TransientModel):
    _name = "ar.it.demande.confirm.wizard"
    _description = "Confirmation workflow demande IT"

    demande_id = fields.Many2one("ar.it.demande", string="Demande", required=True, readonly=True)
    action_key = fields.Selection(
        [
            ("submit_n1", "Soumettre N+1"),
            ("approve_n1", "Valider N+1"),
            ("approve_manager_it", "Valider Manager IT"),
            ("refuse_manager_it", "Refuser Manager IT"),
            ("close_processing", "Cloturer"),
            ("refuse", "Refuser"),
        ],
        string="Action",
        required=True,
        readonly=True,
    )
    title = fields.Char(string="Titre", readonly=True)
    message = fields.Char(string="Message", readonly=True)
    icon_text = fields.Char(string="Icone", readonly=True, default="OK")
    is_refusal = fields.Boolean(string="Refus", compute="_compute_is_refusal")
    refusal_reason = fields.Text(string="Motif de refus")

    @api.depends("action_key")
    def _compute_is_refusal(self):
        for wizard in self:
            wizard.is_refusal = wizard.action_key in ("refuse_manager_it", "refuse")

    def _get_confirmation_texts(self):
        return {
            "submit_n1": {
                "title": _("Confirmer la soumission"),
                "message": _("Voulez-vous vraiment soumettre cette demande au Manager N+1 ?"),
                "icon_text": "OK",
            },
            "approve_n1": {
                "title": _("Confirmer la validation"),
                "message": _("Voulez-vous vraiment valider cette demande ?"),
                "icon_text": "OK",
            },
            "approve_manager_it": {
                "title": _("Confirmer la validation"),
                "message": _("Voulez-vous vraiment valider cette demande ?"),
                "icon_text": "OK",
            },
            "refuse_manager_it": {
                "title": _("Confirmer le refus"),
                "message": _("Voulez-vous vraiment refuser cette demande ?"),
                "icon_text": "!",
            },
            "close_processing": {
                "title": _("Confirmer la cloture"),
                "message": _("Voulez-vous vraiment cloturer cette demande ?"),
                "icon_text": "OK",
            },
            "refuse": {
                "title": _("Confirmer le refus"),
                "message": _("Voulez-vous vraiment refuser cette demande ?"),
                "icon_text": "!",
            },
        }

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        action_key = values.get("action_key") or self.env.context.get("default_action_key")
        texts = self._get_confirmation_texts().get(action_key, {})
        values.update(
            {
                "title": texts.get("title", _("Confirmation")),
                "message": texts.get("message", _("Voulez-vous confirmer cette action ?")),
                "icon_text": texts.get("icon_text", "OK"),
            }
        )
        return values

    def action_confirm(self):
        self.ensure_one()
        if not self.demande_id or not self.action_key:
            raise ValidationError(_("Confirmation incomplete."))
        if self.is_refusal and not self.refusal_reason:
            raise ValidationError(_("Veuillez renseigner le motif de refus."))
        self.demande_id._execute_confirmed_workflow(self.action_key, self.refusal_reason)
        return {"type": "ir.actions.client", "tag": "reload"}
