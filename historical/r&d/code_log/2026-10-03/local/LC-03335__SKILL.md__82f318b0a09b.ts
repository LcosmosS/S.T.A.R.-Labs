// Same Authorization header; returns audio bytes (e.g. MP3)
body: JSON.stringify({ text: data.text, voice_id: "eve" }) // eve = default voice
