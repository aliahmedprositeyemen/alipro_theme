
frappe.provide("alipro_theme");

// -------------------------------------------------------
// Load theme settings and apply dynamic CSS on desk load
// -------------------------------------------------------
frappe.call({
    method: "alipro_theme.api.get_theme_settings",
    callback: function (r) {
        if (r.message) {
            applyTheme(r.message);
        }
    },
});

function applyTheme(theme) {
    // Remove any previously injected alipro style
    const existing = document.getElementById("alipro-dynamic-style");
    if (existing) existing.remove();

    const style = document.createElement("style");
    style.id = "alipro-dynamic-style";
    style.type = "text/css";

    // Frappe v16 uses Bootstrap 5 – selectors updated accordingly
    style.innerHTML = `
		/* ── Navbar ── */
		.navbar {
			background-color: ${theme.navbar_color || ""} !important;
		}
		.navbar .nav-link,
		.navbar .navbar-brand,
		.navbar .navbar-nav .nav-link {
			color: ${theme.navbar_text_color || ""} !important;
		}

		/* ── Primary Button ── */
		.btn-primary,
		.btn-primary:active {
			background-color: ${theme.button_background_color || ""} !important;
			border-color:     ${theme.button_background_color || ""} !important;
			color:            ${theme.button_text_color || ""} !important;
		}
		.btn-primary:hover {
			background-color: ${theme.button_hover_background_color || ""} !important;
			border-color:     ${theme.button_hover_background_color || ""} !important;
			color:            ${theme.button_hover_text_color || ""} !important;
		}

		/* ── Secondary Button (Bootstrap 5: btn-secondary replaces btn-default) ── */
		.btn-secondary {
			background-color: ${theme.secondary_button_background_color || ""} !important;
			color:            ${theme.secondary_button_text_color || ""} !important;
		}

		/* ── Login Page ── */
		.for-login {
			background-color: ${theme.login_page_background_color || ""} !important;
		}
		.for-login .btn-primary {
			background-color: ${theme.login_button_background_color || ""} !important;
			border-color:     ${theme.login_button_background_color || ""} !important;
			color:            ${theme.login_button_text_color || ""} !important;
		}

		/* ── Main Body ── */
		body {
			background-color: ${theme.body_background_color || ""} !important;
		}
		.page-container {
			background-color: ${theme.main_body_content_box_background_color || ""} !important;
		}

		/* ── Tables ── */
		.dt-header .dt-cell__content {
			background-color: ${theme.table_head_background_color || ""} !important;
			color:            ${theme.table_head_text_color || ""} !important;
		}
		.dt-row .dt-cell__content {
			background-color: ${theme.table_body_background_color || ""} !important;
			color:            ${theme.table_body_text_color || ""} !important;
		}

		/* ── Inputs (Bootstrap 5) ── */
		.form-control {
			background-color: ${theme.input_background_color || ""} !important;
			color:            ${theme.input_text_color || ""} !important;
			border-color:     ${theme.input_border_color || ""} !important;
		}
		.control-label,
		label.control-label {
			color: ${theme.input_label_color || ""} !important;
		}

		/* ── Widgets / Number Cards ── */
		.widget,
		.number-card {
			background-color: ${theme.number_card_background_color || ""} !important;
			color:            ${theme.number_card_text_color || ""} !important;
		}
	`;

    document.head.appendChild(style);
}
