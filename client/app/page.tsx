
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex min-h-screen w-full max-w-5xl flex-col justify-center gap-10 px-6 py-16 md:flex-row md:items-center md:gap-16">
        <section className="flex-1 space-y-4">
          <div className="flex items-center gap-4">
            <Image
              src="/ira-logo.png"
              alt="IRA"
              width={200}
              height={200}
              className="h-24 w-24 rounded-3xl bg-background-2 p-3 shadow-[0_18px_40px_-30px_rgba(124,92,224,0.7)] md:h-28 md:w-28"
              priority
            />
            <p className="text-2xl font-semibold uppercase tracking-[0.25em] text-foreground md:text-3xl">
              IRAObserver
            </p>
          </div>
          <h1 className="text-3xl font-semibold leading-tight text-foreground md:text-4xl">
            Enter your room code and display name to join.
          </h1>
          <p className="max-w-md text-base text-foreground-2">
            This is not a login. We only need a room code and the name you want
            others to see.
          </p>
          <div className="flex items-center gap-2 text-sm text-foreground-3">
            <span className="inline-flex h-2 w-2 rounded-full bg-observer" />
            Your activity syncs instantly.
          </div>
        </section>

        <section className="w-full max-w-md rounded-2xl border border-observer/30 bg-background-2/80 p-6 shadow-[0_24px_60px_-40px_rgba(76,29,149,0.55)] backdrop-blur">
          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-foreground">
              Join a room
            </h2>
            <p className="text-sm text-foreground-3">
              Fill in the details to continue.
            </p>
          </div>

          <form className="mt-6 space-y-4">
            <label className="block space-y-2 text-sm text-foreground-2">
              Room code
              <input
                type="text"
                placeholder="Ex: OBS-204"
                className="w-full rounded-xl border border-observer/30 bg-background px-4 py-3 text-sm text-foreground placeholder:text-foreground-3 focus:border-observer focus:outline-none focus:ring-2 focus:ring-observer/30"
              />
            </label>

            <label className="block space-y-2 text-sm text-foreground-2">
              Display name
              <input
                type="text"
                placeholder="Your visible name"
                className="w-full rounded-xl border border-observer/30 bg-background px-4 py-3 text-sm text-foreground placeholder:text-foreground-3 focus:border-observer focus:outline-none focus:ring-2 focus:ring-observer/30"
              />
            </label>

            <Link
              href="/room"
              className="mt-2 block w-full rounded-xl bg-observer px-4 py-3 text-center text-sm font-semibold text-background transition hover:bg-observer-2"
            >
              Continue
            </Link>
          </form>

          <div className="mt-6 rounded-xl border border-dashed border-observer/30 bg-background/40 px-4 py-3">
            <Link href="/create-room" className="text-xs text-observer-3">
              Create room
            </Link>
          </div>
        </section>
      </div>
      <div className="fixed bottom-6 right-6 text-foreground-3">
        <svg
          aria-label="GitHub"
          role="img"
          viewBox="0 0 24 24"
          className="h-7 w-7"
          fill="currentColor"
        >
          <path d="M12 1.8C6.48 1.8 2 6.32 2 11.9c0 4.44 2.86 8.2 6.84 9.54.5.1.68-.22.68-.48v-1.7c-2.78.62-3.37-1.2-3.37-1.2-.46-1.18-1.12-1.5-1.12-1.5-.92-.64.08-.63.08-.63 1.02.07 1.55 1.06 1.55 1.06.9 1.56 2.36 1.1 2.94.84.1-.67.36-1.1.66-1.36-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.04-2.74-.1-.26-.46-1.3.1-2.71 0 0 .84-.27 2.74 1.05.8-.23 1.64-.34 2.48-.34s1.68.11 2.48.34c1.9-1.32 2.74-1.05 2.74-1.05.56 1.41.2 2.45.1 2.71.65.71 1.04 1.62 1.04 2.74 0 3.94-2.34 4.8-4.57 5.06.36.31.69.93.69 1.88v2.78c0 .27.18.59.69.48 3.97-1.35 6.82-5.1 6.82-9.54C22 6.32 17.52 1.8 12 1.8z" />
        </svg>
      </div>
    </main>
  );
}
