"""
このモジュールは、OpenAIのGPT-4を使用して指示を解析し、特定のオブジェクトを特定の方向に配送するための情報を抽出します。
"""
# pylint: disable=import-error
import os
import json
import openai

os.environ['OPENAI_API_KEY'] = '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'

openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_instruction(objects, instruction):
    """
    Analyze the given instruction and extract two pieces of information:
    'target_obj: [object], target_person: [direction]'
    1) The object to be delivered from the list of objects, labeled as 'target_obj'.
    2) The direction of the person (either 'left' or 'right'), labeled as 'target_person'.
    """
    objects_formatted = ', '.join(objects)
    prompt = (
        f"Analyze the given instruction and extract two pieces of information: "
        f"'target_obj: [object], target_person: [direction]' "
        f"1) The object to be delivered from the list of objects"
        f"[{objects_formatted}], labeled as 'target_obj'. "
        f"2) The direction of the person (either 'left' or 'right'), labeled as 'target_person'. "
        f"Instruction: '{instruction}'. Then provide the response in this strict format: "
        f"'target_obj: [object], target_person: [direction]'"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": instruction}
            ]
        )
        extracted_data = response['choices'][0]['message']['content'].strip()
        print(extracted_data)
        # Splitting the response to separate 'target_obj' and 'target_person'
        data_parts = extracted_data.split(',')
        res = {}
        for part in data_parts:
            key_value = part.split(':')
            if len(key_value) == 2:
                res[key_value[0].strip()] = key_value[1].strip()
        return res
    except openai.error.OpenAIError as error:
        print("Error in API request:", error)
        return {}

# # Usage example
# result = askingInstruction("deliver tuna_can to left person")
# print(result)

def is_response_valid(response, valid_keys):
    """
    Check if the response contains the expected keys and valid values.

    Args:
    response (dict): The response to be validated.
    valid_keys (list): List of valid keys for the response.

    Returns:
    bool: True if the response is valid, False otherwise.
    """
    expected_keys = ['Target object', 'Direction of the target person']

    # 期待されるキーがすべてレスポンスに含まれているかチェック
    if not all(key in response for key in expected_keys):
        return False

    # 'target_obj'が有効なキーリストに含まれているかチェック
    if response['Target object'] not in valid_keys:
        return False

    # 'Direction of the target person'が'left'または'right'であるかチェック
    if response['Direction of the target person'] not in ['left', 'right']:
        return False

    return True




def load_keys_from_json(file_path):
    """
    Load keys from a JSON file located at the specified file path.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    list: A list of keys extracted from the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            keys_list_from_json = list(data.keys())
            return keys_list_from_json
    except FileNotFoundError:
        print("JSONファイルが見つかりません。")
    except json.JSONDecodeError:
        print("JSONファイルのフォーマットが正しくありません。")
    return None

def ask_gpt(valid_objects, instruction):
    """
    Attempt to get a valid response by asking GPT-3 for the given instruction.

    Args:
    valid_objects (list): List of valid objects for delivery.
    instruction (str): The delivery instruction.

    Returns:
    dict or None: A valid response containing the target object and direction of the target person,
    or None if no valid response is obtained after several attempts.
    """
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        response = ask_instruction(valid_objects, instruction)
        print(f"Attempt {attempt+1}: Response - {response}")

        if is_response_valid(response, valid_objects):
            return response
        print("Response not in expected format. Retrying...")
        attempt += 1
    print("Failed to get a valid response after several attempts.")
    return None
# 使用例
PATH = '../config/positionLabels.json'
keys_list = load_keys_from_json(PATH)
result = ask_gpt(keys_list,"Could you deliver master_chef_can to right person?")
print(result)
