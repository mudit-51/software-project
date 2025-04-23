from flask import Flask, request
from systemdataclasses import vendor
from flask_cors import CORS  # add this import

vendor_list = vendor.VendorList()
v1 = vendor.Vendor("V001", "Acme Corp", "123-456-7890")
v2 = vendor.Vendor("V002", "Globex Inc", "987-654-3210")

vendor_list.add_vendor(v1)
vendor_list.add_vendor(v2)

app = Flask(__name__)
CORS(app)  # enable CORS for all routes and origins

@app.route('/vendors', methods=['GET'])
def get_vendors():
    return vendor_list.toJson()

@app.route('/vendors/add', methods=['POST'])
def add_vendor():
    data = request.get_json()
    print(data)
    new_vendor = vendor.Vendor(data['vendor_id'], data['name'], data['contact_info'])
    vendor_list.add_vendor(new_vendor)
    return {'message': 'Vendor added successfully'}, 201


@app.route('/')
def hello_world():
    return 'Hello, World!'