        entropy_results = {}
        for dim in [0, 1, 2, 3, 4]:
            # Get birth-death pairs for this dimension
            pairs = simplex_tree.persistence_intervals_in_dimension(dim)
            if len(pairs) > 0:
                # Remove infinite bars for entropy calculation
                finite_pairs = pairs[np.isfinite(pairs[:, 1])]
                if len(finite_pairs) > 0:
                    lifetimes = finite_pairs[:, 1] - finite_pairs[:, 0]
                    l_sum = np.sum(lifetimes)
                    p_i = lifetimes / l_sum
                    # Shannon entropy of the lifetimes
                    entropy = -np.sum(p_i * np.log(p_i + 1e-12))
                    entropy_results[f'H{dim}_entropy'] = entropy
                else:
                    entropy_results[f'H{dim}_entropy'] = 0
            else:
                entropy_results[f'H{dim}_entropy'] = 0
        return entropy_results


    def find_topological_anchor(self, simplex_tree):
        """
        Identifies if the Rank 4 point is indeed the 'Great Attractor'.
