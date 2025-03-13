from mistralai import Mistral
from anonymization import FacerAnonymizer

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
        self.anonymizer = FacerAnonymizer(is_log_anonymizer=True)
        
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
        anonymized_text  = self.anonymizer.anonymize(text)
        
        if self.provider == "mistral":
            response_anonymize = self._send_to_mistral(anonymized_text)
        else:
            raise ValueError(f"Provider {self.provider} is not supported yet.")
        
        response = self.anonymizer.desanonymize(response_anonymize)

        return response
        

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
