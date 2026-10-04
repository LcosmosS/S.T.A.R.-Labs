   if rank == 0:
       return 0
   # The raw arithmetic state of the system
   arithmetic_state = RR(regulator / rank)
   # The physical energy equivalent of that state
   return upsilon * arithmetic_state

# ==============================================================================
# SECTION 3: MAIN PIPELINE EXECUTION
# ==============================================================================

if __name__ == "__main__":
   print("="*80)
   print(" UCF Definitive Test: The Informational Potential Hypothesis")
   print("="*80)
   
   galaxy_data = get_galaxy_virial_data()
