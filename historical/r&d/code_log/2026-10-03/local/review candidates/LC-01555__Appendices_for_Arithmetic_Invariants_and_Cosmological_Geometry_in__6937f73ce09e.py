    except Exception as e:
        print(f"[Step 5] 3-Selmer proxy analysis failed: {e}")
        results['evidence']['estimated_3_selmer_bound'] = 'Error'

    # --- Final Conclusion ---
    final_estimate = results['evidence'].get('estimated_3_selmer_bound')
    results['final_conclusion'] = final_estimate
    print("\n--- Conclusion ---")
    if isinstance(final_estimate, int):
        print(f"\033[92mThe convergent evidence strongly suggests a 3-Selmer Rank of
