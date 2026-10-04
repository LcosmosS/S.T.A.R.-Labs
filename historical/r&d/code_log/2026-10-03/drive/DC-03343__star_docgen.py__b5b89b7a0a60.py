            print()
            print(
                "Example:"
            )
            print(
                "  --model llama3"
            )
            print()


            return 2


        if not check_model(args.model):
            return 2


        evidence_path = (
            args.output /
            "page_evidence.jsonl"
