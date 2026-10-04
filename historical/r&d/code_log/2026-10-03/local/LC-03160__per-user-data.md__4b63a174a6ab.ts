import { createServerFn } from "@tanstack/react-start";
import { getSql } from "@/lib/db";
import { authMiddleware } from "@/lib/auth/middleware";

export const listTodos = createServerFn({ method: "GET" })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    const sql = await getSql();
    // Type the row shape — a server fn's return must be provably serializable.
    return sql<{ id: number; title: string; done: boolean }>`select id, title, done from todos where user_id = ${context.userId} order by id desc`;
  });

// Inputs go through `.validator()` (the current API); the client passes `{ data }`:
export const addTodo = createServerFn({ method: "POST" })
  .validator((title: string) => title.trim())
  .middleware([authMiddleware])
  .handler(async ({ context, data: title }) => {
    if (!title) return;
    const sql = await getSql();
    await sql`insert into todos (user_id, title) values (${context.userId}, ${title})`;
  });
// mutations must scope writes too: `... where id = ${id} and user_id = ${context.userId}`
