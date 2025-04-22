from systemdataclasses import vendor
from systemdataclasses import medicine

v1 = vendor.Vendor("V001", "ABC Pharmaceuticals", "123-456-7890")

print(str(v1))

m1 = medicine.Medicine("Paracetamol", "B001", "2025-12-31", 10.99, v1)

print(str(m1))