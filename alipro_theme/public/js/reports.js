
frappe.provide("alipro_theme");

alipro_theme.print_custom_ledger = function (report) {
    let filters = report.get_values ? report.get_values() : report.filters;

    if (!filters.account && (!filters.party || (Array.isArray(filters.party) && filters.party.length === 0))) {
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
            }
        }
    });
};

// More robust way to add button to General Ledger
$(document).on('page-change', function () {
    setTimeout(() => {
        if (frappe.get_route() && frappe.get_route()[0] === 'query-report' && frappe.get_route()[1] === 'General Ledger') {
            let report = frappe.query_report;
            if (report && report.page && !report.page.has_inner_button(__("كشف حساب مخصص"))) {
                report.page.add_inner_button(__("كشف حساب مخصص"), function () {
                    alipro_theme.print_custom_ledger(report);
                }, __("Print"));
            }
        }
    }, 500); // Small delay to ensure report object is initialized
});

// Also try the standard events hook just in case
if (!frappe.query_report_events) {
    frappe.query_report_events = {};
}

frappe.query_report_events["General Ledger"] = {
    "onload": function (report) {
        if (!report.page.has_inner_button(__("كشف حساب مخصص"))) {
            report.page.add_inner_button(__("كشف حساب مخصص"), function () {
                alipro_theme.print_custom_ledger(report);
            }, __("Print"));
        }
    },
    "refresh": function (report) {
        if (!report.page.has_inner_button(__("كشف حساب مخصص"))) {
            report.page.add_inner_button(__("كشف حساب مخصص"), function () {
                alipro_theme.print_custom_ledger(report);
            }, __("Print"));
        }
    }
};
