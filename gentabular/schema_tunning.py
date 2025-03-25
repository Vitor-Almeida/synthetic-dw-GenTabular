import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(".env.local")
client = OpenAI(api_key=os.getenv("API_KEY"))

def generate_examples_openai(fields, n_examples=5):
    """
    Generates examples for a set of fields using OpenAI ChatCompletion.
    
    fields: a list of dictionaries, each describing a field.
    n_examples: how many examples to generate per field.
    
    Returns a dict like:
        {
          field_name_1: ["Example1", "Example2", ...],
          field_name_2: ["Example1", "Example2", ...],
          ...
        }
    """

    # Build a prompt (or system/user messages) describing what you want. 
    # This example tries to generate a few short examples per field:
    field_descriptions = []
    for f in fields:
        desc = (
            f"Field name: {f['name']}\n"
            f"Type: {f['details'].get('Tipo')}\n"
            f"Description: {f['details'].get('Descrição')}\n"
        )
        field_descriptions.append(desc)
    
    prompt_text = (
        "You are a data generation assistant. "
        "Generate multiple short example values for each field specified below. "
        "Ensure any fields that depend on each other remain logically consistent. "
        "For example, if one field is 'Category' denoting a type of drink, the 'Subcategory' must match that type—"
        "yet feel free to invent unusual or whimsical categories and subcategories. "
        "Your only requirement is to keep related fields aligned with one another. "
        "Finally, return everything in valid JSON format, with each field name as the key and an array "
        f"of {n_examples} example values as the value.\n\n"
        + "\n".join(field_descriptions)
    )

    #arrumar aqui, o system_prompt tem q ter alguma coisa, falar sobre a empresa, e a tarefa em si.

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "" #system_prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text}
                ]
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    # Extract the API's response. Usually it's in response.choices[0].message["content"]
    ai_message = response.choices[0].message.content.strip()

    # In an ideal scenario, we expect valid JSON. 
    # You might want to handle JSON parsing errors, or do sanity checks.
    try:
        results = json.loads(ai_message)
    except json.JSONDecodeError:
        # If the model doesn't return proper JSON, handle that here.
        # For now, just return an empty dict or fallback.
        results = {}

    # We might still need to verify each field got an array of examples.
    # This code assumes the model responded in the correct format.
    return results


def process_schema(schema, n_examples=5):
    """
    Processes the dictionary 'schema' by identifying fields with TipoGen=IA,
    grouping them by GenGrupo, then calling 'generate_examples_openai' for each group
    to populate 'ExemplosCompletos'.
    """
    for table_name, attributes in schema.items():
        # 1. Identify attributes with TipoGen=IA
        ia_attributes = []
        for attr_name, attr_details in attributes.items():
            if attr_details.get("TipoGen") == "IA":
                ia_attributes.append({
                    "name": attr_name,
                    "GenGrupo": attr_details.get("GenGrupo"),
                    "details": attr_details
                })

        # 2. Group attributes by GenGrupo 
        groups = {}
        for attr in ia_attributes:
            group_id = attr["GenGrupo"]
            if group_id is None:
                # Treat as an individual group
                single_group_id = f"__individual_{attr['name']}"
                groups.setdefault(single_group_id, []).append(attr)
            else:
                groups.setdefault(group_id, []).append(attr)

        # 3. For each group, call the function to generate examples
        for group_identifier, group_fields in groups.items():
            # Generate the examples for these fields in one request
            generation_results = generate_examples_openai(group_fields, n_examples=n_examples)

            # 4. Update the original attributes in the schema with the generated examples
            for f in group_fields:
                attr_name = f["name"]
                if attr_name in generation_results:
                    attributes[attr_name]["ExemplosCompletos"] = generation_results[attr_name]
                else:
                    # If the model didn't return results for a given field
                    attributes[attr_name]["ExemplosCompletos"] = []

    return schema


if __name__ == "__main__":
    # Example of reading an input JSON containing your schema
    with open("data/vemma/schema.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 'data' should have something like { "SchemaCompleto": { ... } }
    full_schema = data.get("SchemaCompleto", {})

    # Process the schema to generate examples
    updated_schema = process_schema(full_schema, n_examples=5)

    # Insert the updated schema back into your main dictionary
    data["SchemaCompleto"] = updated_schema

    # Save the JSON with the new field "ExemplosCompletos"
    with open("data/vemma/schema_processado.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
