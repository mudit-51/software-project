from flask import Flask, request
from systemdataclasses import vendor, batch, medicine, inventory, sales, cart
from flask_cors import CORS  # add this import

inventory_obj = inventory.Inventory()
medicine_list = medicine.MedicineList()
vendor_list = vendor.VendorList()

v1 = vendor.Vendor("V001", "Acme Corp", "123-456-7890", inventory_obj, medicine_list)
v2 = vendor.Vendor("V002", "Globex Inc", "987-654-3210", inventory_obj, medicine_list)
vendor_list.add_vendor(v1)
vendor_list.add_vendor(v2)

batch_list = batch.BatchList()
b1 = batch.Batch("B001", "2024-12-31")
b2 = batch.Batch("B002", "2025-06-30")
batch_list.add_batch(b1)
batch_list.add_batch(b2)

m1 = medicine.Medicine("Aspirin", b1, "2024-12-31", 9.99, v1)
m2 = medicine.Medicine("Ibuprofen", b2, "2025-06-30", 12.99, v2)
medicine_list.add_medicine(m1)
medicine_list.add_medicine(m2)

for x in medicine_list.get_medicines():
    inventory_obj.add_medicine(x, 10)

sales_instance = sales.Sales()

app = Flask(__name__)
CORS(app)


# Vendor routes
@app.route("/vendors", methods=["GET"])
def get_vendors():
    return {"vendors": vendor_list.toJson()}


@app.route("/vendors/<vendor_id>/orders", methods=["GET"])
def get_vendor(vendor_id):
    request_type = request.args.get("type", default="all", type=str)
    vendor_obj: vendor.Vendor = vendor_list.find_vendor(vendor_id)
    if not vendor_obj:
        return {"message": "Vendor not found"}, 404
    if request_type == "fulfilled":
        return vendor_obj.get_fulfilled_orders()
    return vendor_obj.get_orders()


@app.route("/vendors/<vendor_id>/orders/process", methods=["GET"])
def fulfill_order(vendor_id):
    print("should not fire")
    order_id = request.args.get("order_id", default="", type=str)
    action = request.args.get("action", default="", type=str)
    if not order_id or not action:
        return {"message": "Order ID and action are required"}, 400
    if action != "approve" and action != "deny":
        return {"message": "Invalid action"}, 400
    vendor_obj: vendor.Vendor = vendor_list.find_vendor(vendor_id)
    if not vendor_obj:
        return {"message": "Vendor not found"}, 404
    try:
        if action == "approve":
            vendor_obj.fullfill_order(order_id)
            return {"message": "Order fulfilled successfully"}, 200
        else:
            vendor_obj.reject_order(order_id)
            return {"message": "Order denied successfully"}, 200
    except ValueError as e:
        return {"message": str(e)}, 400


@app.route("/vendors/add", methods=["POST"])
def add_vendor():
    data = request.get_json()
    new_vendor = vendor.Vendor(data["vendor_id"], data["name"], data["contact_info"], inventory_obj, medicine_list)
    vendor_list.add_vendor(new_vendor)
    return {"message": "Vendor added successfully"}, 201


@app.route("/batches", methods=["GET"])
def get_batches():
    return batch_list.toJson()


@app.route("/batches/add", methods=["POST"])
def add_batch():
    data = request.get_json()
    new_batch = batch.Batch(data["batch_number"], data["expiry_date"])
    batch_list.add_batch(new_batch)
    return {"message": "Batch added successfully"}, 201


@app.route("/medicines", methods=["GET"])
def get_medicines():
    return medicine_list.toJson()


@app.route("/medicines/add", methods=["POST"])
def add_medicine():
    data = request.get_json()
    batch_obj = batch_list.find_batch(data["batch_number"])
    if not batch_obj:
        return {"message": "Batch not found"}, 404
    vendor_obj = vendor_list.find_vendor(data["vendor_id"])
    if not vendor_obj:
        return {"message": "Vendor not found"}, 404
    new_medicine = medicine.Medicine(
        data["name"], batch_obj, data["expiry_date"], data["price"], vendor_obj
    )
    medicine_list.add_medicine(new_medicine)
    return {"message": "Medicine added successfully"}, 201


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return inventory_obj.toJson()


@app.route("/inventory/add", methods=["POST"])
def add_inventory_item():
    data = request.get_json()
    medicine_obj = medicine_list.find_medicine(data["identifier"])
    if not medicine_obj:
        return {"message": "Medicine not found"}, 404
    inventory_obj.queue_order(medicine_obj, data["quantity"])
    return {"message": "Inventory item added successfully"}, 201


@app.route("/inventory/threshold", methods=["GET"])
def get_threshold_alerts():
    threshold = request.args.get("threshold", default=0, type=int)
    return inventory_obj.threshold_toJson(threshold)


@app.route("/inventory/expiry", methods=["GET"])
def get_expiry_alerts():
    current_date = request.args.get("target_date", default="2023-10-01", type=str)
    return inventory_obj.expiry_toJson(current_date)


@app.route("/inventory/valuation", methods=["GET"])
def get_stock_valuation():
    return {"stock_valuation": inventory_obj.get_stock_valuation()}


@app.route("/cart/checkout", methods=["POST"])
def create_cart():
    data = request.get_json()
    curr_cart = cart.Cart(sales_instance, inventory_obj)
    for item in data["items"]:
        medicine_obj = medicine_list.find_medicine(item["medicine"]["identifier"])
        if not medicine_obj:
            return {"message": "Medicine not found"}, 404
        curr_cart.add_item(medicine_obj, item["quantity"])

    return curr_cart.generate_reciept_json(), 201


@app.route("/statistics", methods=["GET"])
def get_value_statistics():
    return sales_instance.get_sales_statistics()


@app.route("/history", methods=["GET"])
def get_history():
    temp = sales_instance.get_sales_history_json()
    temp.reverse()
    return temp


@app.route("/")
def hello_world():
    return "Hello, World!"
