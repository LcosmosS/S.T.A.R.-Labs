agent-browser open http://127.0.0.1:8080/
agent-browser snapshot -i                        # a11y tree with @e1 refs
agent-browser click @e1                          # or: find text "Start" click
agent-browser fill "#email" you@example.com      # type <text> for keystrokes
agent-browser press Enter                        # a tap; holding: see "Keys"
agent-browser wait --fn "window.__ready === true"   # or: wait 500 (ms)
agent-browser eval "document.querySelectorAll('.card').length"
agent-browser console                            # or: errors (page errors)
agent-browser screenshot /workspace/screenshots/step.png
agent-browser close
