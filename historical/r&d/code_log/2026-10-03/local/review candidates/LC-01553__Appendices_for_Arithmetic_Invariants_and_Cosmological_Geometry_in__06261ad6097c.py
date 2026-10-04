        if rank_evidence and min(rank_evidence) == max(rank_evidence):
            convergent_rank = rank_evidence[0]
            # This is our key inference.
            estimated_3_selmer_bound = convergent_rank
            results['evidence']['estimated_3_selmer_bound'] = estimated_3_selmer_bound
            print(f"  > All rank indicators converge to {convergent_rank}.")
            print(f"  > This provides strong evidence for a 3-Selmer Rank >=
