import { createFileRoute } from "@tanstack/react-router";
import { getSnapshot } from "@/lib/star/snapshots.server";
export const Route = createFileRoute("/api/snapshots/$id")({ server: { handlers: { GET: ({ params }) => getSnapshot(params.id) } } });
