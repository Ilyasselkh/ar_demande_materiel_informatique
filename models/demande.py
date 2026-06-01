from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ARITDemande(models.Model):
    _name = "ar.it.demande"
    _description = "Demande matériel informatique"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Référence", default="Nouveau", readonly=True, copy=False)
    state = fields.Selection(
        [
            ("new", "Nouvelle"),
            ("n1", "Validation N+1"),
            ("processing", "Traitement"),
            ("borrowed", "Emprunté"),
            ("delivered", "Livrée"),
            ("refused", "Refusée"),
        ],
        string="Statut",
        default="new",
        tracking=True,
        required=True,
    )

    def _default_employee(self):
        return self.env["hr.employee"].search(
            [("user_id", "=", self.env.user.id)],
            limit=1
        )

    demandeur_id = fields.Many2one(
        "hr.employee",
        string="Demandeur",
        default=_default_employee,
        readonly=True,
        tracking=True,
    )

    department_id = fields.Many2one(
        "hr.department",
        string="Département",
        related="demandeur_id.department_id",
        store=True,
        readonly=True,
        tracking=True,
    )

    manager_n1_id = fields.Many2one(
        "hr.employee",
        string="Manager N+1",
        related="demandeur_id.parent_id",
        store=True,
        readonly=True,
        tracking=True,
    )

    expression_besoin = fields.Selection([
        ("nouveau", "Nouveau besoin"),
        ("remplacement", "Remplacement"),
        ("emprunter", "Emprunter"),
    ], string="Expression de besoin", required=True, tracking=True)

    date_remplacement = fields.Date(string="Date de remplacement", tracking=True)

    date_besoin = fields.Date(string="Date de besoin", tracking=True)

    periode_from = fields.Date(string="Du", tracking=True)
    periode_to = fields.Date(string="Au", tracking=True)

    @api.onchange("expression_besoin")
    def _onchange_expression_besoin(self):
        for rec in self:
            if rec.expression_besoin == "nouveau":
                rec.date_remplacement = False
                rec.periode_from = False
                rec.periode_to = False
            elif rec.expression_besoin == "remplacement":
                rec.date_besoin = False
                rec.periode_from = False
                rec.periode_to = False
            elif rec.expression_besoin == "emprunter":
                rec.date_besoin = False
                rec.date_remplacement = False

    @api.constrains("expression_besoin", "date_besoin", "date_remplacement", "periode_from", "periode_to")
    def _check_expression_besoin_fields(self):
        for rec in self:
            if rec.expression_besoin == "nouveau" and not rec.date_besoin:
                raise ValidationError(_("Veuillez renseigner la Date de besoin (Nouveau besoin)."))

            if rec.expression_besoin == "remplacement" and not rec.date_remplacement:
                raise ValidationError(_("Veuillez renseigner la Date de remplacement (Remplacement)."))

            if rec.expression_besoin == "emprunter":
                if not rec.periode_from or not rec.periode_to:
                    raise ValidationError(_("Veuillez renseigner la période d'emprunt (Du/Au)."))

    @api.constrains("periode_from", "periode_to")
    def _check_periode(self):
        for rec in self:
            if rec.periode_from and not rec.periode_to:
                raise ValidationError(_("Si vous renseignez 'Du', vous devez renseigner 'Au'."))
            if rec.periode_to and not rec.periode_from:
                raise ValidationError(_("Si vous renseignez 'Au', vous devez renseigner 'Du'."))
            if rec.periode_from and rec.periode_to and rec.periode_to < rec.periode_from:
                raise ValidationError(_("La date 'Au' doit être supérieure ou égale à la date 'Du'."))

    line_ids = fields.One2many(
        "ar.it.demande.line",
        "demande_id",
        string="Matériels demandés",
        copy=True
    )

    commentaire = fields.Text(string="Commentaire", tracking=True)

    attachment_ids = fields.Many2many(
        "ir.attachment",
        "ar_it_demande_ir_attachment_rel",
        "demande_id",
        "attachment_id",
        string="Pièces jointes",
        tracking=True,
    )

    can_approve_n1 = fields.Boolean(
        string="Peut valider N+1",
        compute="_compute_can_approve_n1",
    )
    
    is_requester = fields.Boolean(
        string="Est le demandeur",
        compute="_compute_is_requester",
    )

    def _compute_is_requester(self):
        user = self.env.user
        for rec in self:
            rec.is_requester = bool(rec.demandeur_id and rec.demandeur_id.user_id and rec.demandeur_id.user_id.id == user.id)

    def _compute_can_approve_n1(self):
        user = self.env.user
        for rec in self:
            rec.can_approve_n1 = bool(
                rec.manager_n1_id
                and rec.manager_n1_id.user_id
                and rec.manager_n1_id.user_id.id == user.id
            )
    
    # =========================
    # EMAILS WORKFLOW
    # =========================
    def _clean_header(self, value):
        if not value:
            return False
        return str(value).replace("\n", "").replace("\r", "").strip()

    def _get_employee_email(self, emp):
        """Retourne l'email d'un hr.employee (via user/partner)"""
        if not emp:
            return False
        emp = emp.sudo()
        user = emp.user_id
        email = False
        if user:
            email = user.partner_id.email or user.email
        return self._clean_header(email) if email else False

    def _get_demandeur_email(self):
        self.ensure_one()
        return self._get_employee_email(self.demandeur_id)

    def _get_manager_n1_email(self):
        self.ensure_one()
        return self._get_employee_email(self.manager_n1_id)

    def _get_traiteurs_emails(self):
        """Emails des personnes paramétrées dans ar.it.traiteur (disponibles)"""
        self.ensure_one()
        emails = set()
        traiteurs = self.env["ar.it.traiteur"].sudo().search([("is_available", "=", True)])
        for t in traiteurs:
            email = self._get_employee_email(t.employee_id)
            if email:
                emails.add(email)
        return list(emails)

    def _send_template(self, xmlid, email_to_list):
        """Envoi mail template à une liste d'emails."""
        self.ensure_one()
        template = self.env.ref(xmlid, raise_if_not_found=False)
        if not template:
            return

        recipients = [self._clean_header(e) for e in (email_to_list or [])]
        recipients = [e for e in recipients if e]
        if not recipients:
            return

        email_values = {
            "email_to": self._clean_header(",".join(recipients)),
            "reply_to": self._clean_header(self.env.user.partner_id.email or self.env.user.email or ""),
        }
        template.send_mail(self.id, force_send=True, email_values=email_values)

    def _send_on_state_change(self, old_state, new_state):
        """Règles emails selon ton besoin."""
        self.ensure_one()

        # 1) Création => mail au manager N+1
        if old_state in (False, None) and new_state == "new":
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_new_to_manager",
                [self._get_manager_n1_email()],
            )
            return

        # 2) Validation N+1 => (n1 -> processing)
        if old_state == "n1" and new_state == "processing":
            # 2.1 notifier demandeur (validée)
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_approved_to_demandeur",
                [self._get_demandeur_email()],
            )
            # 2.2 notifier traiteurs (à traiter)
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_processing_to_traiteurs",
                self._get_traiteurs_emails(),
            )
            return

        # 3) Livrée => notifier demandeur
        if new_state == "delivered":
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_delivered_to_demandeur",
                [self._get_demandeur_email()],
            )
            return

        # 4) Emprunté => notifier demandeur
        if new_state == "borrowed":
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_borrowed_to_demandeur",
                [self._get_demandeur_email()],
            )
            return

        # 5) Refusée => notifier demandeur
        if new_state == "refused":
            self._send_template(
                "ar_demande_materiel_informatique.mail_template_it_refused_to_demandeur",
                [self._get_demandeur_email()],
            )
            return

    @api.model_create_multi
    def create(self, vals_list):
        employee_model = self.env["hr.employee"]
        sequence_model = self.env["ir.sequence"]
        current_user = self.env.user

        emp = employee_model.search([("user_id", "=", current_user.id)], limit=1)

        for vals in vals_list:
            if emp:
                vals.setdefault("demandeur_id", emp.id)

            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = sequence_model.next_by_code("ar.it.demande") or "DEM"

        records = super().create(vals_list)

        for rec in records:
            if not rec.line_ids:
                raise ValidationError(_("Veuillez ajouter au moins une ligne (Matériel / Quantité)."))
            rec._send_on_state_change(False, rec.state)

        return records
    
    def write(self, vals):
        old_states = {rec.id: rec.state for rec in self}
        res = super().write(vals)

        if "state" in vals:
            for rec in self:
                old_state = old_states.get(rec.id)
                new_state = rec.state
                if old_state != new_state:
                    rec._send_on_state_change(old_state, new_state)

        return res

    @api.constrains("line_ids")
    def _check_lines(self):
        for rec in self:
            if not rec.line_ids:
                raise ValidationError(_("La demande doit contenir au moins une ligne."))
            for l in rec.line_ids:
                if l.quantity <= 0:
                    raise ValidationError(_("La quantité doit être supérieure à 0."))

    # --- Actions workflow ---
    def action_submit_n1(self):
        for rec in self:
            if rec.state != "new":
                continue

            
            # Validation période emprunt seulement si "emprunter"
            if rec.expression_besoin == "emprunter":
                if not rec.periode_from or not rec.periode_to:
                    raise ValidationError(_("Veuillez renseigner la période d'emprunt (Du/Au) avant de soumettre."))
                if rec.periode_to and not rec.periode_from:
                    raise ValidationError(_("Veuillez renseigner la date 'Du' avant de soumettre."))

            rec.state = "n1"

    def action_approve_n1(self):
        for rec in self:
            if rec.state != "n1":
                continue

            # Sécurité: seul le manager N+1 du demandeur peut valider
            if not (
                rec.manager_n1_id
                and rec.manager_n1_id.user_id
                and rec.manager_n1_id.user_id.id == self.env.user.id
            ):
                raise ValidationError(_("Vous n'êtes pas autorisé à valider cette demande (N+1)."))

            rec.state = "processing"

    def _check_traitement_group(self):
        if not self.env.user.has_group("ar_demande_materiel_informatique.group_ar_it_traitement"):
            raise ValidationError(_("Vous n'avez pas l'accès au traitement."))

    def action_close_processing(self):
        self._check_traitement_group()
        for rec in self:
            if rec.state != "processing":
                continue

            # Si une période est renseignée => Emprunté, sinon => Livrée
            if rec.periode_from and rec.periode_to:
                rec.state = "borrowed"
            else:
                rec.state = "delivered"

    def action_refuse(self):
        # Refuser est réservé au groupe Traitement
        self._check_traitement_group()
        for rec in self:
            if rec.state in ("received", "refused"):
                continue
            rec.state = "refused"


class ARITDemandeLine(models.Model):
    _name = "ar.it.demande.line"
    _description = "Ligne demande matériel"
    _order = "id asc"

    demande_id = fields.Many2one("ar.it.demande", string="Demande", required=True, ondelete="cascade")
    materiel_id = fields.Many2one("ar.it.materiel", string="Matériel", required=True)
    quantity = fields.Integer(string="Quantité", required=True, default=1)