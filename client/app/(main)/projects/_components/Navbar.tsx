export default function Navbar() {
  return (
    <header className="border-b border-background-3 bg-background/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-foreground-3">
            IRAObserver
          </p>
          <h1 className="text-2xl font-semibold text-foreground">
            Project collection
          </h1>
        </div>
        <div className="text-right text-sm text-foreground-3">
          <p>Last sync: 5 min ago</p>
          <p>6 active projects</p>
        </div>
      </div>
    </header>
  );
}
