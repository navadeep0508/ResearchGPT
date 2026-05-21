import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoadingSpinner from "../components/LoadingSpinner";
import API from "../services/api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleLogin() {
    try {
      setError("");
      setLoading(true);

      const response = await API.post("/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch {
      setError("Login failed. Check your username and password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen bg-slate-950 text-white lg:grid-cols-[1.05fr_0.95fr]">
      <section className="flex min-h-[40vh] flex-col justify-between bg-[radial-gradient(circle_at_top_left,#4f46e5,transparent_30%),linear-gradient(135deg,#020617,#111827_48%,#312e81)] px-6 py-8 sm:px-10">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-lg bg-white text-sm font-bold text-slate-950">
            RG
          </span>
          <span className="text-lg font-semibold">ResearchGPT</span>
        </div>

        <div className="max-w-2xl pb-8 pt-16">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-200">
            AI research assistant
          </p>
          <h1 className="mt-4 text-4xl font-semibold leading-tight sm:text-5xl">
            Turn dense PDFs into clear, grounded answers.
          </h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-slate-300">
            Upload research papers, ask natural language questions, and keep a
            history of answers for faster review.
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center bg-slate-100 px-6 py-10 text-slate-950">
        <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-xl shadow-slate-950/10 sm:p-8">
          <div>
            <p className="text-sm font-semibold text-indigo-600">Welcome back</p>
            <h2 className="mt-2 text-2xl font-semibold">Sign in to your workspace</h2>
          </div>

          <div className="mt-6 space-y-4">
            <input
              type="text"
              placeholder="Username"
              value={username}
              className="w-full rounded-lg border border-slate-200 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100"
              onChange={(event) => setUsername(event.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              className="w-full rounded-lg border border-slate-200 px-4 py-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100"
              onChange={(event) => setPassword(event.target.value)}
            />

            {error && (
              <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                {error}
              </div>
            )}

            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full rounded-lg bg-slate-950 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? <LoadingSpinner label="Signing in" /> : "Login"}
            </button>
          </div>

          <p className="mt-6 text-center text-sm text-slate-500">
            Don't have an account?
            <Link to="/register" className="ml-1 font-semibold text-indigo-600">
              Register
            </Link>
          </p>
        </div>
      </section>
    </div>
  );
}
