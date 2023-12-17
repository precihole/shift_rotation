import frappe

def update_related_shifts(doc, method):
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 0:
        get_last_shift_request = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name'], order_by='from_date desc')
        get_last_shift_request_of_custom = frappe.db.get_all('Shift Request', {'employee': doc.custom_switch_employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['name'], order_by='from_date desc')
        if get_last_shift_request:
            frappe.db.set_value('Shift Request', get_last_shift_request[0].name, 'to_date', frappe.utils.add_to_date(doc.from_date, days=-1))
            frappe.db.set_value('Shift Assignment', {'shift_request': get_last_shift_request[0].name}, 'end_date', frappe.utils.add_to_date(doc.from_date, days=-1))
        if get_last_shift_request_of_custom:
            frappe.db.set_value('Shift Request', get_last_shift_request_of_custom[0].name, 'to_date', frappe.utils.add_to_date(doc.from_date, days=-1))
            frappe.db.set_value('Shift Assignment', {'shift_request': get_last_shift_request_of_custom[0].name}, 'end_date', frappe.utils.add_to_date(doc.from_date, days=-1))


def create_change_shift_of_switching_with(doc, method):
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 0:
        last_shift_type = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['shift_type'], order_by='from_date desc', limit=1)
        if last_shift_type:
            new_doc = frappe.get_doc({
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
            new_doc.save()
            new_doc.submit()

    #create entry for further dates for both the employees
    if doc.custom_switch_shift == 1 and doc.custom_auto_shift == 1:
        employee_shift_data = frappe.db.get_all('Shift Request', {'employee': doc.employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['shift_type', 'custom_original_to_date'], order_by='from_date desc', limit=1)
        if employee_shift_data:
            emp = frappe.get_doc({
                "doctype": 'Shift Request',
                "shift_type": employee_shift_data[0].shift_type,
                "employee": doc.employee,
                "custom_shift_change_request": doc.custom_shift_change_request,
                "status": 'Approved',
                "from_date": frappe.utils.add_to_date(doc.to_date, days=1),
                "to_date": employee_shift_data[0].custom_original_to_date,
                "custom_original_to_date": employee_shift_data[0].custom_original_to_date,
            }).insert(ignore_permissions=True,ignore_mandatory=True)
            emp.save()
            emp.submit()
        switch_employee_shift_data = frappe.db.get_all('Shift Request', {'employee': doc.custom_switch_employee, 'custom_switch_shift': 0, 'docstatus': 1}, ['shift_type', 'custom_original_to_date'], order_by='from_date desc', limit=1)
        if switch_employee_shift_data:
            switch_emp = frappe.get_doc({
                "doctype": 'Shift Request',
                "shift_type": switch_employee_shift_data[0].shift_type,
                "employee": doc.custom_switch_employee,
                "custom_shift_change_request": doc.custom_shift_change_request,
                "status": 'Approved',
                "from_date": frappe.utils.add_to_date(doc.to_date, days=1),
                "to_date": switch_employee_shift_data[0].custom_original_to_date,
                "custom_original_to_date": employee_shift_data[0].custom_original_to_date,
            }).insert(ignore_permissions=True,ignore_mandatory=True)
            switch_emp.save()
            switch_emp.submit()

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