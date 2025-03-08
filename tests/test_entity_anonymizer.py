import unittest, xmlrunner
from anonymization.entity_anonymizer import EntityAnonymizer
from unittest.mock import patch

class TestEntityAnonymizer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.anonymizer = EntityAnonymizer(is_log_anonymizer=False)

        self.user_text = (
            "Le Crédit Mutuel Arkéa est une banque Française, elle comprend le CMB "
            "qui est une banque située en Bretagne et le CMSO qui est une banque "
            "qui se situe principalement en Aquitaine. C'est sous la présidence de "
            "Louis Lichou, dans les années 1980 que différentes filiales sont créées "
            "au sein du CMB et forment les principales filiales du groupe qui "
            "existent encore aujourd'hui (Federal Finance, Suravenir, Financo, etc.)."
        )

        self.entities = [
            {'entity_group': 'ORG', 'score': 0.9974479, 'word': 'Crédit Mutuel Arkéa', 'start': 2, 'end': 22}, 
            {'entity_group': 'LOC', 'score': 0.9000355, 'word': 'Française', 'start': 37, 'end': 47}, 
            {'entity_group': 'ORG', 'score': 0.97887576, 'word': 'CMB', 'start': 65, 'end': 69}, 
            {'entity_group': 'LOC', 'score': 0.99919766, 'word': 'Bretagne', 'start': 98, 'end': 107}, 
            {'entity_group': 'ORG', 'score': 0.9594884, 'word': 'CMSO', 'start': 113, 'end': 118}, 
            {'entity_group': 'LOC', 'score': 0.99935514, 'word': 'Aquitaine', 'start': 168, 'end': 178}, 
            {'entity_group': 'PER', 'score': 0.99911094, 'word': 'Louis Lichou', 'start': 207, 'end': 220}, 
            {'entity_group': 'ORG', 'score': 0.9622638, 'word': 'CMB', 'start': 290, 'end': 294}, 
            {'entity_group': 'ORG', 'score': 0.9983959, 'word': 'Federal Finance', 'start': 374, 'end': 389}, 
            {'entity_group': 'ORG', 'score': 0.9984454, 'word': 'Suravenir', 'start': 390, 'end': 400}, 
            {'entity_group': 'ORG', 'score': 0.9985084, 'word': 'Financo', 'start': 401, 'end': 409}
        ]

    def test_anonymizer(self):
        modified_text, entity_ids = self.anonymizer.anonymizer(self.user_text)
        
        modified_text_expected = (
            "Le [ORG1] est une banque [LOC1], elle comprend le [ORG2] qui est une banque située en [LOC2]"
            " et le [ORG3] qui est une banque qui se situe principalement en [LOC3]. C'est sous la présidence de [PER1], " 
            "dans les années 1980 que différentes filiales sont créées au sein du [ORG2] et forment les principales filiales " 
            "du groupe qui existent encore aujourd'hui ( [ORG4], [ORG5], [ORG6], etc.)."
        )

        entity_ids_expected = {
            ('ORG', 'Crédit Mutuel Arkéa'): 'ORG1', ('LOC', 'Française'): 'LOC1', 
            ('ORG', 'CMB'): 'ORG2', ('LOC', 'Bretagne'): 'LOC2', ('ORG', 'CMSO'): 'ORG3', 
            ('LOC', 'Aquitaine'): 'LOC3', ('PER', 'Louis Lichou'): 'PER1', ('ORG', 'Federal Finance'): 'ORG4', 
            ('ORG', 'Suravenir'): 'ORG5', ('ORG', 'Financo'): 'ORG6'
        }

        self.assertEqual(modified_text, modified_text_expected)
        self.assertEqual(entity_ids, entity_ids_expected)

    def test_deanonymizer(self):
        self.anonymizer.entity_ids = {
            ('ORG', 'Crédit Mutuel Arkéa'): 'ORG1', ('LOC', 'Française'): 'LOC1', 
            ('ORG', 'CMB'): 'ORG2', ('LOC', 'Bretagne'): 'LOC2', ('ORG', 'CMSO'): 'ORG3', 
            ('LOC', 'Aquitaine'): 'LOC3', ('PER', 'Louis Lichou'): 'PER1', ('ORG', 'Federal Finance'): 'ORG4', 
            ('ORG', 'Suravenir'): 'ORG5', ('ORG', 'Financo'): 'ORG6'
        }

        generated_text = (
            "et qui jouent un rôle clé dans le développement et la diversification des activités bancaires du groupe."
            "Ces filiales couvrent des domaines variés tels que la gestion d'actifs, le financement des entreprises,"
            "et les services bancaires internationaux, renforçant ainsi la position du [ORG1] en tant qu'acteur majeur sur la scène financière mondiale."
            "Elles ont également contribué à l'innovation et à l'expansion géographique du groupe, en s'implantant sur de nouveaux marchés et en développant "
            "des solutions adaptées aux besoins spécifiques de leurs clients, qu'il s'agisse de particuliers, de professionnels ou de grandes entreprises."
            "Sous l'impulsion de [PER1], le [ORG1] a su consolider son réseau international tout en maintenant une forte présence locale grâce à ses filiales comme [ORG4], [ORG5] et [ORG6],"
            "qui restent des piliers stratégiques du groupe."
        )

        final_text = self.anonymizer.deanonymizer(generated_text)

        final_text_expected = ("et qui jouent un rôle clé dans le développement et la diversification des activités bancaires du groupe."
                               "Ces filiales couvrent des domaines variés tels que la gestion d'actifs, le financement des entreprises,"
                               "et les services bancaires internationaux, renforçant ainsi la position du Crédit Mutuel Arkéa en tant qu'acteur majeur sur la scène financière mondiale."
                               "Elles ont également contribué à l'innovation et à l'expansion géographique du groupe, en s'implantant sur de nouveaux marchés et en développant "
                               "des solutions adaptées aux besoins spécifiques de leurs clients, qu'il s'agisse de particuliers, de professionnels ou de grandes entreprises."
                               "Sous l'impulsion de Louis Lichou, le Crédit Mutuel Arkéa a su consolider son réseau international tout en maintenant une forte présence locale grâce à ses filiales"
                               " comme Federal Finance, Suravenir et Financo,qui restent des piliers stratégiques du groupe.")

        self.assertEqual(final_text, final_text_expected)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
