"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

type Batch = {
  batch_number: string;
  expiry_date: string;
};
type Vendor = {
  vendor_id: string;
  name: string;
  contact_info: string;
};
type Medicine = {
  name: string;
  identifier: string;
  batch: Batch;
  expiry_date: string;
  price: number;
  vendor: Vendor;
};

type Inventory = {
  medicine: Medicine;
  quantity: number;
};

export default function Page() {
  const [loading, setLoading] = useState(true);
  const [inventory, setInventory] = useState<Inventory[]>([]);
  const [allMedicines, setAllMedicines] = useState<Medicine[]>([]);
  const [showDialog, setShowDialog] = useState(false);
  const [selectedMedicineId, setSelectedMedicineId] = useState<string>("");
  const [quantity, setQuantity] = useState<number>(0);
  const [showLowStockDialog, setShowLowStockDialog] = useState(false);
  const [showExpiryDialog, setShowExpiryDialog] = useState(false);
  const [threshold, setThreshold] = useState<number>(0);
  const [lowStockResults, setLowStockResults] = useState<Inventory[]>([]);
  const [expiryDate, setExpiryDate] = useState<string>("");
  const [expiryResults, setExpiryResults] = useState<Inventory[]>([]);
  const [stockValuation, setStockValuation] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        // Fetch medicines first
        const medicinesRes = await fetch("http://localhost:5000/medicines");
        const medicinesData: Medicine[] = await medicinesRes.json();
        setAllMedicines(medicinesData);

        // Then fetch inventory
        const inventoryRes = await fetch("http://localhost:5000/inventory");
        const inventoryData: Inventory[] = await inventoryRes.json();
        setInventory(inventoryData);
      } catch (e) {
        // handle error as needed
        console.error("Error fetching data:", e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchStockValuation() {
      try {
        const res = await fetch("http://localhost:5000/inventory/valuation");
        const data = await res.json();
        setStockValuation(data['stock_valuation']);
      } catch (e) {
        setStockValuation(null);
      }
    }
    fetchStockValuation();
  }, []);

  const handleAddInventory = async () => {
    if (!selectedMedicineId) return;
    await fetch("http://localhost:5000/inventory/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier: selectedMedicineId, quantity }),
    });
    setShowDialog(false);
    setQuantity(0);
    setSelectedMedicineId("");
    setLoading(true);
    const res = await fetch("http://localhost:5000/inventory");
    const inventoryData: Inventory[] = await res.json();
    setInventory(inventoryData);
    // Fetch updated stock valuation
    try {
      const valRes = await fetch("http://localhost:5000/inventory/valuation");
      const valData = await valRes.json();
      setStockValuation(valData['stock_valuation']);
    } catch (e) {
      setStockValuation(null);
    }
    setLoading(false);
    toast.success("Order has been submitted to the vendor");
  };

  const handleFetchLowStock = async () => {
    if (!threshold || threshold < 0) return;
    const res = await fetch(
      `http://localhost:5000/inventory/threshold?threshold=${threshold}`
    );
    const data: Inventory[] = await res.json();
    setLowStockResults(data);
  };

  const handleFetchExpiry = async () => {
    if (!expiryDate) return;
    const res = await fetch(
      `http://localhost:5000/inventory/expiry?target_date=${expiryDate}`
    );
    const data: Inventory[] = await res.json();
    setExpiryResults(data);
  };

  // Helper to get selected medicine price
  const selectedMedicine = allMedicines.find(
    (med) => med.identifier === selectedMedicineId
  );
  const orderCost =
    selectedMedicine && quantity > 0
      ? selectedMedicine.price * quantity
      : 0;

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-6">
      {/* Total Stock Valuation Section */}
      <div className="mb-6">
        <div className="text-muted-foreground text-sm">
          Total Stock Valuation
        </div>
        <div className="text-2xl font-bold">
          {stockValuation !== null
            ? `₹${stockValuation.toLocaleString()}`
            : "—"}
        </div>
      </div>
      {/* Add Inventory Button */}
      <div className="mb-4 flex gap-2">
        <Button onClick={() => setShowDialog(true)}>Add Inventory</Button>
        <Button
          variant="outline"
          onClick={() => {
            setShowLowStockDialog(true);
            setLowStockResults([]);
            setThreshold(0);
          }}
        >
          Low Stock
        </Button>
        <Button
          variant="outline"
          onClick={() => {
            setShowExpiryDialog(true);
            setExpiryResults([]);
            setExpiryDate("");
          }}
        >
          Expiring After
        </Button>
      </div>
      {/* Add Inventory Dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Inventory</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block mb-1 text-sm">Select Medicine</label>
              <Select
                value={selectedMedicineId}
                onValueChange={setSelectedMedicineId}
              >
                <SelectTrigger>
                  <SelectValue placeholder="-- Select --" />
                </SelectTrigger>
                <SelectContent>
                  {allMedicines.map((med) => (
                    <SelectItem key={med.identifier} value={med.identifier}>
                      {med.name + " | " + med.identifier}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="block mb-1 text-sm">Quantity</label>
              <Input
                type="number"
                value={quantity}
                min={1}
                onChange={(e) => setQuantity(Number(e.target.value))}
              />
            </div>
          </div>
          <DialogFooter className="flex gap-2 mt-4">
            {/* Order cost display */}
            <div className="flex-1 text-left text-muted-foreground text-sm flex items-center">
              {selectedMedicineId && quantity > 0
                ? <>Order Cost: <span className="font-semibold ml-1">₹{orderCost.toLocaleString()}</span></>
                : null}
            </div>
            <Button
              onClick={handleAddInventory}
              disabled={!selectedMedicineId || quantity <= 0}
            >
              Add
            </Button>
            <Button variant="secondary" onClick={() => setShowDialog(false)}>
              Cancel
            </Button>
            <Button
              variant="outline"
              className="ml-auto"
              onClick={() => router.push("/medicines")}
            >
              New Medicine
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      {/* Low Stock Dialog */}
      <Dialog open={showLowStockDialog} onOpenChange={setShowLowStockDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Medicines Below Stock Threshold</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block mb-1 text-sm">Threshold</label>
              <Input
                type="number"
                value={threshold}
                min={0}
                onChange={(e) => setThreshold(Number(e.target.value))}
              />
            </div>
            <Button onClick={handleFetchLowStock} disabled={threshold <= 0}>
              Fetch
            </Button>
            {lowStockResults.length > 0 && (
              <div className="overflow-x-auto mt-4">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Medicine | Identifier</TableHead>
                      <TableHead>Quantity in Stock</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {lowStockResults.map((unit) => (
                      <TableRow key={unit.medicine.identifier}>
                        <TableCell>
                          {unit.medicine.name +
                            " | " +
                            unit.medicine.identifier}
                        </TableCell>
                        <TableCell>{unit.quantity}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
      {/* Expiry Dialog */}
      <Dialog open={showExpiryDialog} onOpenChange={setShowExpiryDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Medicines Expiring On or After</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="block mb-1 text-sm">Date</label>
              <Input
                type="date"
                value={expiryDate}
                onChange={(e) => setExpiryDate(e.target.value)}
              />
            </div>
            <Button onClick={handleFetchExpiry} disabled={!expiryDate}>
              Fetch
            </Button>
            {expiryResults.length > 0 && (
              <div className="overflow-x-auto mt-4">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Medicine | Identifier</TableHead>
                      <TableHead>Expiry Date</TableHead>
                      <TableHead>Quantity in Stock</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {expiryResults.map((unit) => (
                      <TableRow key={unit.medicine.identifier}>
                        <TableCell>
                          {unit.medicine.name +
                            " | " +
                            unit.medicine.identifier}
                        </TableCell>
                        <TableCell>{unit.medicine.expiry_date}</TableCell>
                        <TableCell>{unit.quantity}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
      {/* Medicines Table */}
      {inventory && (
        <div className="overflow-x-auto mt-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Medicine | Identifier</TableHead>
                <TableHead>Vendor</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Quantity in Stock</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {inventory.map((unit) => (
                <TableRow key={unit.medicine.identifier}>
                  <TableCell>
                    {unit.medicine.name + " | " + unit.medicine.identifier}
                  </TableCell>
                  <TableCell>
                    {unit.medicine.vendor?.name || "—"}
                  </TableCell>
                  <TableCell>
                    ₹{unit.medicine.price}
                  </TableCell>
                  <TableCell>{unit.quantity}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
