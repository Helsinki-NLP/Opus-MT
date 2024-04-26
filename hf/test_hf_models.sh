#!/bin/bash
#SBATCH --job-name="test_hf_models_%j"
#SBATCH --account=project_2000661
#SBATCH --output=test_hf_models_%j.out
#SBATCH --error=test_hf_models_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=16G
#SBATCH --partition=small
#SBATCH --mail-type=FAIL,END


# export TRANSFORMERS_CACHE="/scratch/project_2005815/HF-leaderboard/.cache/hugging_face/"
python3 test_hf_models.py
