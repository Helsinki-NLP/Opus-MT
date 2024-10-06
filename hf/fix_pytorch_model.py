
from transformers import MarianMTModel
import torch
import sys

checkpoint = sys.argv[1]

model = MarianMTModel.from_pretrained(checkpoint)
state_dict = torch.load(checkpoint + "/pytorch_model.bin")

with torch.no_grad():
    model.model.shared.weight[:] = state_dict['model.shared.weight']

model.save_pretrained(checkpoint, safe_serialization=False)  # Overwrites the old checkpoint
model.save_pretrained(checkpoint, safe_serialization=True)  # Add safetensors while we're here
