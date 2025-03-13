import unittest
from anonymization.entity_anonymizer import FacerAnonymizer
from anonymization.handler.llm_handler import LLMHandler
from unittest.mock import MagicMock

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.anonymizer = FacerAnonymizer(log_to_json=False)
        self.llm_handler = MagicMock(spec=LLMHandler)

    def test_full_integration(self):
        text = "Le Crédit Mutuel Arkéa est basé en Bretagne."
        
        # Simuler l'anonymisation
        modified_text = self.anonymizer.anonymizer(text)

        # Simuler la réponse du LLM
        self.llm_handler.send_to_llm.return_value = "Le [ORG1] [ORG2] est en Bretagne."

        # Tester l'intégration
        response = self.llm_handler.send_to_llm(modified_text)
        self.assertEqual(response, "Le [ORG1] [ORG2] est en Bretagne.")

if __name__ == "__main__":
    unittest.main()
