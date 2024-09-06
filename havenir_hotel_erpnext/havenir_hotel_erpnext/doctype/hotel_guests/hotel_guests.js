// Copyright (c) 2020, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotel Guests", {
  guest_name: function(frm) {
    frm.set_value("guest_name", frm.doc.guest_name.toUpperCase());
  },

  validate: function(frm) {
    // && frm.doc.passport_no == undefined
    if (frm.doc.cnic == undefined ) {
      frappe.throw("Please enter ID Number");
    }

    // if (frm.doc.cnic && frm.doc.cnic.length != 15) {
    //   frm.doc.cnic = undefined;
    //   frm.refresh_field("cnic");
    //   frappe.msgprint("Please enter CNIC in the correct format");
    // } else {
    //   if (frm.doc.cnic[5] != "-") {
    //     frm.doc.cnic = undefined;
    //     frm.refresh_field("cnic");
    //     frappe.msgprint("Please enter CNIC in the correct format");
    //   }
    //   if (frm.doc.cnic[13] != "-") {
    //     frm.doc.cnic = undefined;
    //     frm.refresh_field("cnic");
    //     frappe.msgprint("Please enter CNIC in the correct format");
    //   }
    // }
    // if (frm.doc.contact_no && frm.doc.contact_no.length != 12) {
    //   frm.doc.contact_no = undefined;
    //   frm.refresh_field("contact_no");
    //   frappe.msgprint("Please enter Mobile No in the correct format");
    // } else {
    //   if (frm.doc.contact_no[0] != "9") {
    //     frm.doc.contact_no = undefined;
    //     frm.refresh_field("contact_no");
    //     frappe.msgprint("Please enter Mobile No in the correct format");
    //   }
    //   if (frm.doc.contact_no[1] != "2") {
    //     frm.doc.contact_no = undefined;
    //     frm.refresh_field("contact_no");
    //     frappe.msgprint("Please enter Mobile No in the correct format");
    //   }
    // }
  }
});
