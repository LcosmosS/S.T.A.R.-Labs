        except Exception as exc:
            print()
            print(
                "ERROR during Ollama enrichment:"
            )
            print(exc)
            return 1


        print()
        print(
            "Ollama enrichment complete."
        )
        print()
        print(
            f"Output:"
        )
        print(
            f"  {enriched_path}"
        )
        print()


        return 0


    # --------------------------------------------------------
    # Synthesis mode
    # --------------------------------------------------------


    if args.synthesize_only:


        if not args.model:
            print()
            print(
                "ERROR: --model is required "
                "for synthesis."
