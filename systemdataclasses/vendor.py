from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    import inventory  # noqa: F401
    import medicine  # noqa: F401


class Vendor:
    def __init__(
        self,
        vendor_id: str,
        name: str,
        contact_info: str,
        inventory_obj: inventory.Inventory,
    ):
        self.vendor_id = vendor_id
        self.name = name
        self.contact_info = contact_info
        self.orders = {}
        self.orders_fulfilled = {}
        self.inventory_obj = inventory_obj

    def add_order(self, order):
        order_id = "".join(
            random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            for _ in range(5)
        )
        self.orders.update({order_id: order})

    def fullfill_order(self, order_id: str):
        if order_id in self.orders:
            order = self.orders[order_id]
            medicine_obj = self.inventory_obj.search_medicine(order["identifier"])
            if medicine_obj:
                self.inventory_obj.add_medicine(medicine_obj, order["quantity"])
                self.orders_fulfilled.update({order_id: order})
                del self.orders[order_id]
            else:
                raise ValueError("Medicine not found in inventory.")
        else:
            raise ValueError("Order ID not found.")

    def reject_order(self, order_id: str):
        if order_id in self.orders:
            del self.orders[order_id]
        else:
            raise ValueError("Order ID not found.")

    def __str__(self):
        return f"Vendor ID: {self.vendor_id}, Name: {self.name}, Contact Info: {self.contact_info}"

    def get_orders(self):
        res = []
        order: dict
        for id, order in self.orders.items():
            order.update({"order_id": id})
            res.append(order)
        return res

    def get_fulfilled_orders(self):
        res = []
        order: dict
        for id, order in self.orders_fulfilled.items():
            order.update({"order_id": id})
            res.append(order)
        return res
    
    def toJson(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "contact_info": self.contact_info,
        }


class VendorList:
    def __init__(self):
        self.vendors = []

    def add_vendor(self, vendor: Vendor):
        self.vendors.append(vendor)

    def remove_vendor(self, vendor_id: str):
        self.vendors = [
            vendor for vendor in self.vendors if vendor.vendor_id != vendor_id
        ]

    def get_vendors(self):
        return self.vendors

    def find_vendor(self, vendor_id: str):
        for vendor in self.vendors:
            if vendor.vendor_id == vendor_id:
                return vendor
        return None

    def toJson(self):
        return [vendor.toJson() for vendor in self.vendors]
