from sageall import CremonaDatabase

def main():
    db = CremonaDatabase()
    labels = []

    for N in range(1, 5000):
        curves = db.curves(N)
        for L in curves:
            labels.append(L)
            if len(labels) >= 1000:
                break
        if len(labels) >= 1000:
            break

    for L in labels[:1000]:
        print(L)

if __name__ == "__main__":
    main()
