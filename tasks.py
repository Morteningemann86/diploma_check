from openai import OpenAI
import base64
import requests
import json
import os
from pathlib import Path
from resources.key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_openai_response(base64_image):
    prompt = '''
                Based on the image input, provide me with the following information: Is the image a picture of a university diploma? What is the name of the university?
                Your response should be in JSON format like this, depending on the image content.

                    {
                      "type_of_document": "Diploma",
                      "name_university": "University of Copenhagen"
                    }

                    or this:

                    {
                      "type_of_document": "Transcript",
                      "name_university": "University of Copenhagen"
                    }

                    If the image is neither a diploma nor transcript, return:

                    {
                      "type_of_document": "Unknown",
                      "name_university": "Unknown"
                    }
                '''

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ],
            }
        ],
        max_tokens=300
    )

    result = response.json()
    data = json.loads(result)
    content = data['choices'][0]['message']['content']
    content = content.replace('```json\n', '').replace('\n```', '')
    return json.loads(content)

def process_image(filename):
    base64_image = encode_image(os.path.join('input', filename))
    content = get_openai_response(base64_image)
    print(content['type_of_document'], content['name_university'])

    if content['type_of_document'].lower() == "unknown" or content['name_university'].lower() == "unknown":
        return

    move_file(filename, content['type_of_document'], content['name_university'])

def move_file(filename, type_of_document, name_university):
    original_file_path = os.path.join('input', filename)
    new_file_name = f'{type_of_document} - {name_university}'
    output_folder = 'output'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    new_file_path = Path(output_folder) / Path(new_file_name).with_suffix('.jpg')
    Path(original_file_path).rename(new_file_path)
    print(f"Moved file from {original_file_path} to {new_file_path}")

def admission_documents_organizer():
    for filename in os.listdir('input'):
        if filename.endswith('.jpg'):
            process_image(filename)

admission_documents_organizer()