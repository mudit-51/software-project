import { redirect } from "next/navigation";

export default function Home() {
  redirect("/medicines");
  return null;
}
