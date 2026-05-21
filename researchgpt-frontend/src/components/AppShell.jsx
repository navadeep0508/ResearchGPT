import { Link, NavLink } from "react-router-dom";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "R" },
  { href: "/history", label: "History", icon: "H" },
];

export default function AppShell({ children, title, subtitle, actions }) {
  function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-white/10 bg-slate-950 px-5 py-6 text-white lg:block">
        <Link to="/dashboard" className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-lg bg-indigo-500 font-bold">
            RG
          </span>
          <span>
            <span className="block text-lg font-semibold">ResearchGPT</span>
            <span className="text-xs text-slate-400">AI research workspace</span>
          </span>
        </Link>

        <nav className="mt-10 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-white text-slate-950"
                    : "text-slate-300 hover:bg-white/10 hover:text-white"
                }`
              }
            >
              <span className="grid h-8 w-8 place-items-center rounded-md bg-slate-800 text-xs text-white">
                {item.icon}
              </span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-6 left-5 right-5 rounded-lg border border-white/10 bg-white/5 p-4">
          <p className="text-sm font-medium">Private document Q&A</p>
          <p className="mt-1 text-xs leading-5 text-slate-400">
            Upload PDFs, ask grounded questions, and revisit previous answers.
          </p>
        </div>
      </aside>

      <main className="min-h-screen bg-slate-100 lg:ml-72">
        <header className="border-b border-slate-200 bg-white/90 px-5 py-4 backdrop-blur sm:px-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-indigo-600">
                ResearchGPT
              </p>
              <h1 className="mt-1 text-2xl font-semibold text-slate-950 sm:text-3xl">
                {title}
              </h1>
              {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
            </div>

            <div className="flex items-center gap-3">
              {actions}
              <button
                onClick={logout}
                className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <div className="px-5 py-6 sm:px-8">{children}</div>
      </main>
    </div>
  );
}
