import openai
from app.core import ports
from app.configurations import Configs

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

            response = openai.ChatCompletion.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": f"The context is: {retrieval_context}, please respond to the following question: "
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self._max_tokens,
                temperature=self._temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return "Error generating text."

    def create_embedding(self, text: str):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding'] if response['data'] else []
