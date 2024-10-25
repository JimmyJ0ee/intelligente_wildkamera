"""SSL-Error"""

from datasets import load_dataset
from huggingface_hub import login

login("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")

ds = load_dataset("imagenet-1k", trust_remote_code=True)
train_ds = ds["train"]
train_ds[0]["image"]  # a PIL Image
