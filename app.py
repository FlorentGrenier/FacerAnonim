import re, os, argparse, json
from transformers import pipeline
from mistralai import Mistral

def replace_words_with_entity_groups_consistent_ids(text, entities):
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
        modified_text += f"[{entity_ids[key]}]"
        current_position = end

    modified_text += text[current_position:]

    return modified_text, entity_ids

def replace_entity_ids_with_text_from_tuple_dict(modified_text, entity_ids):

    reversed_entity_ids = {v: k[1] for k, v in entity_ids.items()}

    entity_id_pattern = re.compile(r'\[([A-Z]+[0-9]+)\]')

    def replace_match(match):
        entity_id = match.group(1)
        return reversed_entity_ids.get(entity_id, match.group(0))

    return entity_id_pattern.sub(replace_match, modified_text)

def extract_ner(text):
 

    ner = pipeline(
        task='ner',
        model="cmarkea/distilcamembert-base-ner",
        tokenizer="cmarkea/distilcamembert-base-ner",
        aggregation_strategy="simple"
    )

    return ner(text)

def chat(client, prompt, model="mistral-large-latest"):
    try:
        result = extract_ner(prompt)
        modified_text, entity_ids = replace_words_with_entity_groups_consistent_ids(result, result)
        
        # Sauvegarder modified_text et entity_ids
        with open("modified_text_and_entities.json", "w", encoding="utf-8") as file:
            json.dump({"modified_text": modified_text, "entity_ids": entity_ids}, file, ensure_ascii=False, indent=4)
        
        chat_response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content": modified_text,
                },
            ]
        )

        generated_text = replace_entity_ids_with_text_from_tuple_dict(chat_response.choices[0].message.content, entity_ids)
        
        # Sauvegarder le texte généré
        with open("generated_text.txt", "w", encoding="utf-8") as file:
            file.write(generated_text)

        return generated_text
    
    except Exception as e:
        return f"Erreur lors de la communication avec le modèle : {e}"

def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="Le nom du modèle à utliser.")
    args = parser.parse_args()

    print("Bienvenue ! Tapez 'exit' pour quitter.")
    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Au revoir !")
            break
        
        response = chat(client, user_input, model=args.model)
        print(f"IA : {response}")

if __name__ == '__main__':
    main()