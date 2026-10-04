                        f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            except Exception as e:
                print(f"Failed to estimate 3-Selmer rank: {e}")
            break
