"use client";

import { useEffect, useState } from "react";

export default function CallbackPage() {
    const [msg, setMsg] = useState("Completing login...");

    useEffect(() => {
        const run = async () => {
            const params = new URLSearchParams(window.location.search);
            const code = params.get("code");
            if (!code) {
                setMsg("No code returned.");
                return;
            }

            const codeVerifier = sessionStorage.getItem("pkce_verifier");
            if (!codeVerifier) {
                setMsg("Missing PKCE verifier.");
                return;
            }

            const apiBase = process.env.NEXT_PUBLIC_API_BASE!;
            const res = await fetch(`${apiBase}/auth/google/callback`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code, code_verifier: codeVerifier, org_name: "Founder Org" }),
            });

            if (!res.ok) {
                setMsg("Auth failed.");
                return;
            }

            const data = await res.json();
            localStorage.setItem("jarvis_jwt", data.access_token);

            window.location.href = "/dashboard";
        };

        run().catch(() => setMsg("Callback error."));
    }, []);

    return <main style={{ padding: 24 }}>{msg}</main>;
}
