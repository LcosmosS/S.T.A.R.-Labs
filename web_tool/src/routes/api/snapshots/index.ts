import { createFileRoute } from "@tanstack/react-router";
import { listSnapshots, saveSnapshot } from "@/lib/star/snapshots.server";
export const Route = createFileRoute("/api/snapshots/")({ server: { handlers: { GET: listSnapshots, POST: ({ request }) => saveSnapshot(request) } }, });
