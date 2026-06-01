/** @odoo-module **/

const FORM_SELECTOR = ".o_form_view.ar_it_demande_form";

function animateForm(form) {
    if (!form || form.dataset.arItAnimated === "1") {
        return;
    }
    form.dataset.arItAnimated = "1";

    const sheet = form.querySelector(".ar_sortie_caisse_sheet");
    if (sheet) {
        sheet.classList.add("ar_sc_ready");
    }

    form.querySelectorAll(".ar_sortie_caisse_title, .ar_sortie_caisse_panel").forEach((element) => {
        element.classList.add("ar_sc_reveal");
    });

    const amount = form.querySelector(".ar_sortie_caisse_amount");
    if (!amount) {
        return;
    }

    amount.addEventListener("animationend", (event) => {
        if (event.animationName === "arScAmountFlash") {
            amount.classList.remove("ar_sc_amount_flash");
        }
    });

    let lastValue = amount.textContent.trim();
    const observer = new MutationObserver(() => {
        const value = amount.textContent.trim();
        if (value === lastValue) {
            return;
        }
        lastValue = value;
        amount.classList.remove("ar_sc_amount_flash");
        window.requestAnimationFrame(() => amount.classList.add("ar_sc_amount_flash"));
    });

    observer.observe(amount, {
        childList: true,
        subtree: true,
        characterData: true,
    });
}

function scan() {
    document.querySelectorAll(FORM_SELECTOR).forEach(animateForm);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
} else {
    scan();
}

if (document.body) {
    const bodyObserver = new MutationObserver(scan);
    bodyObserver.observe(document.body, {
        childList: true,
        subtree: true,
    });
}
