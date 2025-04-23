from flask import Flask
from systemdataclasses import vendor

vendor_list = vendor.VendorList()
v1 = vendor.Vendor("V001", "Acme Corp", "123-456-7890")
v2 = vendor.Vendor("V002", "Globex Inc", "987-654-3210")

vendor_list.add_vendor(v1)
vendor_list.add_vendor(v2)

app = Flask(__name__)

@app.route('/vendors', methods=['GET'])
def get_vendors():
    return vendor_list.toJson()

@app.route('/')
def hello_world():
    return 'Hello, World!'