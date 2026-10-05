import { createFileRoute } from "@tanstack/react-router";
import { health } from "@/lib/star/snapshots.server";
export const Route = createFileRoute("/api/health")({ server: { handlers: { GET: health } } });
