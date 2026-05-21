import { useMemo, useState } from "react";
import AppShell from "../components/AppShell";
import LoadingSpinner from "../components/LoadingSpinner";
import MarkdownText from "../components/MarkdownText";
import API from "../services/api";

const demoAnswer = `## Summary
ResearchGPT found three themes across the uploaded paper:

- **Retrieval improves answer quality** by grounding the model in PDF chunks.
- The system separates upload, embedding, search, and answer generation.
- Next improvements should include citations, streaming responses, and richer file management.

Use this answer as a recruiter-friendly demo of Markdown rendering.`;

export default function Dashboard() {
  const demoMode = useMemo(
    () => new URLSearchParams(window.location.search).get("demo") === "1",
    []
  );
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState(
    demoMode ? "What are the key findings from this research paper?" : ""
  );
  const [answer, setAnswer] = useState(demoMode ? demoAnswer : "");
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(
    demoMode ? "demo-paper.pdf is indexed and ready for questions." : ""
  );
  const [error, setError] = useState("");

  async function handleUpload() {
    if (!file) {
      setError("Please select a PDF before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setError("");
      setLoading(true);

      await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setUploadStatus(`${file.name} is indexed and ready for questions.`);
    } catch {
      setError("Upload failed. Please try again with a PDF file.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk() {
    if (!question.trim()) {
      setError("Ask a question about the uploaded document.");
      return;
    }

    try {
      setError("");
      setLoading(true);

      const response = await API.post("/chat", {
        question,
      });

      setAnswer(response.data.generated_answer);
    } catch {
      setError("Question failed. Confirm the API is running and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell
      title="Dashboard"
      subtitle="Upload research papers and ask grounded questions in one focused workspace."
    >
      <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
        <section className="space-y-6">
          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold text-slate-950">Upload PDF</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Add a paper to create searchable context.
                </p>
              </div>
              <span className="rounded-md bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
                PDF
              </span>
            </div>

            <label className="mt-5 flex cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-slate-50 px-4 py-8 text-center transition hover:border-indigo-300 hover:bg-indigo-50/50">
              <input
                type="file"
                accept=".pdf"
                onChange={(event) => setFile(event.target.files[0])}
                className="sr-only"
              />
              <span className="text-sm font-semibold text-slate-800">
                {file ? file.name : "Choose a PDF"}
              </span>
              <span className="mt-1 text-xs text-slate-500">
                Files are embedded for semantic search.
              </span>
            </label>

            <button
              onClick={handleUpload}
              disabled={loading}
              className="mt-4 w-full rounded-lg bg-slate-950 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? <LoadingSpinner label="Uploading" /> : "Upload and index"}
            </button>

            {uploadStatus && (
              <div className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-800">
                {uploadStatus}
              </div>
            )}
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">Session</h2>
            <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-slate-500">Status</p>
                <p className="mt-1 font-semibold text-slate-950">
                  {uploadStatus ? "Ready" : "Waiting"}
                </p>
              </div>
              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-slate-500">Mode</p>
                <p className="mt-1 font-semibold text-slate-950">RAG Q&A</p>
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 p-5">
            <h2 className="text-lg font-semibold text-slate-950">Ask Questions</h2>
            <p className="mt-1 text-sm text-slate-500">
              Answers render Markdown for readable summaries, bullets, and code.
            </p>
          </div>

          <div className="space-y-5 p-5">
            <div className="flex justify-end">
              <div className="max-w-2xl rounded-lg bg-indigo-600 px-4 py-3 text-sm leading-6 text-white shadow-sm">
                {question || "Ask a question about the document..."}
              </div>
            </div>

            {answer && (
              <div className="flex justify-start">
                <div className="max-w-3xl rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 shadow-sm">
                  <div className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    AI Answer
                  </div>
                  <MarkdownText text={answer} />
                </div>
              </div>
            )}

            {loading && (
              <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                <LoadingSpinner label="Generating answer" />
              </div>
            )}

            {error && (
              <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                {error}
              </div>
            )}

            <div className="rounded-lg border border-slate-200 bg-white p-3">
              <textarea
                value={question}
                placeholder="Ask a question about the document..."
                className="h-28 w-full resize-none rounded-md border-0 p-3 text-sm text-slate-800 outline-none placeholder:text-slate-400"
                onChange={(event) => setQuestion(event.target.value)}
              />
              <div className="flex items-center justify-between border-t border-slate-100 pt-3">
                <span className="text-xs text-slate-500">Grounded by your uploaded PDF</span>
                <button
                  onClick={handleAsk}
                  disabled={loading}
                  className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Ask AI
                </button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
