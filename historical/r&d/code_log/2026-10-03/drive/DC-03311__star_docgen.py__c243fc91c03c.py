def check_model(model: str):
    """Verify that the requested Ollama model is installed."""


    installed = ollama_models()


    if model not in installed:
        print()
        print("ERROR: Requested Ollama model is not installed.")
        print()
        print(f"Requested model: {model}")
        print()


        if installed:
            print("Installed models:")
            for name in installed:
                print(f"  {name}")
        else:
            print("No Ollama models are currently installed.")


        print()
        print(f"Install the model with:")
        print(f"  ollama pull {model}")
        print()


        return False


    return True




def ollama(model: str, prompt: str, temperature: float = 0.1) -> str:
    """
    Send a prompt to Ollama and return its generated response.
