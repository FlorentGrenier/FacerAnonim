# Projet d'Anonymisation de texte avec envoie à un LLM

## Description
Ce projet permet d'anonymiser des entités nommées (personnes, organisations, lieux, etc.) dans un texte en remplaçant les mots identifiés par des identifiants uniques et cohérents. Il est utile pour masquer des informations sensibles tout en conservant la structure et la lisibilité du texte.

## Fonctionnalités
- Extraction et anonymisation des entités nommées
- Remplacement des entités par des identifiants uniques et cohérents
- Génération d'un dictionnaire des correspondances entre entités et identifiants

## Installation
### Prérequis
- Python 3.x
- Bibliothèques requises :

```python 
pip install -r requirements.txt
```

## Utilisation
### Exemple de code
```python 
text = "Le Crédit Mutuel Arkéa est basé en Bretagne. Louis Lichou était le président."
entities = [
    {"start": 3, "end": 18, "entity_group": "ORG", "word": "Crédit Mutuel"},
    {"start": 19, "end": 24, "entity_group": "ORG", "word": "Arkéa"},
    {"start": 54, "end": 65, "entity_group": "PER", "word": "Louis Lichou"}
]

modified_text, entity_ids = replace_words_with_entity_groups_consistent_ids(text, entities)

print(modified_text)
# "Le [ORG1] [ORG2] est basé en Bretagne. [PER1] était le président."
print(entity_ids)
# {('ORG', 'Crédit Mutuel'): 'ORG1', ('ORG', 'Arkéa'): 'ORG2', ('PER', 'Louis Lichou'): 'PER1'}
```

### Prise en charge des modèles LLM

Ce projet prend actuellement en charge les modèles suivants :

- **Mistral** (via l'API Mistral)

Vous pouvez configurer le modèle souhaité lors de l'initialisation du handler LLM. Exemple :

```python
llm_handler = LLMHandler(provider="mistral", api_key=os.environ["API_KEY_MISTRAL"])
```

## Tests
Les tests unitaires sont disponibles dans test.py. Pour les exécuter :
```python 
python -m unittest test.py
```
