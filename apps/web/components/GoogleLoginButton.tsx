"use client";

import { randomString, sha256 } from "@/lib/pkce";

export default function GoogleLoginButton() {
    const onLogin = async () => {
        const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!;
        const redirectUri = process.env.NEXT_PUBLIC_GOOGLE_REDIRECT_URI!; // http://localhost:3000/callback

        const codeVerifier = randomString(64);
        const codeChallenge = await sha256(codeVerifier);

        sessionStorage.setItem("pkce_verifier", codeVerifier);

        const scopes = [
            "openid",
            "email",
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.compose",
            "https://www.googleapis.com/auth/calendar.readonly",
        ].join(" ");

        const params = new URLSearchParams({
            client_id: clientId,
            redirect_uri: redirectUri,
            response_type: "code",
            scope: scopes,
            access_type: "offline",
            prompt: "consent",
            code_challenge: codeChallenge,
            code_challenge_method: "S256",
        });

        window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
    };

    return (
        <button
            onClick={onLogin}
            className="px-4 py-2 rounded bg-black text-white"
        >
            Continue with Google
        </button>
    );
}
