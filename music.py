import librosa
import torch
import numpy as np
from panns_inference import AudioTagging
import json
def extract_features(audio_path):
    checkpoint_path = r"Cnn14_DecisionLevelMax_mAP=0.385.pth"
    # Load audio
    # PANNs expects 32kHz mono
    
    audio, sr = librosa.load(audio_path, sr=32000, mono=True)
    audio_tensor = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)  # batch dim

    # Load pretrained model
    # Patch labels so CSV is not required
    model = AudioTagging(checkpoint_path=checkpoint_path, device="gpu")

    # Run inference
    clipwise_output, embeddings = model.inference(audio_tensor)
    clipwise_output = clipwise_output[0]  # remove batch dim

    # Extract top 10 tags + weights
    top_indices = np.argsort(clipwise_output)[::-1][:10]
    tags_with_weights = [
        {"tag": model.labels[i], "weight": float(clipwise_output[i])} 
        for i in top_indices
    ]

    print("Top 10 tags + weights:")
    l={}
    for item in tags_with_weights:
        l[item['tag']]=float(item['weight'])*100
    print(l)

    # Convert to list of dicts
    converted = [{"tag": key, "weight": value} for key, value in l.items()]

    # Output as JSON string (pretty-printed)
    json_output = json.dumps(converted, indent=2)
    return json_output
    
# audio_path = r"Linkin.mp3"
# print(extract_features(audio_path))
