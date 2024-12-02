# install.py in havenir_hotel_erpnext/havenir_hotel_erpnext/

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    frappe.msgprint("Creating Custom Fields for Sales Invoice")
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "check_in_id",
                "label": "Check In ID",
                "fieldtype": "Data",
                "insert_after": "customer_name",  # Ensure this field exists
                "reqd": 0,
                "description": "Reference ID for Check-In",
            },
            {
                "fieldname": "check_out_id",
                "label": "Check Out ID",
                "fieldtype": "Data",
                "insert_after": "check_in_id",
                "reqd": 0,
                "description": "Reference ID for Check-Out",
            },
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            create_custom_field(doctype, field)

    frappe.db.commit()

def before_install():
    check_if_erpnext_installed()

def check_if_erpnext_installed():
    if "erpnext" not in frappe.get_installed_apps():
        frappe.throw("Please install the ERPNext app first before installing Havenir Hotel ERPNext app.")
