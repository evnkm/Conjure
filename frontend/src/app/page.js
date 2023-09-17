import Interface from "@/components/Interface";

export default function Home() {
  return (
    <div>
      <h1 style={{ fontSize: "4rem", fontFamily: "inherit", paddingLeft:"50px", backgroundColor: "#5FA5FA", color:"white" }}>conjure</h1>
    <main className="w-full h-full min-h-screen flex flex-row bg-white">
      <Interface />
    </main>
    </div>
  );
}
