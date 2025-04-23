"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

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

type CartItem = {
  medicine: Medicine;
  quantity: number;
};

export default function Page() {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [cartCreated, setCartCreated] = useState(false);
  const [inventory, setInventory] = useState<Inventory[]>([]);
  const [selectedMedicine, setSelectedMedicine] = useState<string>("");
  const [quantity, setQuantity] = useState<number>(1);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Fetch inventory from backend
  const fetchInventory = async () => {
    const res = await fetch("http://localhost:5000/inventory");
    const data: Inventory[] = await res.json();
    setInventory(data);
  };

  const handleCreateCart = async () => {
    setCartCreated(true);
    await fetchInventory();
  };

  // Get available stock for selected medicine
  const getAvailableStock = (medicineId: string) => {
    const inv = inventory.find((i) => i.medicine.identifier === medicineId);
    // Support both id and identifier for compatibility
    if (!inv) return 0;
    // Subtract already added to cart
    const inCart = cart.find((c) => c.medicine.identifier === medicineId);
    return inv.quantity - (inCart ? inCart.quantity : 0);
  };

  const handleAddToCart = () => {
    const inv = inventory.find(
      (i) => i.medicine.identifier === selectedMedicine
    );
    if (!inv) return;
    const available = getAvailableStock(selectedMedicine);
    if (quantity > 0 && quantity <= available) {
      setCart((prev) => {
        // If already in cart, update quantity
        const idx = prev.findIndex(
          (c) => c.medicine.identifier === selectedMedicine
        );
        if (idx !== -1) {
          const updated = [...prev];
          updated[idx] = {
            ...updated[idx],
            quantity: updated[idx].quantity + quantity,
          };
          return updated;
        }
        return [...prev, { medicine: inv.medicine, quantity }];
      });
      setSelectedMedicine("");
      setQuantity(1);
      setDialogOpen(false);
    }
  };

  const handleCheckout = async () => {
    await fetch("http://localhost:5000/cart/checkout", {
      method: "POST",
      body: JSON.stringify({ items: cart }),
      headers: { "Content-Type": "application/json" },
    });
    setCart([]);
    setCartCreated(false);
  };

  // Update inventory after cart changes (to reflect available stock)
  useEffect(() => {
    if (cartCreated) fetchInventory();
    // eslint-disable-next-line
  }, [cartCreated]);

  return (
    <div className="p-8">
      {!cartCreated ? (
        <Button onClick={handleCreateCart}>Create Cart</Button>
      ) : (
        <>
          <Button onClick={() => setDialogOpen(true)} className="mb-4">
            Add Medicine
          </Button>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add Medicine to Cart</DialogTitle>
              </DialogHeader>
              <Select
                value={selectedMedicine}
                onValueChange={(val) => {
                  setSelectedMedicine(val);
                  setQuantity(1);
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select medicine" />
                </SelectTrigger>
                <SelectContent>
                  {inventory.map((inv) => {
                    const available = getAvailableStock(
                      inv.medicine.identifier
                    );
                    return (
                      <SelectItem
                        key={inv.medicine.identifier}
                        value={inv.medicine.identifier}
                        disabled={available <= 0}
                      >
                        {inv.medicine.name} ({available} in stock)
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
              <Input
                type="number"
                min={1}
                max={
                  selectedMedicine
                    ? getAvailableStock(selectedMedicine)
                    : undefined
                }
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value))}
                placeholder="Quantity"
                className="mt-2"
                disabled={!selectedMedicine}
              />
              {selectedMedicine && (
                <div className="text-xs text-muted-foreground mt-1">
                  Max: {getAvailableStock(selectedMedicine)}
                </div>
              )}
              <Button
                onClick={handleAddToCart}
                disabled={
                  !selectedMedicine ||
                  quantity < 1 ||
                  quantity > getAvailableStock(selectedMedicine)
                }
                className="mt-2"
              >
                Add
              </Button>
            </DialogContent>
          </Dialog>
          <Table className="mb-4">
            <TableHeader>
              <TableRow>
                <TableHead>Medicine</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {cart.map((item, idx) => (
                <TableRow key={idx}>
                  <TableCell>{item.medicine.name}</TableCell>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>
                    <Button
                      size="sm"
                      variant="outline"
                      className="mr-2"
                      onClick={() => {
                        setCart((prev) =>
                          prev
                            .map((c, i) =>
                              i === idx
                                ? { ...c, quantity: c.quantity - 1 }
                                : c
                            )
                            .filter((c, i) => !(i === idx && c.quantity <= 0))
                        );
                      }}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => {
                        setCart((prev) => prev.filter((_, i) => i !== idx));
                      }}
                    >
                      Remove
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Button onClick={handleCheckout} disabled={cart.length === 0}>
            Complete Transaction
          </Button>
        </>
      )}
    </div>
  );
}
