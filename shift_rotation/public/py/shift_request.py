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
    if shift_requests:
        last_shift_request = shift_requests[0]
        if last_shift_request.from_date == frappe.utils.getdate(from_date):
            frappe.db.set_value('Shift Request', last_shift_request.name, 'from_date', frappe.utils.add_to_date(to_date, days=1))
            frappe.db.set_value('Shift Assignment', {'shift_request': last_shift_request.name}, 'start_date', frappe.utils.add_to_date(to_date, days=1))
        elif not last_shift_request.from_date == frappe.utils.getdate(from_date):
            frappe.db.set_value('Shift Request', last_shift_request.name, 'to_date', frappe.utils.add_to_date(from_date, days=-1))
            frappe.db.set_value('Shift Assignment', {'shift_request': last_shift_request.name}, 'end_date', frappe.utils.add_to_date(from_date, days=-1))

def handle_shift_switching(doc, method):
    def get_shift_data(employee):
        filters = {
            'employee': employee,
            'custom_switch_shift': 0,
            'docstatus': 1
        }
        return frappe.db.get_all(
            'Shift Request',
            filters,
            ['shift_type', 'custom_original_from_date', 'custom_original_to_date'],
            order_by='from_date desc',
            limit=1
        )
    
    def create_entry_for_further_dates(employee, shift_data, to_date):
        if shift_data:
            if not shift_data[0].custom_original_to_date == frappe.utils.getdate(to_date) and shift_data[0].custom_original_from_date != frappe.utils.getdate(to_date):
                shift_type = shift_data[0].shift_type
                shift_request = frappe.get_doc({
                    "doctype": 'Shift Request',
                    "shift_type": shift_type,
                    "employee": employee,
                    "custom_shift_change_request": doc.custom_shift_change_request,
                    "status": 'Approved',
                    "from_date": frappe.utils.add_to_date(to_date, days=1),
                    "to_date": shift_data[0].custom_original_to_date,
                    "custom_original_to_date": shift_data[0].custom_original_to_date,
                }).insert(ignore_permissions=True, ignore_mandatory=True)
                shift_request.save()
                shift_request.submit()

    if doc.custom_switch_shift == 1:
        if doc.custom_auto_shift == 0:
            last_shift_type = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['shift_type'], order_by='from_date desc', limit=1)
            if last_shift_type:
                shift_request = frappe.get_doc({
                    "doctype": 'Shift Request',
                    "shift_type": last_shift_type[0].shift_type,
                    "employee": doc.custom_switch_employee,
                    "status": 'Approved',
                    "custom_switch_shift": 1,
                    "custom_auto_shift": 1,
                    "custom_switch_employee": doc.employee,
                    "custom_switch_shift_type": last_shift_type[0].shift_type,
                    "custom_shift_change_request": doc.name,
                    "from_date": doc.from_date,
                    "to_date": doc.to_date
                }).insert(ignore_permissions=True,ignore_mandatory=True)
                shift_request.save()
                shift_request.submit()

        elif doc.custom_auto_shift == 1:
            employee_shift_data = get_shift_data(doc.employee)
            create_entry_for_further_dates(doc.employee, employee_shift_data, doc.to_date)

            employee_shift_data = get_shift_data(doc.custom_switch_employee)
            create_entry_for_further_dates(doc.custom_switch_employee, employee_shift_data, doc.to_date)
        
def revert_shift_change(doc, method):
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 0:
        shift_request_filter = {'custom_shift_change_request': doc.name, 'docstatus': 1}
        frappe.db.set_value('Shift Request', shift_request_filter, {'status': 'Cancelled', 'workflow_state': 'Cancelled', 'docstatus': 2})
        
        assignments_filter = {'shift_request': doc.name, 'docstatus': 1}
        frappe.db.set_value('Shift Assignment', assignments_filter, {'status': 'Cancelled', 'workflow_state': 'Cancelled', 'docstatus': 2})

        get_employee_last_shift_request = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name', 'custom_original_to_date'], order_by='from_date desc', limit=1)
        frappe.db.set_value('Shift Request', get_employee_last_shift_request[0].name, 'to_date', get_employee_last_shift_request[0].custom_original_to_date)

        get_switch_employee_last_shift_request = frappe.db.get_all('Shift Request', {'employee': doc.custom_switch_employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name', 'custom_original_to_date'], order_by='from_date desc', limit=1)
        frappe.db.set_value('Shift Request', get_switch_employee_last_shift_request[0].name, 'to_date', get_switch_employee_last_shift_request[0].custom_original_to_date)