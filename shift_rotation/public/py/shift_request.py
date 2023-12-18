import frappe

def adjust_shift_dates(doc, method):
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 0:
        update_shift_request(doc.employee, 0, doc.from_date, doc.to_date)
        update_shift_request(doc.custom_switch_employee, 0, doc.from_date, doc.to_date)

def update_shift_request(employee, custom_switch_shift, from_date, to_date):
    filters = {
        'employee': employee,
        'custom_switch_shift': custom_switch_shift,
        'docstatus': 1
    }

    shift_requests = frappe.db.get_all('Shift Request', filters, ['name', 'from_date'], order_by='from_date desc')
    frappe.errprint(shift_requests)
    if shift_requests:
        last_shift_request = shift_requests[0]
        if last_shift_request.from_date == frappe.utils.getdate(from_date):
            frappe.db.set_value('Shift Request', last_shift_request.name, 'from_date', frappe.utils.add_to_date(to_date, days=1))
            frappe.db.set_value('Shift Assignment', {'shift_request': last_shift_request.name}, 'start_date', frappe.utils.add_to_date(to_date, days=1))
        elif not last_shift_request.from_date == frappe.utils.getdate(from_date):
            frappe.db.set_value('Shift Request', last_shift_request.name, 'to_date', frappe.utils.add_to_date(from_date, days=-1))
            frappe.db.set_value('Shift Assignment', {'shift_request': last_shift_request.name}, 'end_date', frappe.utils.add_to_date(from_date, days=-1))

def handle_shift_switching(doc, method):
    if doc.custom_switch_shift == 1:
        if doc.custom_auto_shift == 0:
            #auto shift
            create_and_submit_shift_request(
                doc.custom_switch_employee,
                1,
                doc.employee,
                doc.name,
                doc.from_date,
                doc.to_date,
                shift_type=get_last_shift_type(doc.employee)
            )

        elif doc.custom_auto_shift == 1:
            create_and_submit_shift_request_for_further_dates(
                doc.employee,
                doc.to_date,
                get_last_shift_data(doc.employee)
            )

            create_and_submit_shift_request_for_further_dates(
                doc.custom_switch_employee,
                doc.to_date,
                get_last_shift_data(doc.custom_switch_employee)
            )

def get_last_shift_type(employee):
    return frappe.db.get_value('Shift Request', {
        'employee': employee,
        'custom_switch_shift': 0,
        'docstatus': 1
    }, 'shift_type', order_by='from_date desc')

def get_last_shift_data(employee):
    return frappe.db.get_all('Shift Request', {
        'employee': employee,
        'custom_switch_shift': 0,
        'docstatus': 1
    }, ['shift_type', 'custom_original_to_date'], order_by='from_date desc', limit=1)

def create_and_submit_shift_request(employee, from_date, to_date, s_flag, shift_type=None, s_employee=None, docname=None):
    shift_doc = frappe.new_doc('Shift Request')
    shift_doc.update({
        'doctype': 'Shift Request',
        'shift_type': shift_type,
        'employee': employee,
        'status': 'Approved',
        'custom_switch_shift': 1,
        'custom_auto_shift': s_flag,
        'custom_switch_employee': s_employee,
        'custom_shift_change_request': docname,
        'from_date': from_date,
        'to_date': to_date,
    })

    shift_doc.insert(ignore_permissions=True, ignore_mandatory=True)
    shift_doc.save()
    shift_doc.submit()

def create_and_submit_shift_request_for_further_dates(employee, to_date, last_shift_data):
    if last_shift_data and not last_shift_data[0].custom_original_to_date == to_date:
        create_and_submit_shift_request(
            employee,
            frappe.utils.add_to_date(to_date, days=1),
            last_shift_data[0].custom_original_to_date,
            0,
            shift_type=last_shift_data[0].shift_type
        )
        
def remove_all_effect(doc, method):
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 0:
        #cancel all linked document
        frappe.db.set_value('Shift Request', {'custom_shift_change_request': doc.name, 'docstatus': 1}, 'status', 'Cancelled')
        frappe.db.set_value('Shift Request', {'custom_shift_change_request': doc.name, 'docstatus': 1}, 'workflow_state', 'Cancelled')
        frappe.db.set_value('Shift Request', {'custom_shift_change_request': doc.name, 'docstatus': 1}, 'docstatus', 2)
        
        all_linked = frappe.db.get_all('Shift Request', {'custom_shift_change_request': doc.name, 'docstatus': 1}, ['name'])
        for item in all_linked:
            frappe.db.set_value('Shift Assignment', {'shift_request': doc.name, 'docstatus': 1}, 'status', 'Cancelled')
            frappe.db.set_value('Shift Assignment', {'shift_request': doc.name, 'docstatus': 1}, 'workflow_state', 'Cancelled')
            frappe.db.set_value('Shift Assignment', {'shift_request': item.name, 'docstatus': 1}, 'docstatus', 2)

        #update last shift as it is
        get_employee_last_shift_request = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name', 'custom_original_to_date'], order_by='from_date desc')
        frappe.db.set_value('Shift Request', get_employee_last_shift_request[0].name, 'to_date', get_employee_last_shift_request[0].custom_original_to_date)
        
        get_switch_employee_last_shift_request = frappe.db.get_all('Shift Request', {'employee': doc.custom_switch_employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name', 'custom_original_to_date'], order_by='from_date desc')
        frappe.db.set_value('Shift Request', get_switch_employee_last_shift_request[0].name, 'to_date', get_switch_employee_last_shift_request[0].custom_original_to_date)