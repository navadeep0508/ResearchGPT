import { useState } from "react";
import API from "../services/api";

export default function Dashboard() {

  const [file, setFile] = useState(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleUpload() {

    if (!file) {
      alert("Please select a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      setLoading(true);

      await API.post(
        "/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("PDF uploaded successfully!");

    } catch (error) {

      alert("Upload failed");

    } finally {

      setLoading(false);
    }
  }

  async function handleAsk() {

    if (!question) {
      return;
    }

    try {

      setLoading(true);

      const response = await API.post(
        "/chat",
        {
          question,
        }
      );

      setAnswer(response.data.generated_answer);

    } catch (error) {

      alert("Question failed");

    } finally {

      setLoading(false);
    }
  }

  function logout() {

    localStorage.removeItem("token");

    window.location.href = "/";
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <div className="flex justify-between items-center mb-8">

        <h1 className="text-4xl font-bold">
          ResearchGPT
        </h1>

        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>

      </div>

      <div className="bg-white p-6 rounded-xl shadow mb-8">

        <h2 className="text-2xl font-semibold mb-4">
          Upload PDF
        </h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4"
        />

        <button
          onClick={handleUpload}
          className="bg-black text-white px-6 py-3 rounded"
        >
          Upload
        </button>

      </div>

      <div className="bg-white p-6 rounded-xl shadow">

        <h2 className="text-2xl font-semibold mb-4">
          Ask Questions
        </h2>

        <textarea
          placeholder="Ask a question about the document..."
          className="w-full border rounded p-4 mb-4 h-32"
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={handleAsk}
          className="bg-black text-white px-6 py-3 rounded"
        >
          Ask
        </button>

        {loading && (
          <p className="mt-4">
            Loading...
          </p>
        )}

        {answer && (
          <div className="mt-6 bg-gray-100 p-4 rounded">

            <h3 className="font-bold mb-2">
              Answer:
            </h3>

            <p>{answer}</p>

          </div>
        )}

      </div>

    </div>
  );
}