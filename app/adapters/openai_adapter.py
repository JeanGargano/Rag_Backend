import openai
from app.core import ports
from app.configurations import Configs
import logging

class OpenAIAdapter(ports.LlmPort):
    def __init__(self, config: Configs):
        openai.api_key = config.openai_api_key
        self._model = config.model
        self._max_tokens = config.max_tokens
        self._temperature = config.temperature

    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        try:
            print(f"Retrieval Context: {retrieval_context}")
            print(f"Prompt: {prompt}")

            # Combinar el contexto y la consulta
            combined_prompt = f"{retrieval_context}\n\n{prompt}"

            response = openai.ChatCompletion.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Use the following context to answer the user's query."
                    },
                    {"role": "user", "content": combined_prompt},
                ],
                max_tokens=self._max_tokens,
                temperature=self._temperature,
            )
            generated_answer = response['choices'][0]['message']['content']
            print(f"Generated Answer: {generated_answer}")
            return generated_answer
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return "Error generating text."

    def create_embedding(self, text: str):
        try:
            # Generar el embedding
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )

            # Comprobar si hay datos en la respuesta
            if 'data' in response and len(response['data']) > 0:
                embedding = response['data'][0]['embedding']
            else:
                raise ValueError("No se recibieron datos de embedding válidos.")

            # Loggear el embedding generado
            logging.info(f"Embedding generado para el texto: {embedding}")

            # Devolver el embedding
            return embedding

        except Exception as e:
            logging.error(f"Error al crear el embedding: {e}", exc_info=True)
            return None  # O lanza una excepción, según tu preferencia

