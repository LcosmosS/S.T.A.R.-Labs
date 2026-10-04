import { authMiddleware } from "@/lib/auth/middleware";

export const listTodos = createServerFn({ method: "GET" })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    const sql = await getSql();
    return sql<{ id: number; title: string }>`select id, title from todos where user_id = ${context.userId} order by id desc`;
  });
// mutations must scope writes too: `... where id = ${id} and user_id = ${context.userId}`
