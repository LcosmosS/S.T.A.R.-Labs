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


                return False, None, None, None, None, None, None





    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)


    if success:


        try: