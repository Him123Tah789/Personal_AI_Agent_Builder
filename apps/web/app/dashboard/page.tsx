"use client";
import { apiFetch } from "@/lib/api";
import { useEffect, useState } from "react";

export default function DashboardPage() {
    const [health, setHealth] = useState<string>("...");

    useEffect(() => {
        apiFetch("/health")
            .then(r => r.json())
            .then(d => setHealth(JSON.stringify(d)))
            .catch(() => setHealth("error"));
    }, []);

    return (
        <main style={{ padding: 24 }}>
            <h1>Dashboard</h1>
            <p>API health: {health}</p>
            <p>Next: Integrations → Gmail/Calendar views, Chat, Approvals.</p>
        </main>
    );
}
