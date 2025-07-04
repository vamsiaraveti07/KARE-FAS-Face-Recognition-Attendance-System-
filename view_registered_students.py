import pickle
import os

# Path to the encodings file
encodings_path = "encodings.pkl"

# Check if file exists
if not os.path.exists(encodings_path):
    print("[ERROR] No registered students found. 'encodings.pkl' does not exist.")
    exit()

# Load data
with open(encodings_path, "rb") as f:
    data = pickle.load(f)

# Check if list is empty
if not data["ids"]:
    print("[INFO] No students currently registered.")
else:
    print("\n✅ Registered Students:\n")
    for i in range(len(data["ids"])):
        print(f"{i+1}. ID: {data['ids'][i]}  |  Name: {data['names'][i]}")
