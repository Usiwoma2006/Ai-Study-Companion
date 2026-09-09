"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useGoogleLogin } from "@react-oauth/google";
import { useAuth } from "@/context/AuthContext";
import styles from "./signup.module.css";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const { signup, googleLogin } = useAuth();
  const router = useRouter();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await signup(email, password);
      router.push("/dashboard");
    } catch (err) {
      setError(err.message || "Something went wrong. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  const handleGoogleSignup = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (response) => {
      setError("");
      try {
        await googleLogin(response.code);
        router.push("/dashboard");
      } catch (err) {
        setError(err.message || "Google sign-in failed. Try again.");
      }
    },
    onError: () => {
      setError("Google sign-in failed. Try again.");
    },
  });

  return (
    <div className={styles.wrapper}>
      <form className={styles.card} onSubmit={handleSubmit}>
        <h1 className={styles.title}>Sign up</h1>

        {error && <p className={styles.error}>{error}</p>}

        <div className={styles.field}>
          <label className={styles.label} htmlFor="email">Email</label>
          <input
            id="email"
            className={styles.input}
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="password">Password</label>
          <input
            id="password"
            className={styles.input}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button className={styles.button} type="submit" disabled={submitting}>
          {submitting ? "Signing up..." : "Sign up"}
        </button>

        <div className={styles.divider}>or</div>

        <button
          type="button"
          className={styles.googleButton}
          onClick={() => handleGoogleSignup()}
        >
          Continue with Google
        </button>

        <p className={styles.footerText}>
          Already have an account?{" "}
          <a className={styles.footerLink} href="/login">Log in</a>
        </p>
      </form>
    </div>
  );
}