import json
import os

def create_assistant(client):
    assistant_file_path = 'assistant.json'

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # List of filenames for PDFs
        pdf_files = [
            "Sample-1.pdf",
            "Sample-2.pdf",
            "Sample-3.pdf",
            "Sample-4.pdf",
            "Sample-5.pdf",
            "Sample-6.pdf",
            "Sample-7.pdf",
            "Sample-8.pdf",
            "Sample-9.pdf",
            "Sample-10.pdf",
            "Sample-11.pdf",
        ]

        file_ids = []
        for filename in pdf_files:
            with open(filename, 'rb') as pdf_file:
                file = client.files.create(file=pdf_file, purpose='assistants')
                file_ids.append(file.id)

        assistant = client.beta.assistants.create(
            instructions=""""
            The MedChatAssistant is meticulously designed to address queries solely within the domain of lung cancer-related topics based on the available documents. It draws insights from an extensive repository curated specifically for lung cancer, encompassing the latest advancements, research findings, and statistical data pertinent to this field.
            Endowed with a comprehensive understanding of the provided documents, the assistant rigorously evaluates each file before responding to inquiries. Patients can explore a wide spectrum of lung cancer-related topics, including treatment methodologies, side effects, clinical trials, and lifestyle recommendations.
            Maintaining confidentiality and impartiality, the assistant refrains from referencing specific documents or revealing their origins. Instead, it synthesizes information from its repository through detailed analysis, ensuring a nuanced understanding of the patient's query.
            Utilizing cutting-edge AI technology, the assistant retrieves accurate information without explicitly citing the source documents. Responses are formulated based on a collective knowledge base distilled from its repository, bypassing direct reliance on individual sources.
            The MedChatAssistant operates within strict boundaries, exclusively addressing lung cancer-related queries aligned with its available documents. If faced with inquiries outside this scope, it responds with a predefined message: "I am sorry, I am programmed to provide information solely related to lung cancer within the scope of available documents."
            Ultimately, the MedChatAssistant aims to empower patients with credible information, aiding informed decision-making and fostering better comprehension of their condition. It strives to facilitate meaningful discussions with healthcare providers specifically within the sphere of lung cancer expertise.
            """,
            model="gpt-3.5-turbo-1106",
            tools=[{"type": "retrieval"}],
            file_ids=file_ids)

        client.fine_tuning.jobs.create(
        training_file="Sample-6.pdf",
        model="gpt-3.5-turbo-1106")

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
