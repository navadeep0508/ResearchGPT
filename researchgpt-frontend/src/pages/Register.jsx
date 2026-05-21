import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

export default function Register() {

  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  async function handleRegister() {

    try {

      await API.post(
        "/auth/register",
        {
          username,
          password,
        }
      );

      alert("Registration successful!");

      navigate("/");

    } catch (error) {

      alert("Registration failed");
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">

      <div className="bg-white p-8 rounded-xl shadow-lg w-96">

        <h1 className="text-3xl font-bold mb-6 text-center">
          Register
        </h1>

        <input
          type="text"
          placeholder="Username"
          className="w-full border p-3 mb-4 rounded"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-3 mb-4 rounded"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleRegister}
          className="w-full bg-black text-white p-3 rounded"
        >
          Register
        </button>

        <p className="mt-4 text-center">
          Already have an account?

          <a
            href="/"
            className="text-blue-500 ml-1"
          >
            Login
          </a>
        </p>

      </div>

    </div>
  );
}