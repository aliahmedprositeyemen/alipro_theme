
frappe.provide("alipro_theme");

frappe.call({
    method: "alipro_theme.api.get_theme_settings",
    callback: function (r) {
        if (r.message) {
            applyTheme(r.message);
        }
    }
});

function applyTheme(theme) {
    let style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = `
        /* Navbar */
        .navbar {
            background-color: ${theme.navbar_color || ''} !important;
        }
        .navbar .navbar-nav .nav-link, .navbar .navbar-brand {
            color: ${theme.navbar_text_color || ''} !important;
        }

        /* Primary Button */
        .btn-primary, .btn-primary:active {
            background-color: ${theme.button_background_color || ''} !important;
            border-color: ${theme.button_background_color || ''} !important;
        }
        .btn-primary span, .btn-primary:active span {
            color: ${theme.button_text_color || ''} !important;
        }
        .btn-primary:hover {
            background-color: ${theme.button_hover_background_color || ''} !important;
            border-color: ${theme.button_hover_background_color || ''} !important;
        }
        .btn-primary:hover span {
            color: ${theme.button_hover_text_color || ''} !important;
        }

        /* Secondary Button */
        .btn-default {
            background-color: ${theme.secondary_button_background_color || ''} !important;
            color: ${theme.secondary_button_text_color || ''} !important;
        }
        
        /* Login Page */
        .login-page {
            background-color: ${theme.login_page_background_color || ''} !important;
        }
        .login-page .btn-primary {
            background-color: ${theme.login_button_background_color || ''} !important;
            border-color: ${theme.login_button_background_color || ''} !important;
        }
        .login-page .btn-primary {
             color: ${theme.login_button_text_color || ''} !important;
        }

        /* Main Body */
        body {
            background-color: ${theme.body_background_color || ''} !important;
        }
        .page-container {
             background-color: ${theme.main_body_content_box_background_color || ''} !important;
        }
        
        /* Tables */
        .table thead th {
             background-color: ${theme.table_head_background_color || ''} !important;
             color: ${theme.table_head_text_color || ''} !important;
        }
        .table tbody td {
             background-color: ${theme.table_body_background_color || ''} !important;
             color: ${theme.table_body_text_color || ''} !important;
        }

        /* Inputs */
        .form-control {
            background-color: ${theme.input_background_color || ''} !important;
            color: ${theme.input_text_color || ''} !important;
            border-color: ${theme.input_border_color || ''} !important;
        }
        .form-group label {
            color: ${theme.input_label_color || ''} !important;
        }

        /* Widgets */
        .widget {
            background-color: ${theme.number_card_background_color || ''} !important;
            color: ${theme.number_card_text_color || ''} !important;
        }
    `;
    document.head.appendChild(style);
}
