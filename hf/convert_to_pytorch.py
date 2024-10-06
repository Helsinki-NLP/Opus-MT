# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from pathlib import Path
from transformers.models.marian.convert_marian_to_pytorch import convert


argparser = argparse.ArgumentParser('Convert Marian NMT models to pyTorch')
argparser.add_argument('--model-path', action="store", required=True)
argparser.add_argument('--dest-path', action="store", required=True)
args = argparser.parse_args()

Path(args.dest_path).mkdir(parents=True, exist_ok=True)
convert(Path(args.model_path), Path(args.dest_path))


# add a fix that does not seem to work with the conversion script

from transformers import MarianMTModel
import torch

checkpoint = args.dest_path
model = MarianMTModel.from_pretrained(checkpoint)
state_dict = torch.load(checkpoint + "/pytorch_model.bin")

with torch.no_grad():
    model.model.shared.weight[:] = state_dict['model.shared.weight']

model.save_pretrained(checkpoint, safe_serialization=False)  # Overwrites the old checkpoint
model.save_pretrained(checkpoint, safe_serialization=True)   # Add safetensors while we're here
