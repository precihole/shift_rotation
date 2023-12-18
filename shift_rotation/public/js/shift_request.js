frappe.ui.form.on('Shift Request', {
    custom_switch_employee:function(frm) {
        frappe.call({
            method: "shift_rotation.api.get_last_shift",
            args: {
                "emp": frm.doc.custom_switch_employee,
            },
            callback: function (res) {
                if (res.message != undefined){
                    console.log(res.message)
                    frm.set_value('shift_type', res.message)
                    frm.set_value('custom_switch_shift_type', res.message)
                }
            }
        })
    },
    to_date:function(frm) {
        frm.set_value('custom_original_to_date', frm.doc.to_date)
    },
    from_date:function(frm) {
        frm.set_value('custom_original_from_date', frm.doc.from_date)
    },
});