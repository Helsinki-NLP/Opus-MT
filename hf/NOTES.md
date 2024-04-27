

# Issue with broken models after conversion

The script I use to fix the issue is below. Before you start, git clone the checkpoint you want to fix, then:

```
from transformers import MarianMTModel
import torch

checkpoint = "opus-mt-tc-big-fi-en"

model = MarianMTModel.from_pretrained(checkpoint)
state_dict = torch.load(checkpoint + "/pytorch_model.bin")

with torch.no_grad():
    model.model.shared.weight[:] = state_dict['model.shared.weight']

model.save_pretrained(checkpoint, safe_serialization=False)  # Overwrites the old checkpoint
model.save_pretrained(checkpoint, safe_serialization=True)  # Add safetensors while we're here
```

After that, both the models you linked give good results again:

```
>>> pipe("Hei! Hyvää iltaa!")
[{'translation_text': 'Hey, good evening!'}]
```