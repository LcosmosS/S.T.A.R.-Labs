import { createServerFn } from "@tanstack/react-start";
import { getSql } from "@/lib/db";

export const listPosts = createServerFn({ method: "GET" }).handler(async () => {
  const sql = await getSql();
  // Type the row shape — a server fn's return must be provably serializable.
  return sql<{ id: number; title: string }>`select id, title from posts order by id desc`;
  // or: return sql.query<{ id: number; title: string }>("select id, title from posts where id = $1", [id]);
});
