export async function apiFetch(path: string, init?: RequestInit) {
    const base = process.env.NEXT_PUBLIC_API_BASE!;
    const jwt = typeof window !== "undefined" ? localStorage.getItem("jarvis_jwt") : null;

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(init?.headers as any),
    };
    if (jwt) headers["Authorization"] = `Bearer ${jwt}`;

    const res = await fetch(`${base}${path}`, { ...init, headers });
    return res;
}
