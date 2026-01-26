
import frappe
from frappe import _
from erpnext.accounts.report.general_ledger.general_ledger import execute as gl_execute
from frappe.utils import formatdate, fmt_money, getdate, add_days, money_in_words
import json

@frappe.whitelist()
def get_custom_statement_html(filters):
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    # Ensure company is present
    if not filters.get("company"):
        filters["company"] = frappe.db.get_single_value("Global Defaults", "default_company")
        
    # Standard GL Logic
    columns, data = gl_execute(filters)
    
    if not data:
        return "<div style='text-align:center; padding:20px;'>لا توجد بيانات للفترة المحددة.</div>"

    company_doc = frappe.get_doc("Company", filters.get("company"))
    
    # Party details
    party_type = filters.get("party_type")
    party = filters.get("party")
    if isinstance(party, list) and len(party) > 0:
        party = party[0]
    
    party_name = ""
    if party and party_type:
        party_name = frappe.db.get_value(party_type, party, "customer_name" if party_type == "Customer" else "supplier_name") or party

    account = filters.get("account")
    if isinstance(account, list) and len(account) > 0:
        account = account[0]
    account_name = frappe.db.get_value("Account", account, "account_name") or account
    
    # Process data with translation awareness
    opening_balance = 0
    final_balance = 0
    total_debit = 0
    total_credit = 0
    table_rows = []
    
    # Translation keys used in ERPNext GL
    opening_label = f"'{_('Opening')}'"
    total_label = f"'{_('Total')}'"
    closing_label = f"'{_('Closing (Opening + Total)')}'"
    
    for d in data:
        acc_val = str(d.get("account") or "")
        if acc_val == opening_label or acc_val == "'Opening'":
            opening_balance = d.get("balance", 0)
        elif acc_val == total_label or acc_val == "'Total'":
            total_debit = d.get("debit", 0)
            total_credit = d.get("credit", 0)
        elif acc_val == closing_label or acc_val == "'Closing (Opening + Total)'":
            final_balance = d.get("balance", 0)
        elif d.get("posting_date"):
            table_rows.append(d)

    # Balance in words
    balance_in_words = money_in_words(abs(final_balance), company_doc.default_currency)
    balance_type = "عليكم" if final_balance > 0 else "لكم"
    
    # Arabic Currency labels
    currency_label = "ريال يمني" if company_doc.default_currency == "YER" else company_doc.default_currency

    html = f"""
    <div dir="rtl" style="font-family: 'Tahoma', 'Arial', sans-serif; padding: 15px; color: #000; background: white; max-width: 950px; margin: auto; border: 1px solid #000;">
        <!-- Header Container -->
        <div style="border: 2px solid #000; border-radius: 15px; padding: 10px; margin-bottom: 10px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="width: 33%; text-align: right; vertical-align: top;">
                        <h2 style="margin: 0; font-size: 18px;">SAM WiFi network System</h2>
                        <p style="margin: 2px 0; font-size: 14px;">Sna'a 50th ST</p>
                        <p style="margin: 2px 0; font-size: 14px;">770199558 - 773148552</p>
                    </td>
                    <td style="width: 34%; text-align: center; vertical-align: middle;">
                        <div style="font-size: 24px; font-weight: bold; border: 2px solid #000; display: inline-block; padding: 5px 15px; border-radius: 5px; margin-bottom: 5px;">SAM</div>
                        <h3 style="margin: 5px 0; font-size: 18px;">كشف حساب تحليلي</h3>
                        <p style="margin: 0; font-size: 12px;">من تاريخ: {formatdate(filters.from_date)} الى تاريخ: {formatdate(filters.to_date)}</p>
                    </td>
                    <td style="width: 33%; text-align: left; vertical-align: top;">
                        <h2 style="margin: 0; font-size: 18px;">شبكة سام اللاسلكية</h2>
                        <p style="margin: 2px 0; font-size: 14px;">اليمن ، صنعاء - شارع الخمسين</p>
                        <p style="margin: 2px 0; font-size: 14px;">770199558 - 773148552</p>
                    </td>
                </tr>
            </table>
        </div>

        <!-- Account Info -->
        <table style="width: 100%; margin-bottom: 5px; font-size: 14px; font-weight: bold;">
            <tr>
                <td style="text-align: right; color: red;">العملة: {currency_label}</td>
                <td style="text-align: left; color: brown;">رقم الحساب: {account or ""} اسم الحساب: {party_name or account_name}</td>
            </tr>
        </table>

        <!-- Main Ledger Table -->
        <table style="width: 100%; border-collapse: collapse; border: 2px solid #000; font-size: 13px;">
            <thead>
                <tr style="background: #e5e7eb; text-align: center;">
                    <th style="border: 1px solid #000; padding: 8px; width: 12%;">التاريخ</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 13%;">نوع المستند</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 10%;">المستند رقم</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 35%;">البيان</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 10%;">مدين</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 10%;">دائن</th>
                    <th style="border: 1px solid #000; padding: 8px; width: 10%;">الرصيد</th>
                </tr>
            </thead>
            <tbody>
                <!-- Opening Balance Row -->
                <tr style="font-weight: bold;">
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;"></td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;"></td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;"></td>
                    <td style="border: 1px solid #000; padding: 8px; font-size: 14px;">الرصيد الافتتاحي</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{fmt_money(abs(opening_balance)) if opening_balance > 0 else ""}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{fmt_money(abs(opening_balance)) if opening_balance < 0 else ""}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;"></td>
                </tr>
    """

    balance = opening_balance
    for row in table_rows:
        debit = row.get("debit", 0)
        credit = row.get("credit", 0)
        balance += (debit - credit)
        
        remark = row.get("remarks") or ""
        if "Against" in remark: remark = remark.split("Against")[0]

        html += f"""
                <tr>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{formatdate(row.posting_date)}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{_(row.voucher_type)}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{row.voucher_no}</td>
                    <td style="border: 1px solid #000; padding: 8px;">{remark}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{fmt_money(debit) if debit else ""}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{fmt_money(credit) if credit else ""}</td>
                    <td style="border: 1px solid #000; padding: 8px; text-align: center;">{fmt_money(balance)}</td>
                </tr>
        """

    html += f"""
                <!-- Total Movement Row -->
                <tr style="background: #f9fafb; font-weight: bold;">
                    <td colspan="4" style="border: 1px solid #000; padding: 10px; text-align: left;">إجمالي الحركة</td>
                    <td style="border: 1px solid #000; padding: 10px; text-align: center;">{fmt_money(total_debit)}</td>
                    <td style="border: 1px solid #000; padding: 10px; text-align: center;">{fmt_money(total_credit)}</td>
                    <td style="border: 1px solid #000; padding: 10px;"></td>
                </tr>
                <!-- Final Balance Row -->
                <tr style="font-weight: bold;">
                    <td style="border: 1px solid #000; padding: 10px; text-align: center; background: #fff;">{fmt_money(balance)}</td>
                    <td colspan="6" style="border: 1px solid #000; padding: 10px; text-align: right; font-size: 15px;">
                        الرصيد: <span style="color: red;">({balance_type}) {balance_in_words} .</span>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Signatures -->
        <div style="margin-top: 40px;">
            <table style="width: 100%; text-align: center; font-weight: bold; font-size: 14px;">
                <tr>
                    <td style="width: 33%;">توقيع المحاسب</td>
                    <td style="width: 33%;">توقيع المدير</td>
                    <td style="width: 33%;">توقيع العميل</td>
                </tr>
                <tr>
                    <td style="height: 60px; vertical-align: bottom;">..........................</td>
                    <td style="height: 60px; vertical-align: bottom;">..........................</td>
                    <td style="height: 60px; vertical-align: bottom;">..........................</td>
                </tr>
            </table>
        </div>
    </div>
    """
    
    return html

@frappe.whitelist()
def run_override(report_name, filters=None, **kwargs):
    from frappe.desk.query_report import run as original_run
    return original_run(report_name, filters, **kwargs)
