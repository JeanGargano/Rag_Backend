import logging
import openai
from app.configurations import Configs
from app.core import ports
import asyncio
from concurrent.futures import ThreadPoolExecutor

class OpenAIAdapter(ports.LlmPort):
    def __init__(self, config: Configs):
        # Usamos el cliente sincrónico de OpenAI
        self.api_key = config.openai_api_key
        self._model = config.model
        self._max_tokens = config.max_tokens
        self._temperature = config.temperature

    async def generate_embeddings_parallel(self, chunks):
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(executor, self.create_embedding, chunk) for chunk in chunks]
            return await asyncio.gather(*tasks)

    def create_embedding(self, text: str):
        try:
            openai.api_key = self.api_key
            # Llamar a los embeddings
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logging.error(f"Error al crear el embedding: {e}")
            return None

    async def generate_text(self, prompt: str, retrieval_context: str) -> str:
        try:
            combined_prompt = f"{retrieval_context}\n\n{prompt}"
            response = openai.ChatCompletion.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Use the following context to answer the user's query."},
                    {"role": "user", "content": combined_prompt},
                ],
                max_tokens=self._max_tokens,
                temperature=self._temperature,
            )
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Error durante la llamada a la API de OpenAI: {e}")
            return "Error generating text."
