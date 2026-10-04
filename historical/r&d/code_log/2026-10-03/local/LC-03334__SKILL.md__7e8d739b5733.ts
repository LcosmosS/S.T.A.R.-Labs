// POST https://api.x.ai/v1/images/generations — same auth header as chat
body: JSON.stringify({
  model: "grok-imagine-image-quality", // or "grok-imagine-image" (cheaper)
  prompt: data.prompt,
  // n (≤10), resolution ("1k"|"2k"), response_format ("url"|"b64_json")
})
// → body.data[0].url
