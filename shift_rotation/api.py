import frappe

@frappe.whitelist()
def get_last_shift():
    last_shift_type = frappe.db.get_all('Shift Request', {'employee': frappe.form_dict.emp, 'custom_switch_shift': 0, 'docstatus': 1}, ['shift_type'], order_by='from_date desc', limit=1)
    if last_shift_type:
        return last_shift_type[0].shift_type