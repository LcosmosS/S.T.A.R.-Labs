const apiKey = process.env.XAI_API_KEY;
if (!apiKey) throw new Error("AI is not available in this environment");
