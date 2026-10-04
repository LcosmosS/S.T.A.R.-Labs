                    f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")

            break

        except Exception as e:

            print(f"Rank computation failed on attempt {attempt + 1}: {e}")

            if attempt == max_attempts - 1:
