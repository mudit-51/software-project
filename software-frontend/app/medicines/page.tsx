"use client";
import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useRouter } from "next/navigation";
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  SortingState,
  getFilteredRowModel,
  ColumnFiltersState,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ChevronDown, ChevronUp, Search } from "lucide-react";

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

// Column definitions for the data table
const columns: ColumnDef<Medicine>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="flex items-center gap-1"
        >
          Name
          {column.getIsSorted() === "asc" ? (
            <ChevronUp className="h-4 w-4" />
          ) : column.getIsSorted() === "desc" ? (
            <ChevronDown className="h-4 w-4" />
          ) : null}
        </Button>
      );
    },
  },
  {
    accessorKey: "batch.batch_number",
    header: "Batch",
    cell: ({ row }) => row.original.batch.batch_number,
  },
  {
    accessorKey: "expiry_date",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="flex items-center gap-1"
        >
          Expiry Date
          {column.getIsSorted() === "asc" ? (
            <ChevronUp className="h-4 w-4" />
          ) : column.getIsSorted() === "desc" ? (
            <ChevronDown className="h-4 w-4" />
          ) : null}
        </Button>
      );
    },
  },
  {
    accessorKey: "price",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="flex items-center gap-1"
        >
          Price
          {column.getIsSorted() === "asc" ? (
            <ChevronUp className="h-4 w-4" />
          ) : column.getIsSorted() === "desc" ? (
            <ChevronDown className="h-4 w-4" />
          ) : null}
        </Button>
      );
    },
    cell: ({ row }) => {
      const price = parseFloat(row.getValue("price"));
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(price);
    },
  },
  {
    accessorKey: "vendor.name",
    header: "Vendor",
    cell: ({ row }) => (
      <div>
        {row.original.vendor.vendor_id} | {row.original.vendor.name}
      </div>
    ),
  },
];

// Data Table Component
function DataTable({ data, columns }: { data: Medicine[]; columns: ColumnDef<Medicine>[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState("");

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center">
        <div className="relative flex-1">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search medicines..."
            value={globalFilter ?? ""}
            onChange={(e) => setGlobalFilter(e.target.value)}
            className="pl-8"
          />
        </div>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default function Page() {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [addingBatch, setAddingBatch] = useState(false);

  // Form state
  const [form, setForm] = useState({
    name: "",
    batch_number: "",
    expiry_date: "",
    price: "",
    vendor_id: "",
    new_batch_number: "",
    new_batch_expiry: "",
  });

  const router = useRouter();

  useEffect(() => {
    fetch("http://localhost:5000/medicines")
      .then((res) => res.json())
      .then((data) => {
        setMedicines(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
    fetch("http://localhost:5000/batches")
      .then((res) => res.json())
      .then(setBatches);
    fetch("http://localhost:5000/vendors")
      .then((res) => res.json())
      .then((data) => {
        setVendors(data["vendors"]);
      });
  }, []);

  const handleFormChange = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleAddMedicine = async () => {
    let batchToUse = form.batch_number;
    // If adding new batch, create it first
    if (addingBatch && form.new_batch_number && form.new_batch_expiry) {
      const resp = await fetch("http://localhost:5000/batches/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          batch_number: form.new_batch_number,
          expiry_date: form.new_batch_expiry,
        }),
      });
      if (resp.ok) {
        batchToUse = form.new_batch_number;
        // Refresh batches
        const newBatches = await fetch("http://localhost:5000/batches").then(
          (r) => r.json()
        );
        setBatches(newBatches);
      } else {
        alert("Failed to add batch");
        return;
      }
    }
    // Add medicine
    const resp = await fetch("http://localhost:5000/medicines/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        batch_number: batchToUse,
        expiry_date: form.expiry_date,
        price: parseFloat(form.price),
        vendor_id: form.vendor_id,
      }),
    });
    if (resp.ok) {
      setOpen(false);
      setForm({
        name: "",
        batch_number: "",
        expiry_date: "",
        price: "",
        vendor_id: "",
        new_batch_number: "",
        new_batch_expiry: "",
      });
      setAddingBatch(false);
      // Refresh medicines
      setLoading(true);
      fetch("http://localhost:5000/medicines")
        .then((res) => res.json())
        .then((data) => {
          setMedicines(data);
          setLoading(false);
        });
    } else {
      alert("Failed to add medicine");
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Medicines</CardTitle>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-full mb-2" />
          <Skeleton className="h-8 w-full mb-2" />
          <Skeleton className="h-8 w-full mb-2" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Medicines</CardTitle>
        <Button onClick={() => setOpen(true)}>Add Medicine</Button>
      </CardHeader>
      <CardContent>
        {medicines.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            No medicines found.
          </div>
        ) : (
          <DataTable columns={columns} data={medicines} />
        )}
      </CardContent>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Medicine</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label>Name</Label>
              <Input
                value={form.name}
                onChange={(e) => handleFormChange("name", e.target.value)}
                placeholder="Medicine name"
              />
            </div>
            <div>
              <Label>Batch</Label>
              {!addingBatch ? (
                <div className="flex gap-2">
                  <Select
                    value={form.batch_number}
                    onValueChange={(val) =>
                      handleFormChange("batch_number", val)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select batch" />
                    </SelectTrigger>
                    <SelectContent>
                      {batches.map((b) => (
                        <SelectItem key={b.batch_number} value={b.batch_number}>
                          {b.batch_number} (exp: {b.expiry_date})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setAddingBatch(true)}
                  >
                    Add New Batch
                  </Button>
                </div>
              ) : (
                <div className="space-y-2">
                  <Input
                    value={form.new_batch_number}
                    onChange={(e) =>
                      handleFormChange("new_batch_number", e.target.value)
                    }
                    placeholder="Batch number"
                  />
                  <Input
                    type="date"
                    value={form.new_batch_expiry}
                    onChange={(e) =>
                      handleFormChange("new_batch_expiry", e.target.value)
                    }
                    placeholder="Expiry date"
                  />
                  <div className="flex gap-2">
                    <Button
                      type="button"
                      onClick={() => setAddingBatch(false)}
                      variant="secondary"
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              )}
            </div>
            <div>
              <Label>Expiry Date</Label>
              <Input
                type="date"
                value={form.expiry_date}
                onChange={(e) =>
                  handleFormChange("expiry_date", e.target.value)
                }
                placeholder="Expiry date"
              />
            </div>
            <div>
              <Label>Price</Label>
              <Input
                type="number"
                value={form.price}
                onChange={(e) => handleFormChange("price", e.target.value)}
                placeholder="Price"
                min="0"
              />
            </div>
            <div>
              <Label>Vendor</Label>
              <div className="flex gap-2">
                <Select
                  value={form.vendor_id}
                  onValueChange={(val) => handleFormChange("vendor_id", val)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select vendor" />
                  </SelectTrigger>
                  <SelectContent>
                    {vendors.map((v) => (
                      <SelectItem key={v.vendor_id} value={v.vendor_id}>
                        {v.name} ({v.vendor_id})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setOpen(false);
                    router.push("/vendors");
                  }}
                >
                  Add New Vendor
                </Button>
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button
              onClick={handleAddMedicine}
              disabled={
                !form.name ||
                (!form.batch_number &&
                  !(
                    addingBatch &&
                    form.new_batch_number &&
                    form.new_batch_expiry
                  )) ||
                !form.expiry_date ||
                !form.price ||
                !form.vendor_id
              }
            >
              Add
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
}