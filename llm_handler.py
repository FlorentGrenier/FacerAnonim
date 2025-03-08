from mistralai import Mistral

class LLMHandler:
    def __init__(self, provider="mistral", api_key=None, model=None):
        """
        Constructeur pour l'initialisation du handler LLM.
        :param model: Nom du modèle à utiliser. Par défaut, "mistral".
        :param api_key: Clé API pour OpenAI (si utilisé).
        :param endpoint: URL de l'API si un modèle distant est utilisé.
        """
        self.provider = provider
        self.api_key = api_key
        self.model = model
        
        if provider == "mistral":
            self.client = Mistral(api_key=self.api_key)
        else:
            raise ValueError(f"Prodvider {provider} is not supported yet.")

    def send_to_llm(self, text):
        """
        Envoie le texte au modèle LLM spécifié.
        :param text: Le texte à envoyer au LLM.
        :return: La réponse du modèle.
        """
        if self.provider == "mistral":
            return self._send_to_mistral(text)
        else:
            raise ValueError(f"Provider {self.provider} is not supported yet.")

    def _send_to_mistral(self, text):
        """
        Envoi du texte à Mistral via une API (exemple fictif).
        :param text: Le texte à envoyer.
        :return: La réponse de Mistral.
        """
        response = self.client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "user",
                    "content": text,
                },
            ]
        )
        return response.choices[0].message.content
