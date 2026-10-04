agent-browser batch --bail <<'JSON'
[["open","http://127.0.0.1:8080/"],
 ["find","text","Add note","click"],
 ["fill","#title","Grocery list"],
 ["press","Enter"],
 ["wait","300"],
 ["eval","if (![...document.querySelectorAll('li')].some(n => n.textContent.includes('Grocery list'))) throw Error('note did not appear in the list')"],
 ["screenshot","/workspace/screenshots/note-added.png"]]
JSON
