import torch
from transformers import AutoModel, AutoTokenizer


def get_embedding(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_im = "jhgan/ko-sroberta-multitask"
    tokenizer = AutoTokenizer.from_pretrained(model_im)
    embedding_model = AutoModel.from_pretrained(model_im).to(device)
    inputs = tokenizer(text, return_tensors="pt").to(
        "cpu"
    )  # GPU 사용 시 "cpu" 대신 "cuda"로 변경
    outputs = embedding_model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding
