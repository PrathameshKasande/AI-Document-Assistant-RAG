from huggingface_hub import InferenceClient

from src.config import (
    HUGGINGFACE_API_KEY,
    HUGGINGFACE_MODEL,
    HUGGINGFACE_PROVIDER,
    LLM_MODEL,
    LLM_PROVIDER,
    OLLAMA_HOST,
    MAX_NEW_TOKENS,
    TEMPERATURE,
)

from src.logger import get_logger


logger = get_logger(__name__)


# ============================================
# HUGGING FACE CLIENT
# ============================================

def get_huggingface_client():

    if not HUGGINGFACE_API_KEY:

        raise ValueError(
            "HUGGINGFACE_API_KEY is missing. "
            "Please add it to your .env file."
        )


    return InferenceClient(

        api_key=HUGGINGFACE_API_KEY,

        provider=HUGGINGFACE_PROVIDER

    )


# ============================================
# GENERATE USING HUGGING FACE
# ============================================

def generate_with_huggingface(prompt):

    try:

        client = get_huggingface_client()


        logger.info(
            "Using Hugging Face"
        )


        logger.info(
            "Hugging Face Model: %s",
            HUGGINGFACE_MODEL
        )


        logger.info(
            "Hugging Face Provider: %s",
            HUGGINGFACE_PROVIDER
        )


        response = client.chat.completions.create(

            model=HUGGINGFACE_MODEL,

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are a document question-answering "
                        "assistant. Answer only using the provided "
                        "document context. Do not invent information "
                        "or use outside knowledge."
                    ),

                },

                {

                    "role": "user",

                    "content": prompt,

                },

            ],

            max_tokens=MAX_NEW_TOKENS,

            temperature=TEMPERATURE,

        )


        if not response.choices:

            raise ValueError(
                "The Hugging Face LLM returned "
                "an empty response."
            )


        answer = (
            response.choices[0]
            .message.content
        )


        if not answer:

            raise ValueError(
                "The Hugging Face LLM returned "
                "empty answer content."
            )


        return answer.strip()


    except Exception as error:

        logger.error(
            "Hugging Face generation failed: %s",
            error
        )


        raise RuntimeError(

            f"Hugging Face generation failed: {error}"

        ) from error


# ============================================
# GENERATE USING OLLAMA
# ============================================

def generate_with_ollama(prompt):

    try:

        from ollama import Client


        logger.info(
            "Using Ollama"
        )


        logger.info(
            "Ollama Model: %s",
            LLM_MODEL
        )


        client = Client(

            host=OLLAMA_HOST

        )


        response = client.chat(

            model=LLM_MODEL,

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are a document question-answering "
                        "assistant. Answer only using the provided "
                        "document context. Do not invent information "
                        "or use outside knowledge."
                    ),

                },

                {

                    "role": "user",

                    "content": prompt,

                },

            ],

            options={

                "temperature": TEMPERATURE,

                "num_predict": MAX_NEW_TOKENS,

            }

        )


        answer = response.message.content


        if not answer:

            raise ValueError(
                "The Ollama LLM returned "
                "empty answer content."
            )


        return answer.strip()


    except Exception as error:

        logger.error(
            "Ollama generation failed: %s",
            error
        )


        raise RuntimeError(

            f"Ollama generation failed: {error}"

        ) from error


# ============================================
# MAIN LLM GENERATION
# ============================================

def generate_answer(prompt):

    logger.info(
        "Active LLM Provider: %s",
        LLM_PROVIDER
    )


    logger.info(
        "Active LLM Model: %s",
        LLM_MODEL
    )


    # ========================================
    # OLLAMA
    # ========================================

    if LLM_PROVIDER == "ollama":

        return generate_with_ollama(
            prompt
        )


    # ========================================
    # HUGGING FACE
    # ========================================

    elif LLM_PROVIDER == "huggingface":

        return generate_with_huggingface(
            prompt
        )


    # ========================================
    # INVALID PROVIDER
    # ========================================

    else:

        raise ValueError(

            "Unsupported LLM_PROVIDER: "
            f"{LLM_PROVIDER}. "
            "Supported providers are: "
            "ollama, huggingface."

        )