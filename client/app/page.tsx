
import Image from "next/image";

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
            Ingresa tu codigo y nombre para unirte a la sala.
          </h1>
          <p className="max-w-md text-base text-foreground-2">
            No es un login. Solo necesitamos un codigo de acceso y el nombre que
            quieres mostrar al resto del equipo.
          </p>
          <div className="flex items-center gap-2 text-sm text-foreground-3">
            <span className="inline-flex h-2 w-2 rounded-full bg-observer" />
            Tu actividad se sincroniza al instante.
          </div>
        </section>

        <section className="w-full max-w-md rounded-2xl border border-observer/30 bg-background-2/80 p-6 shadow-[0_24px_60px_-40px_rgba(76,29,149,0.55)] backdrop-blur">
          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-foreground">
              Acceder a una sala
            </h2>
            <p className="text-sm text-foreground-3">
              Completa los datos para continuar.
            </p>
          </div>

          <form className="mt-6 space-y-4">
            <label className="block space-y-2 text-sm text-foreground-2">
              Codigo de la sala
              <input
                type="text"
                placeholder="Ej: OBS-204"
                className="w-full rounded-xl border border-observer/30 bg-background px-4 py-3 text-sm text-foreground placeholder:text-foreground-3 focus:border-observer focus:outline-none focus:ring-2 focus:ring-observer/30"
              />
            </label>

            <label className="block space-y-2 text-sm text-foreground-2">
              Nombre de usuario
              <input
                type="text"
                placeholder="Tu nombre visible"
                className="w-full rounded-xl border border-observer/30 bg-background px-4 py-3 text-sm text-foreground placeholder:text-foreground-3 focus:border-observer focus:outline-none focus:ring-2 focus:ring-observer/30"
              />
            </label>

            <button
              type="button"
              className="mt-2 w-full rounded-xl bg-observer px-4 py-3 text-sm font-semibold text-background transition hover:bg-observer-2"
            >
              Continuar
            </button>
          </form>

          <div className="mt-6 rounded-xl border border-dashed border-observer/30 bg-background/40 px-4 py-3">
            <p className="text-xs text-observer-3">Crear sala</p>
          </div>
        </section>
      </div>
    </main>
  );
}
