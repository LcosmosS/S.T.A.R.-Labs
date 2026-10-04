                        f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            except Exception as e:
                print(f"Failed to estimate 3-Selmer rank: {e}")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                print("Max attempts reached, skipping curve")
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False
