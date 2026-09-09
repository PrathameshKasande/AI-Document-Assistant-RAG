import os

from dotenv import load_dotenv


load_dotenv()


# ============================================
# BASE DIRECTORY
# ============================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================
# DATA DIRECTORIES
# ============================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


UPLOAD_DIR = os.path.join(
    DATA_DIR,
    "uploaded_documents"
)


VECTOR_STORE_DIR = os.path.join(
    DATA_DIR,
    "vector_store"
)


LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)


# ============================================
# LLM PROVIDER
# ============================================

# Supported values:
#
# ollama
# huggingface

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
).lower()


# ============================================
# HUGGING FACE SETTINGS
# ============================================

HUGGINGFACE_API_KEY = os.getenv(
    "HUGGINGFACE_API_KEY"
)


HUGGINGFACE_MODEL = os.getenv(
    "HUGGINGFACE_MODEL",
    "Qwen/Qwen3-8B"
)


# Optional Hugging Face provider
#
# Examples:
# auto
# hf-inference
# together

HUGGINGFACE_PROVIDER = os.getenv(
    "HUGGINGFACE_PROVIDER",
    "auto"
)


# ============================================
# OLLAMA SETTINGS
# ============================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)


# ============================================
# ACTIVE LLM MODEL
# ============================================

if LLM_PROVIDER == "ollama":

    LLM_MODEL = OLLAMA_MODEL


elif LLM_PROVIDER == "huggingface":

    LLM_MODEL = HUGGINGFACE_MODEL


else:

    raise ValueError(
        "Invalid LLM_PROVIDER. "
        "Use 'ollama' or 'huggingface'."
    )


# ============================================
# EMBEDDING MODEL
# ============================================

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================
# CHUNK SETTINGS
# ============================================

CHUNK_SIZE = 1000


CHUNK_OVERLAP = 100


# ============================================
# RETRIEVAL SETTINGS
# ============================================

TOP_K = 5


NEIGHBOR_WINDOW = 1


# ============================================
# LLM SETTINGS
# ============================================

MAX_NEW_TOKENS = 1000


TEMPERATURE = 0.2


# ============================================
# CREATE DIRECTORIES
# ============================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


os.makedirs(
    VECTOR_STORE_DIR,
    exist_ok=True
)


os.makedirs(
    LOG_DIR,
    exist_ok=True
)