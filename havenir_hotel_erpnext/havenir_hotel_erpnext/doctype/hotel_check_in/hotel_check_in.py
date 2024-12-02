# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from datetime import datetime


class HotelCheckIn(Document):
    def before_save(self):
        # Check if reservation_status is "Confirmed"
        if self.reservation_status == "Confirmed":
            self.validate_room_availability()
            self.update_room_status()
    
    def validate_room_availability(self):
        for room in self.rooms:
            # Get room details from Rooms doctype
            room_doc = frappe.get_doc('Rooms', room.room_no)
            
            # Convert dates to datetime objects if they are in string format
            if isinstance(self.check_in, str):
                self.check_in = datetime.strptime(self.check_in, '%Y-%m-%d %H:%M:%S')
            if isinstance(self.check_out, str):
                self.check_out = datetime.strptime(self.check_out, '%Y-%m-%d %H:%M:%S')
            if isinstance(room_doc.check_in, str):
                room_doc.check_in = datetime.strptime(room_doc.check_in, '%Y-%m-%d %H:%M:%S')
            if isinstance(room_doc.check_out, str):
                room_doc.check_out = datetime.strptime(room_doc.check_out, '%Y-%m-%d %H:%M:%S')

            # Check if the selected room's check-in and check-out are conflicting
            # Also check that the current check-in is not for the same room
            if room_doc.check_in and room_doc.check_out:
                if (self.name != room_doc.check_in_id and
                    ((self.check_in >= room_doc.check_in and self.check_in <= room_doc.check_out) or
                     (self.check_out >= room_doc.check_in and self.check_out <= room_doc.check_out))):
                    # Use plain string instead of _ for error message
                    frappe.throw("Room {0} is already reserved from {1} to {2}.".format(
                        room.room_no, room_doc.check_in, room_doc.check_out))
    
                     
    def update_room_status(self):
        for room in self.rooms:
            # Update room status, check-in, and check-out
            room_doc = frappe.get_doc('Rooms', room.room_no)
            room_doc.room_status = "Reserved"
            room_doc.check_in = self.check_in
            room_doc.check_out = self.check_out
            room_doc.check_in_id = self.name
            room_doc.save()

    # def validate(self):
    #     for room in self.rooms:
    #         room_doc = frappe.get_doc('Rooms', room.room_no)
    #         if room_doc.room_status != 'Available':
    #             frappe.throw('Room {} is not Available'.format(room.room_no))

    # def on_submit(self):
    #     self.status = 'To Check Out'
    #     doc = frappe.get_doc('Hotel Check In', self.name)
    #     doc.db_set('status', 'To Check Out')
    #     for room in self.rooms:
    #         room_doc = frappe.get_doc('Rooms', room.room_no)
    #         room_doc.db_set('check_in_id', self.name)
    #         room_doc.db_set('room_status', 'Checked In')
    #     # send_payment_sms(self)
    def on_submit(self):
        # Update the status of Hotel Check In
        self.status = 'To Check Out'
        doc = frappe.get_doc('Hotel Check In', self.name)
        doc.db_set('status', 'To Check Out')
        # Update the room status for all selected rooms
        for room in self.rooms:
            if room.room_no:
                room_doc = frappe.get_doc('Rooms', room.room_no)
                room_doc.db_set('check_in_id', self.name)  # Link to the current Hotel Check In
                room_doc.db_set('room_status', 'Checked In')

    def on_cancel(self):
        self.status = "Cancelled"
        doc = frappe.get_doc('Hotel Check In', self.name)
        doc.db_set('status', 'Cancelled')
        for room in self.rooms:
            room_doc = frappe.get_doc('Rooms', room.room_no)
            room_doc.db_set('check_in_id', None)
            room_doc.db_set('room_status', 'Available')

    @frappe.whitelist()
    def get_room_price(self, room):
        room_price = frappe.get_value('Rooms', {
            'room_number': room
        }, [
            'price'
        ])
        return room_price

@frappe.whitelist()
def send_payment_sms(self):
    sms_settings = frappe.get_doc('SMS Settings')
    if sms_settings.sms_gateway_url:
        msg = 'Dear '
        msg += self.guest_name
        msg += ''',\nWe are delighted that you have selected our hotel. The entire team at the Hotel welcomes you and trust your stay with us will be both enjoyable and comfortable.\nRegards,\nHotel Management'''
        send_sms([self.contact_no], msg=msg)
