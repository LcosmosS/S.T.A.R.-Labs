npm run preview:restart   # built output on 127.0.0.1:8081 — QA only, never the live preview
node scripts/browser-smoke.mjs http://127.0.0.1:8081/ /workspace/screenshots/app-builder-built.png --baseline /workspace/screenshots/app-builder-preview.json
npm run preview:stop      # frees :8081 when the built-output QA is done
