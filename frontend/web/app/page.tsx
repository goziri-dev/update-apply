import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex flex-col items-center justify-center gap-3">
        <h1>Welcome to UpdateApply</h1>
        <Link href={"/dashboard"}>
          <button className="btn">Go to Dashboard</button>
        </Link>
      </main>
    </div>
  );
}
