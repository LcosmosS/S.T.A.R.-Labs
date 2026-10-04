def ollama_available() -> bool:
    """Return True if the Ollama API is reachable."""


    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=10,
        )
        response.raise_for_status()
        return True


    except requests.RequestException:
        return False




def ollama_models():
    """Return installed Ollama model names."""


    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=10,
        )
        response.raise_for_status()


        data = response.json()


        return [
            model.get("name")
            for model in data.get("models", [])
            if model.get("name")
