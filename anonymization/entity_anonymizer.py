import re, json, logging, os, datetime
from transformers import pipeline

class EntityAnonymizer:
    def __init__(self, is_log_anonymizer=False, log_filename="log_anonymizer.json"):
        """
        Constructeur pour initialiser la classe EntityAnonymizer.
        :param log_to_json: Booléen pour décider si on doit loguer dans un fichier JSON.
        :param log_filename: Nom du fichier JSON pour enregistrer les entités et leurs identifiants.
        """
        self.log_anonymizer = is_log_anonymizer
        self.log_filename = log_filename

    def anonymizer(self, text):
        """
        Anonymise le texte en remplaçant les entités par des identifiants uniques.
        :param text: Le texte à anonymiser
        :return: Le texte anonymisé
        """
                
        ner_extract = self._extract_ner(text)
        clean_text, entity_ids = self._replace_words_with_entity_groups_consistent_ids(text, ner_extract)
        self.entity_ids = entity_ids

        if self.log_anonymizer:
            self._log_anonymization_to_file(clean_text, entity_ids)
      
        return clean_text, entity_ids

    def deanonymizer(self, text):
        """
        Restaure le texte original en remplaçant les identifiants par les entités.
        :param text: Le texte anonymisé avec des identifiants
        :return: Le texte restauré
        """

        deanonymizer_text = self._replace_entity_ids_with_text_from_tuple_dict(text, self.entity_ids)
        return deanonymizer_text

    def _replace_words_with_entity_groups_consistent_ids(self, text, entities):
        entities = sorted(entities, key=lambda x: x['start'])

        entity_ids = {}
        id_counters = {}

        modified_text = ""
        current_position = 0

        for entity in entities:
            start, end, entity_group, word = entity['start'], entity['end'], entity['entity_group'], entity['word']

            key = (entity_group, word)

            if key not in entity_ids:
                if entity_group not in id_counters:
                    id_counters[entity_group] = 1
                else:
                    id_counters[entity_group] += 1
                entity_ids[key] = f"{entity_group}{id_counters[entity_group]}"


            modified_text += text[current_position:start]
            modified_text += f" [{entity_ids[key]}]"
            current_position = end

        modified_text += text[current_position:]

        return modified_text, entity_ids

    def _replace_entity_ids_with_text_from_tuple_dict(self, modified_text, entity_ids):

        reversed_entity_ids = {v: k[1] for k, v in entity_ids.items()}

        entity_id_pattern = re.compile(r'\[([A-Z]+[0-9]+)\]')

        def replace_match(match):
            entity_id = match.group(1)
            return reversed_entity_ids.get(entity_id, match.group(0))

        return entity_id_pattern.sub(replace_match, modified_text)

    def _extract_ner(self, text):
        ner = pipeline(
            task='ner',
            model="cmarkea/distilcamembert-base-ner",
            tokenizer="cmarkea/distilcamembert-base-ner",
            aggregation_strategy="simple"
        )

        return ner(text)
    
    def _log_anonymization_to_file(self, clean_text, entity_ids):

        if not os.path.exists(self.log_filename):
            with open(self.log_filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        with open(self.log_filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "modified_text": clean_text,
            "entity_ids": entity_ids
        }

        data.append(log_entry)

        with open(self.log_filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)