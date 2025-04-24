import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
// Import shadcn components
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Medicine Shop Management System",
};

// Navbar component using shadcn Button and utility classes
function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between px-6 py-4 border-b bg-white">
      <div className="text-xl font-bold">M.SaaS</div>
      <div className="flex gap-4">
        <Link href="/inventory">
          <Button variant="ghost" className="font-normal">
            Inventory
          </Button>
        </Link>
        <Link href="/medicines">
          <Button variant="ghost" className="font-normal">
            Medicines
          </Button>
        </Link>
        <Link href="/sales">
          <Button variant="ghost" className="font-normal">
            Process Customers
          </Button>
        </Link>
        <Link href="/statistics">
          <Button variant="ghost" className="font-normal">
            Sales Statistics
          </Button>
        </Link>
        <Link href="/vendors">
          <Button variant="ghost" className="font-normal">
            Vendor Management
          </Button>
        </Link>
      </div>
    </nav>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        {children}
        <Toaster />
      </body>
    </html>
  );
}
