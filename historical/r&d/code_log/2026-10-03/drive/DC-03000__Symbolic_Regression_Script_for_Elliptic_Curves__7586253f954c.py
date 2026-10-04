                   rank = descent_rank 
                   rank_success = True 
          except: 
              print("Two-descent failed, attempting point search") 
              try: 
                  points = E.points(bound=100) 
                  non_torsion = [p for p in points if p.order() == 0] 
                  if non_torsion: 
                      print(f"Found non-torsion points: {non_torsion}") 
                  rank = max(1, rank)  
                  else: 
                      print("No non-torsion points found, rank likely 0 if Selmer agrees") 
                  rank = 0 if selmer_rank == two_torsion_rank else rank 
                  rank_success = True   
               except: 
                   print("Point search failed") 
             print(f"Algebraic rank: {rank} (independent nodes in cosmic web)") 
             print(f"2-Selmer rank: {selmer_rank}") 
             try: 
                 S3 = E.selmer_group(3, []) 
                 selmer3_rank = len(S3) - 1 
                 print(f"3-Selmer rank: {selmer3_rank}") 
                 selmer3_success = True 
             except: 
                 print("Failed to compute 3-Selmer rank") 
             break 
         except: 
             print(f"Rank computation failed on attempt {attempt + 1}") 
         if attempt == max_attempts - 1: 
            print("Max attempts reached, skipping curve") 
            return False, None


if rank_success and selmer2_success and selmer3_success: 
      try: 
          L = E.lseries() 
          dok = L.dokchitser(prec=100) 
          L1 = dok(1) 
          if abs(L1) < 1e-10: 
              try: 
                  L1_deriv = dok.derivative(1, 1) 
                  if abs(L1_deriv) < 1e-10: 
                     L1_deriv2 = dok.derivative(1, 2) 
                     if abs(L1_deriv2) < 1e-10 
