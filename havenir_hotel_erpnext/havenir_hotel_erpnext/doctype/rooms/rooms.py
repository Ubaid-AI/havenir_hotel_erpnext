# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir and contributors
# For license information, please see license.txt

# from __future__ import unicode_literals
# # import frappe
# from frappe.model.document import Document

# class Rooms(Document):
# 	pass
from __future__ import unicode_literals
import dateutil
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import set_name_by_naming_series
from frappe.utils import cint, cstr, getdate
from erpnext import get_default_currency
from erpnext.accounts.party import get_dashboard_info

class Rooms(Document):
	def validate(self):
		# self.set_full_name()
		self.flags.is_new_doc = self.is_new()
		# self.flags.existing_item = self.is_new() and bool(self.item)

	def before_insert(self):
		self.set_missing_item_details()

	def on_update(self):
		if frappe.db.get_single_value("Nazeel Settings", "link_item_to_room"):
			if self.item:
				if  frappe.db.exists(
					{"doctype": "Rooms", "name": ["!=", self.name], "item": self.item}
				):
					self.update_patient_based_on_existing_item()
				else:
					self.update_linked_item()

			else:
				create_item(self)



	def update_linked_item(self):
		item = frappe.get_doc("Item", self.item)
		if self.item_group:
			item.item_group = self.item_group
		item.item_name = self.guest_name
		item.item_group = self.item_group
		item.standard_rate = self.price
		item.ignore_mandatory = True
		item.save(ignore_permissions=True)

		frappe.msgprint(_("item {0} updated").format(item.name), alert=True)

	def update_patient_based_on_existing_item(self):
		item = frappe.get_doc("Item", self.item)
		self.db_set(
			{
				"item": item.name,
				"item_group": item.item_group,
			}
		)
		self.notify_update()

	def set_missing_item_details(self):
		if not self.item_group:
			self.item_group = frappe.db.get_single_value(
				"Nazeel Settings", "item_group"
			)
		# if not self.territory:
		# 	self.territory = frappe.db.get_single_value("Selling Settings", "territory") or get_root_of(
		# 		"Territory"
		# 	)
		# if not self.default_price_list:
		# 	self.default_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")

		if not self.item_group:
			frappe.msgprint(
				_(
					"Please set defaults for Item Group in Nazeel Settings"
				),
				alert=True,
			)

def create_item(doc):
	item = frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": doc.room_number,
			"item_name": doc.room_name,
			"item_group": doc.item_group
			or frappe.db.get_single_value("Stock Settings", "item_group"),
			"stock_uom": "Nos" or frappe.db.get_single_value("Stock Settings", "stock_uom"),
			"is_stock_item": 0,
			"include_item_in_manufacturing":0,
			"standard_rate": doc.price,
			"is_sales_item": 1,
		}
	).insert(ignore_permissions=True, ignore_mandatory=True)

	frappe.db.set_value("Rooms", doc.name, "item", item.name)
	frappe.msgprint(_("Item {0} created and linked to Unit").format(item.name), alert=True)




		# if not self.default_currency:
		# 	self.default_currency = get_default_currency()
		# if not self.language:
		# 	self.language = frappe.db.get_single_value("System Settings", "language")
