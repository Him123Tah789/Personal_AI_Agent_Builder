import GoogleLoginButton from "@/components/GoogleLoginButton";

export default function LoginPage() {
    return (
        <main style={{ padding: 24 }}>
            <h1>Sign in</h1>
            <p>Connect your Google account to enable Gmail + Calendar.</p>
            <GoogleLoginButton />
        </main>
    );
}
