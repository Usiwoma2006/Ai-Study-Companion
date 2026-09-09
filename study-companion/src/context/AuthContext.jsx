"use client";

import { createContext, useContext, useState, useEffect } from "react";

// 1. Create the context object — this is the "box"
const AuthContext = createContext(null);

// 2. This is the provider — it wraps your whole app (in layout.js)
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // true while we check localStorage on first load

  // Runs once when the app first mounts — check if tokens already exist
  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      // We have a token from a previous session.
      // For now, just decode basic info or mark as logged in.
      // (Later we might fetch /api/auth/user/ to get fresh user data.)
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
    }
    setLoading(false); // done checking, safe to render app now
  }, []);

  async function login(email, password) {
    const res = await fetch("http://localhost:8000/api/auth/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || "Login failed");
    }

    const data = await res.json();
    // data should contain access + refresh tokens (confirm exact field names from your Postman test)
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);

    // If your login response includes user info, store it too.
    // If not, we'll need a separate step — flag this, see note below.
    if (data.user) {
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
    } else {
      setUser({ email }); // fallback minimal user object
    }
  }

  async function signup(email, password) {
    const res = await fetch("http://localhost:8000/api/auth/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || "Signup failed");
    }

    const data = await res.json();
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);

    if (data.user) {
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
    } else {
      setUser({ email });
    }
  }
async function googleLogin(code) {
  const res = await fetch("http://localhost:8000/api/auth/google/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Google sign-in failed");
  }

  const data = await res.json();
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);

  if (data.user) {
    localStorage.setItem("user", JSON.stringify(data.user));
    setUser(data.user);
  }
}
  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setUser(null);
  }

  const value = { user, loading, login, signup, logout, googleLogin };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// 3. The hook every component will actually use
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
}