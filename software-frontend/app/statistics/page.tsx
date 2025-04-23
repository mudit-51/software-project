"use client";
import { useEffect, useState } from "react";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import React from "react";

type Batch = {
  batch_number: string;
  expiry_date: string;
};
type Vendor = {
  vendor_id: string;
  name: string;
  contact_info: string;
};
type MedicineStatistics = {
  name: string;
  identifier: string;
  batch: Batch;
  expiry_date: string;
  price: number;
  vendor: Vendor;
  quantity_sold: number;
  value_sold: number;
};

type SalesEntry = {
  name: string;
  volume: number;
  price: number;
};

type SortKey = "name" | "volume" | "value";
type SortOrder = "asc" | "desc";

type Transaction = {
  batch: Batch;
  expiry_date: string;
  identifier: string;
  name: string;
  price: number;
  quantity: number;
  total_price: number;
  vendor: Vendor;
};

export default function Page() {
  const [sales, setSales] = useState<MedicineStatistics[]>([]);
  const [transactions, setTransactions] = useState<Transaction[][]>([]);
  const [sortKey, setSortKey] = useState<SortKey>("name");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

  useEffect(() => {
    async function fetchSales() {
      const res = await fetch("http://localhost:5000/statistics");
      const data: MedicineStatistics[] = await res.json();
      setSales(data);
    }
    async function fetchTransactions() {
      const res = await fetch("http://localhost:5000/history");
      const data: Transaction[][] = await res.json();
      setTransactions(data);
    }
    fetchSales();
    fetchTransactions();
  }, []);

  const sortedSales = [...sales].sort((a, b) => {
    let aValue: string | number = "";
    let bValue: string | number = "";
    if (sortKey === "name") {
      aValue = a.name.toLowerCase();
      bValue = b.name.toLowerCase();
    } else if (sortKey === "volume") {
      aValue = a.quantity_sold;
      bValue = b.quantity_sold;
    } else if (sortKey === "value") {
      aValue = a.value_sold;
      bValue = b.value_sold;
    }
    if (aValue < bValue) return sortOrder === "asc" ? -1 : 1;
    if (aValue > bValue) return sortOrder === "asc" ? 1 : -1;
    return 0;
  });

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Sales History</h1>
      <div className="overflow-x-auto mb-10">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <Button
                  variant="ghost"
                  className="p-0"
                  onClick={() => handleSort("name")}
                >
                  Name
                  {sortKey === "name" && (sortOrder === "asc" ? " ▲" : " ▼")}
                </Button>
              </TableHead>
              <TableHead>
                <Button
                  variant="ghost"
                  className="p-0"
                  onClick={() => handleSort("volume")}
                >
                  Volume
                  {sortKey === "volume" && (sortOrder === "asc" ? " ▲" : " ▼")}
                </Button>
              </TableHead>
              <TableHead>
                <Button
                  variant="ghost"
                  className="p-0"
                  onClick={() => handleSort("value")}
                >
                  Value
                  {sortKey === "value" && (sortOrder === "asc" ? " ▲" : " ▼")}
                </Button>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedSales.map((entry, idx) => (
              <TableRow key={idx}>
                <TableCell>{entry.name}</TableCell>
                <TableCell>{entry.quantity_sold}</TableCell>
                <TableCell>₹{entry.value_sold.toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <h2 className="text-xl font-semibold mb-4">Transaction History</h2>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Quantity</TableHead>
              <TableHead>Price</TableHead>
              <TableHead>Total Price</TableHead>
              <TableHead>Batch</TableHead>
              <TableHead>Expiry</TableHead>
              <TableHead>Vendor</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions &&
              transactions.map((group, groupIdx) => (
                <React.Fragment key={groupIdx}>
                  {group.map((txn, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{txn.name}</TableCell>
                      <TableCell>{txn.quantity}</TableCell>
                      <TableCell>₹{txn.price.toLocaleString()}</TableCell>
                      <TableCell>₹{txn.total_price.toLocaleString()}</TableCell>
                      <TableCell>{txn.batch.batch_number}</TableCell>
                      <TableCell>{txn.expiry_date}</TableCell>
                      <TableCell>{txn.vendor.name}</TableCell>
                    </TableRow>
                  ))}
                  {/* Separator row between groups */}
                  {groupIdx < transactions.length - 1 && (
                    <TableRow key={`sep-${groupIdx}`}>
                      <TableCell colSpan={7}>
                        <div className="border-t border-gray-300 my-2"></div>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
