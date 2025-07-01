import profile from "./assets/images/profile.png";

const App = () => {
  return (
    <div className="h-screen w-full flex flex-col bg-neutral-900 text-white border border-white-500">
      <header className="w-full h-[7%] flex justify-center border border-red-500 ">
        <nav className="flex w-[70%] h-full justify-between items-center border border-blue-500 ">
          <div>
            <img src={profile} className="w-[80px]" />
          </div>
          <div>TEST1</div>
          <div>TEST2</div>
          <div>TEST3</div>
          <div>TEST4</div>
        </nav>
      </header>

      <main className="border bg-amber-800 border-amber-500 w-full h-screen"></main>

      <footer class="relative overflow-hidden bg-neutral-900"></footer>
    </div>
  );
};

export default App;
