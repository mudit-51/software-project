from flask import Flask, request
from flask_cors import CORS
import uuid
from systemdataclasses.vendor import Vendor, VendorList
from systemdataclasses.medicine import Medicine
from systemdataclasses.batch import Batch
from systemdataclasses.inventory import Inventory
from systemdataclasses.sales import Sales
from systemdataclasses.cart import Cart

# Initialize data structures
vendor_list = VendorList()
inventory = Inventory([], [])
sales = Sales()
carts = {}

# Add sample vendors
v1 = Vendor("V001", "Acme Corp", "123-456-7890")
v2 = Vendor("V002", "Globex Inc", "987-654-3210")
vendor_list.add_vendor(v1)
vendor_list.add_vendor(v2)

app = Flask(__name__)
CORS(app)


# Vendor routes
@app.route('/vendors', methods=['GET'])
def get_vendors():
    return {'vendors': vendor_list.toJson()}


@app.route('/vendors/add', methods=['POST'])
def add_vendor():
    data = request.get_json()
    new_vendor = Vendor(data['vendor_id'], data['name'], data['contact_info'])
    vendor_list.add_vendor(new_vendor)
    return {'message': 'Vendor added successfully'}, 201


@app.route('/vendors/<vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    vendor = next((v for v in vendor_list.get_vendors() if v.vendor_id == vendor_id), None)
    return vendor.toJson() if vendor else ('', 404)


@app.route('/vendors/<vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    data = request.get_json()
    vendor = next((v for v in vendor_list.get_vendors() if v.vendor_id == vendor_id), None)
    if not vendor:
        return {'error': 'Vendor not found'}, 404
    vendor.name = data.get('name', vendor.name)
    vendor.contact_info = data.get('contact_info', vendor.contact_info)
    return vendor.toJson()


@app.route('/vendors/<vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    vendor_list.remove_vendor(vendor_id)
    return {'message': 'Vendor deleted successfully'}


# Inventory routes
@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory_data = []
    for med, qty in inventory.inventory.items():
        inventory_data.append({
            'identifier': med.identifier,
            'name': med.name,
            'batch': {
                'batch_number': med.batch.batch_number,
                'expiry_date': med.batch.expiry_date
            },
            'expiry_date': med.expiry_date,
            'price': med.price,
            'vendor': med.vendor.toJson(),
            'quantity': qty
        })
    return {'inventory': inventory_data}


@app.route('/inventory/add', methods=['POST'])
def add_to_inventory():
    data = request.get_json()
    try:
        vendor = next(v for v in vendor_list.get_vendors() if v.vendor_id == data['vendor_id'])
    except StopIteration:
        return {'error': 'Vendor not found'}, 404

    batch = Batch(data['batch_number'], data['batch_expiry_date'])
    medicine = Medicine(
        name=data['name'],
        batch=batch,
        expiry_date=data['medicine_expiry_date'],
        price=data['price'],
        vendor=vendor
    )
    inventory.add_medicine(medicine, data['quantity'])
    return {'message': 'Medicine added to inventory'}, 201


@app.route('/inventory/remove', methods=['POST'])
def remove_from_inventory():
    data = request.get_json()
    for med in inventory.inventory:
        if med.identifier == data['identifier']:
            try:
                inventory.remove_medicine(med, data['quantity'])
                return {'message': 'Stock updated'}
            except ValueError as e:
                return {'error': str(e)}, 400
    return {'error': 'Medicine not found'}, 404


@app.route('/inventory/valuation', methods=['GET'])
def get_valuation():
    return {'total_value': inventory.get_stock_valuation()}


@app.route('/inventory/alerts', methods=['GET'])
def get_alerts():
    threshold = request.args.get('threshold', default=10, type=int)
    alerts = []
    for med, qty in inventory.get_threshold_alerts(threshold):
        alerts.append({
            'name': med.name,
            'identifier': med.identifier,
            'quantity': qty
        })
    return {'alerts': alerts}


@app.route('/inventory/expired', methods=['GET'])
def get_expired():
    current_date = request.args.get('current_date')
    expired = []
    for med, expiry in inventory.track_batch_expiry(current_date):
        expired.append({
            'name': med.name,
            'batch_expiry': expiry,
            'identifier': med.identifier
        })
    return {'expired': expired}


# Cart routes
@app.route('/carts', methods=['POST'])
def create_cart():
    cart_id = str(uuid.uuid4())
    carts[cart_id] = Cart(sales)
    return {'cart_id': cart_id}, 201


@app.route('/carts/<cart_id>/add', methods=['POST'])
def add_cart_item(cart_id):
    data = request.get_json()
    cart = carts.get(cart_id)
    if not cart:
        return {'error': 'Cart not found'}, 404

    for med in inventory.inventory:
        if med.identifier == data['identifier']:
            if inventory.get_quantity(med) < data['quantity']:
                return {'error': 'Insufficient stock'}, 400
            cart.add_item(med, data['quantity'])
            return {'message': 'Item added to cart'}
    return {'error': 'Medicine not found'}, 404


@app.route('/carts/<cart_id>/checkout', methods=['POST'])
def checkout(cart_id):
    cart = carts.get(cart_id)
    if not cart:
        return {'error': 'Cart not found'}, 404

    try:
        for med, qty in cart.get_cart().items():
            inventory.remove_medicine(med, qty)
    except ValueError as e:
        return {'error': str(e)}, 400

    receipt = cart.generate_receipt()
    del carts[cart_id]
    return {'receipt': receipt}


# Sales routes
@app.route('/sales/history', methods=['GET'])
def sales_history():
    history = []
    for cart in sales.get_sales_history():
        items = []
        for med, qty in cart.get_cart().items():
            items.append({
                'name': med.name,
                'quantity': qty,
                'price': med.price,
                'total': med.price * qty
            })
        history.append({'items': items, 'total': cart.calculate_total()})
    return {'history': history}


@app.route('/sales/rank/quantity', methods=['GET'])
def rank_quantity():
    ranked = []
    for med in sales.rank_by_quantity():
        ranked.append({'name': med.name, 'identifier': med.identifier})
    return {'ranked': ranked}


@app.route('/sales/rank/value', methods=['GET'])
def rank_value():
    ranked = []
    for med in sales.rank_by_value():
        ranked.append({'name': med.name, 'identifier': med.identifier})
    return {'ranked': ranked}


if __name__ == '__main__':
    app.run(debug=True)