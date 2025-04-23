"use client";

import * as React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";

export default function Page() {
  const [vendors, setVendors] = React.useState<
    { vendor_id: string; name: string; contact_info: string }[]
  >([]);
  const [open, setOpen] = React.useState(false);
  const [vendorId, setVendorId] = React.useState("");
  const [name, setName] = React.useState("");
  const [contact, setContact] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const loadVendors = React.useCallback(async () => {
    const data = await fetchVendors();
    setVendors(data);
  }, []);

  React.useEffect(() => {
    loadVendors();
  }, [loadVendors]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await submitVendor({ vendorId, name, contact });
      setVendorId("");
      setName("");
      setContact("");
      setOpen(false);
      await loadVendors();
    } catch (err) {
      // handle error as needed
    }
    setLoading(false);
  };

  // Placeholder API functions
  async function fetchVendors(): Promise<
    {
      vendor_id: string;
      name: string;
      contact_info: string;
    }[]
  > {
    const res = await fetch("http://localhost:5000/vendors");
    const data = await res.json();
    return data["vendors"];
  }

  async function submitVendor(data: {
    vendorId: string;
    name: string;
    contact: string;
  }) {
    // Replace with actual API call
    const req_object = {
      vendor_id: data.vendorId,
      name: data.name,
      contact_info: data.contact,
    };
    const response = await fetch("http://localhost:5000/vendors/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req_object),
    });
    if (response.status != 201) {
      console.log("error");
    } else {
      const vendors = await fetchVendors();
      setVendors(vendors);
    }
  }
  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 border rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-4">Vendors</h1>
      <div className="mb-6">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => setOpen(true)}>Add Vendor</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Vendor</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="vendorId">Vendor ID</Label>
                <Input
                  id="vendorId"
                  value={vendorId}
                  onChange={(e) => setVendorId(e.target.value)}
                  required
                  placeholder="Enter unique vendor ID"
                />
              </div>
              <div>
                <Label htmlFor="name">Vendor Name</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  placeholder="Enter vendor name"
                />
              </div>
              <div>
                <Label htmlFor="contact">Contact Info</Label>
                <Input
                  id="contact"
                  value={contact}
                  onChange={(e) => setContact(e.target.value)}
                  required
                  placeholder="Enter contact info"
                />
              </div>
              <Button type="submit" disabled={loading}>
                {loading ? "Submitting..." : "Submit"}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>
      <div>
        {vendors.length === 0 ? (
          <div>No vendors found.</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Vendor ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Contact</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {vendors &&
                vendors.map((v) => (
                  <TableRow key={v.vendor_id}>
                    <TableCell>{v.vendor_id}</TableCell>
                    <TableCell>{v.name}</TableCell>
                    <TableCell>{v.contact_info}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
