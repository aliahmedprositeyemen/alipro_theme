
$(document).on('app_ready', function () {
    if (frappe.query_reports) {
        // We can't easily override the report definition directly if it's already loaded
        // but we can hook into the render event
    }
});

// Use a more robust way to intercept report rendering
var original_report_make = frappe.views.ReportView.prototype.make;
frappe.views.ReportView.prototype.make = function () {
    original_report_make.apply(this, arguments);
    if (this.report_name === "General Ledger") {
        this.page.add_inner_button(__("كشف حساب مخصص"), () => {
            alipro_theme.print_custom_ledger(this);
        }, __("Print"));
    }
};

// For Query Reports (Script Reports)
var original_query_report_make = frappe.views.QueryReport.prototype.make;
frappe.views.QueryReport.prototype.make = function () {
    original_query_report_make.apply(this, arguments);
    if (this.report_name === "General Ledger") {
        this.page.add_inner_button(__("كشف حساب مخصص"), () => {
            alipro_theme.print_custom_ledger(this);
        }, __("Print"));
    }
};

frappe.provide("alipro_theme");

alipro_theme.print_custom_ledger = function (report) {
    let filters = report.get_values ? report.get_values() : report.filters;

    if (!filters.account && (!filters.party || filters.party.length === 0)) {
        frappe.msgprint(__("الرجاء اختيار حساب أو عميل أولاً"));
        return;
    }

    frappe.call({
        method: "alipro_theme.overrides.general_ledger.get_custom_statement_html",
        args: {
            filters: filters
        },
        callback: function (r) {
            if (r.message) {
                var w = window.open();
                w.document.write(r.message);
                w.document.close();
                // Optionally auto-print
                // setTimeout(() => w.print(), 1000);
            }
        }
    });
};
