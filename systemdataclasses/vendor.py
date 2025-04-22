class Vendor:
    def __init__(self, vendor_id: str, name: str, contact_info: str):
        self.vendor_id = vendor_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Vendor ID: {self.vendor_id}, Name: {self.name}, Contact Info: {self.contact_info}"
