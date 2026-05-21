import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import AppShell from "../components/AppShell";
import LoadingSpinner from "../components/LoadingSpinner";
import MarkdownText from "../components/MarkdownText";
import API from "../services/api";

const demoHistory = [
  {
    question: "What problem does the paper solve?",
    answer:
      "The paper proposes a retrieval-first workflow that reduces hallucination by pairing user questions with relevant PDF passages before generation.",
  },
  {
    question: "List future improvements.",
    answer:
      "- Add cited source chunks\n- Stream answers as they generate\n- Support multiple document collections\n- Add evaluation metrics",
  },
];

export default function History() {
  const demoMode = useMemo(
    () => new URLSearchParams(window.location.search).get("demo") === "1",
    []
  );
  const [history, setHistory] = useState(demoMode ? demoHistory : []);
  const [loading, setLoading] = useState(!demoMode);
  const [error, setError] = useState("");

  async function fetchHistory() {
    try {
      const response = await API.get("/history");
      setHistory(response.data.history);
    } catch {
      setError("Failed to load history.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (demoMode) {
      return undefined;
    }

    const timer = window.setTimeout(fetchHistory, 0);
    return () => window.clearTimeout(timer);
  }, [demoMode]);

  return (
    <AppShell
      title="History"
      subtitle="Review previous research questions and generated answers."
      actions={
        <Link
          to="/dashboard"
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500"
        >
          New question
        </Link>
      }
    >
      <div className="space-y-4">
        {loading && (
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <LoadingSpinner label="Loading history" />
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
            {error}
          </div>
        )}

        {!loading && history.length === 0 && !error && (
          <div className="rounded-lg border border-slate-200 bg-white p-8 text-center shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">No chat history yet</h2>
            <p className="mt-2 text-sm text-slate-500">
              Ask your first question to start building a searchable research trail.
            </p>
          </div>
        )}

        {history.map((chat, index) => (
          <article
            key={`${chat.question}-${index}`}
            className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="flex flex-col gap-4 lg:flex-row">
              <div className="lg:w-72">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-indigo-600">
                  Question
                </p>
                <p className="mt-2 text-sm font-medium leading-6 text-slate-950">
                  {chat.question}
                </p>
              </div>

              <div className="min-w-0 flex-1 rounded-lg bg-slate-50 p-4">
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Answer
                </p>
                <MarkdownText text={chat.answer} />
              </div>
            </div>
          </article>
        ))}
      </div>
    </AppShell>
  );
}
