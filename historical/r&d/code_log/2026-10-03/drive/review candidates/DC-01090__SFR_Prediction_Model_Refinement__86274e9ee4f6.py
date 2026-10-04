import pickle


with open("best_gb_model.pkl", "rb") as f:  # note the 'rb' for read-binary
    gb = pickle.load(f)
