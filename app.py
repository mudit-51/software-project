from flask import Flask, request
from systemdataclasses import vendor, batch, medicine
from flask_cors import CORS  # add this import

vendor_list = vendor.VendorList()
v1 = vendor.Vendor("V001", "Acme Corp", "123-456-7890")
v2 = vendor.Vendor("V002", "Globex Inc", "987-654-3210")
vendor_list.add_vendor(v1)
vendor_list.add_vendor(v2)

batch_list = batch.BatchList()
b1 = batch.Batch("B001", "2024-12-31")
b2 = batch.Batch("B002", "2025-06-30")
batch_list.add_batch(b1)
batch_list.add_batch(b2)

medicine_list = medicine.MedicineList()

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

@app.route('/batches', methods=['GET'])
def get_batches():
    return batch_list.toJson()

@app.route('/batches/add', methods=['POST'])
def add_batch():
    data = request.get_json()
    new_batch = batch.Batch(data['batch_number'], data['expiry_date'])
    batch_list.add_batch(new_batch)
    return {'message': 'Batch added successfully'}, 201

@app.route('/medicines', methods=['GET'])
def get_medicines():
    return medicine_list.toJson()

@app.route('/medicines/add', methods=['POST'])
def add_medicine():
    data = request.get_json()
    batch_obj = batch_list.find_batch(data['batch_number'])
    if not batch_obj:
        return {'message': 'Batch not found'}, 404
    vendor_obj = vendor_list.find_vendor(data['vendor_id'])
    if not vendor_obj:
        return {'message': 'Vendor not found'}, 404
    new_medicine = medicine.Medicine(data['name'], batch_obj, data['expiry_date'], data['price'], vendor_obj)
    medicine_list.add_medicine(new_medicine)
    return {'message': 'Medicine added successfully'}, 201

@app.route('/')
def hello_world():
    return 'Hello, World!'