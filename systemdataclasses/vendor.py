class Vendor:
    def __init__(self, vendor_id: str, name: str, contact_info: str):
        self.vendor_id = vendor_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Vendor ID: {self.vendor_id}, Name: {self.name}, Contact Info: {self.contact_info}"
    
    def toJson(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "contact_info": self.contact_info
        }

class VendorList:
    def __init__(self):
        self.vendors = []

    def add_vendor(self, vendor: Vendor):
        self.vendors.append(vendor)

    def remove_vendor(self, vendor_id: str):
        self.vendors = [vendor for vendor in self.vendors if vendor.vendor_id != vendor_id]
        
    def get_vendors(self):
        return self.vendors

    def toJson(self):
        return [vendor.toJson() for vendor in self.vendors]