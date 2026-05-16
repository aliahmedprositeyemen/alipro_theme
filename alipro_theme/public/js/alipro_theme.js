
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

	// Safe CSS property generator
	const rule = (property, value, fallback = "") => {
		let final_val = value || fallback;
		if (final_val) {
			return `${property}: ${final_val} !important;`;
		}
		return "";
	};

	// Frappe v16 uses Bootstrap 5 and native CSS variables – selectors updated accordingly
	style.innerHTML = `
		:root, [data-theme="light"], [data-theme="dark"] {
			/* Sidebar overrides */
			${rule("--sidebar-hover-color", theme.sidebar_hover_background_color, theme.sidebar_active_background_color)}
			${rule("--sidebar-active-color", theme.sidebar_active_background_color)}
			${rule("--sidebar-select-color", theme.sidebar_active_background_color)}
			
			/* Generic Overrides */
			${rule("--bg-color", theme.body_background_color, "var(--bg-color)")}
			${rule("--fg-color", theme.main_body_content_box_background_color, "var(--fg-color)")}
		}

		/* ── Navbar ── */
		.navbar {
			${rule("background-color", theme.navbar_color)}
		}
		.navbar .nav-link,
		.navbar .navbar-brand,
		.navbar .navbar-nav .nav-link {
			${rule("color", theme.navbar_text_color)}
		}

		/* ── Primary Button ── */
		.btn-primary,
		.btn-primary:active {
			${rule("background-color", theme.button_background_color)}
			${rule("border-color", theme.button_background_color)}
			${rule("color", theme.button_text_color)}
		}
		.btn-primary:hover {
			${rule("background-color", theme.button_hover_background_color)}
			${rule("border-color", theme.button_hover_background_color)}
			${rule("color", theme.button_hover_text_color)}
		}

		/* ── Secondary Button ── */
		.btn-secondary, .btn-default {
			${rule("background-color", theme.secondary_button_background_color)}
			${rule("color", theme.secondary_button_text_color)}
		}

		/* ── Login Page ── */
		.for-login, .login-page {
			${rule("background-color", theme.login_page_background_color)}
		}
		.for-login .btn-primary, .login-page .btn-primary {
			${rule("background-color", theme.login_button_background_color)}
			${rule("border-color", theme.login_button_background_color)}
			${rule("color", theme.login_button_text_color)}
		}

		/* ── Main Body ── */
		body {
			${rule("background-color", theme.body_background_color)}
		}
		.page-container, .layout-main-section, .page-wrapper {
			${rule("background-color", theme.main_body_content_box_background_color)}
		}

		/* ── Tables ── */
		.dt-header .dt-cell__content {
			${rule("background-color", theme.table_head_background_color)}
			${rule("color", theme.table_head_text_color)}
		}
		.dt-row .dt-cell__content {
			${rule("background-color", theme.table_body_background_color)}
			${rule("color", theme.table_body_text_color)}
		}

		/* ── Inputs ── */
		.form-control, .input-with-feedback {
			${rule("background-color", theme.input_background_color)}
			${rule("color", theme.input_text_color)}
			${rule("border-color", theme.input_border_color)}
		}
		.control-label,
		label.control-label {
			${rule("color", theme.input_label_color)}
		}

		/* ── Widgets / Number Cards ── */
		.widget,
		.number-card {
			${rule("background-color", theme.number_card_background_color)}
			${rule("color", theme.number_card_text_color)}
		}

		/* ── Sidebar (Workspace / Desk) ── */
		.body-sidebar-container, .body-sidebar {
			${rule("background-color", theme.sidebar_background_color)}
		}

		.body-sidebar-container .sidebar-item-label,
		.body-sidebar-container .sidebar-item-icon svg {
			${rule("color", theme.sidebar_text_color)}
			${rule("fill", theme.sidebar_text_color)}
			${rule("stroke", theme.sidebar_text_color)}
		}

		.body-sidebar-container .sidebar-item-container.is-selected,
		.body-sidebar-container .sidebar-item-container:hover {
			${rule("background-color", theme.sidebar_active_background_color)}
		}

		.body-sidebar-container .sidebar-item-container.is-selected .sidebar-item-label,
		.body-sidebar-container .sidebar-item-container:hover .sidebar-item-label,
		.body-sidebar-container .sidebar-item-container.is-selected .sidebar-item-icon svg,
		.body-sidebar-container .sidebar-item-container:hover .sidebar-item-icon svg {
			${rule("color", theme.sidebar_active_text_color)}
			${rule("fill", theme.sidebar_active_text_color)}
			${rule("stroke", theme.sidebar_active_text_color)}
		}

		/* ── Page Head ── */
		.page-head, .page-header {
			${rule("background-color", theme.page_head_background_color)}
			${rule("color", theme.page_head_text_color)}
		}
		.page-head .title-text, .page-title h6 {
			${rule("color", theme.page_head_text_color)}
		}

		/* ── Modals / Dialogs ── */
		.modal-content, .modal-dialog .modal-content {
			${rule("background-color", theme.modal_background_color)}
			${rule("color", theme.modal_text_color)}
		}
		.modal-header, .modal-dialog .modal-header {
			${rule("background-color", theme.modal_header_background_color)}
		}
		.modal-title {
			${rule("color", theme.modal_text_color)}
		}

		/* ── Dropdowns / Awesomeplete menus ── */
		.dropdown-menu,
		.awesomplete > ul {
			${rule("background-color", theme.dropdown_background_color)}
		}
		.dropdown-menu > li > a,
		.dropdown-item,
		.awesomplete > ul > li > a {
			${rule("color", theme.dropdown_text_color)}
		}
		.dropdown-menu > li > a:hover,
		.dropdown-item:hover,
		.awesomplete > ul > li > a:hover,
		.awesomplete > ul > li:hover,
		.awesomplete > ul > li[aria-selected="true"] {
			${rule("background-color", theme.dropdown_hover_background_color)}
			${rule("color", theme.dropdown_text_color)}
		}
	`;
	document.head.appendChild(style);
}
