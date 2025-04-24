"use client";
import { useEffect, useState } from "react";
// shadcn/ui imports
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
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
type Order = {
  name: string;
  identifier: string;
  batch: Batch;
  expiry_date: string;
  price: number;
  order_id: string;
  vendor: Vendor;
  quantity: number;
  volume: number; // Add this property if not already present
};

export default function Page({ params }: { params: { id: string } }) {
  const { id } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [approvedOrders, setApprovedOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [approvedLoading, setApprovedLoading] = useState(true);
  const [dialogOrder, setDialogOrder] = useState<Order | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  // Fetch pending orders
  const fetchPendingOrders = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/vendors/${id}/orders`);
      const data: Order[] = await res.json();
      setOrders(data);
    } catch (e) {
      setOrders([]);
    }
    setLoading(false);
  };

  // Fetch approved orders
  const fetchApprovedOrders = async () => {
    setApprovedLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/vendors/${id}/orders?type=fulfilled`);
      const data: Order[] = await res.json();
      setApprovedOrders(data);
    } catch (e) {
      setApprovedOrders([]);
    }
    setApprovedLoading(false);
  };

  useEffect(() => {
    fetchPendingOrders();
    fetchApprovedOrders();
  }, [id]);

  async function handleOrderAction(orderId: string, action: "approve" | "deny") {
    setActionLoading(true);
    try {
      await fetch(`http://localhost:5000/vendors/${id}/orders/process?order_id=${orderId}&action=${action}`, {
        method: "GET",
      });
      setDialogOrder(null);
      // Refresh both tables
      await Promise.all([fetchPendingOrders(), fetchApprovedOrders()]);
    } catch (e) {
      // handle error if needed
    }
    setActionLoading(false);
  }

  return (
    <Card className="max-w-4xl mx-auto mt-10 shadow-lg">
      <CardHeader>
        <CardTitle>
          <h2 className="text-2xl font-bold">
            Pending Orders for Vendor: {id}
          </h2>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Pending Orders Table */}
        {loading ? (
          <div className="space-y-2">
            <Skeleton className="h-8 w-1/3" />
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
          </div>
        ) : orders.length === 0 ? (
          <p className="text-muted-foreground">No pending orders.</p>
        ) : (
          <>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order ID</TableHead>
                  <TableHead>Item</TableHead>
                  <TableHead>Quantity</TableHead>
                  <TableHead>Value</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.map((order) => (
                  <TableRow key={order.order_id}>
                    <TableCell>{order.order_id}</TableCell>
                    <TableCell>{order.name + " | " + order.identifier}</TableCell>
                    <TableCell>{order.quantity}</TableCell>
                    <TableCell>{order.quantity * order.price}</TableCell>
                    <TableCell>
                      <Dialog open={dialogOrder?.order_id === order.order_id} onOpenChange={open => setDialogOrder(open ? order : null)}>
                        <DialogTrigger asChild>
                          <Button variant="outline" size="sm">Review</Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Approve or Disapprove Order</DialogTitle>
                          </DialogHeader>
                          <div className="mb-4">
                            <div><b>Order ID:</b> {order.order_id}</div>
                            <div><b>Item:</b> {order.name} | {order.identifier}</div>
                            <div><b>Quantity:</b> {order.quantity}</div>
                            <div><b>Batch:</b> {order.batch?.batch_number}</div>
                            <div><b>Expiry:</b> {order.expiry_date}</div>
                            <div><b>Price:</b> ₹{order.price}</div>
                          </div>
                          <DialogFooter>
                            <Button
                              variant="destructive"
                              disabled={actionLoading}
                              onClick={() => handleOrderAction(order.order_id, "deny")}
                            >
                              Disapprove
                            </Button>
                            <Button
                              disabled={actionLoading}
                              onClick={() => handleOrderAction(order.order_id, "approve")}
                            >
                              Approve
                            </Button>
                          </DialogFooter>
                        </DialogContent>
                      </Dialog>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </>
        )}

        {/* Approved Orders Table */}
        <div className="mt-12">
          <h3 className="text-xl font-semibold mb-4">Approved Orders</h3>
          {approvedLoading ? (
            <div className="space-y-2">
              <Skeleton className="h-8 w-1/3" />
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
            </div>
          ) : approvedOrders.length === 0 ? (
            <p className="text-muted-foreground">No approved orders.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order ID</TableHead>
                  <TableHead>Item</TableHead>
                  <TableHead>Quantity</TableHead>
                  <TableHead>Value</TableHead>
                  {/* ...add more columns as needed */}
                </TableRow>
              </TableHeader>
              <TableBody>
                {approvedOrders.map((order) => (
                  <TableRow key={order.order_id}>
                    <TableCell>{order.order_id}</TableCell>
                    <TableCell>{order.name + " | " + order.identifier}</TableCell>
                    <TableCell>{order.quantity}</TableCell>
                    <TableCell>{order.quantity * order.price}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
