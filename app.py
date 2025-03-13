import os
from anonymization import FacerAnonymizer, LLMHandler


def chat(text):
    try:
        anonymizer = FacerAnonymizer(is_log_anonymizer=True)
        anonymized_text  = anonymizer.anonymize(text)
        llm_handler = LLMHandler(provider="mistral", api_key=os.environ["API_KEY_MISTRAL"])
        response_llm = llm_handler.send_to_llm(anonymized_text )
        response = anonymizer.desanonymize(response_llm)
        return response
    
    except Exception as e:
        return f"Erreur lors de la communication avec le modèle : {e}"

def main():
    print("Bienvenue ! Tapez 'exit' pour quitter.")
    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Au revoir !")
            break
        
        response = chat(user_input)
        print(f"IA : {response}")

if __name__ == '__main__':
    main()