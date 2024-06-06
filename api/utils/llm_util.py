import sys
import json
from openai import OpenAI


def ask_wpversion_details(version):
    api_key = 'sk-proj-tiRDzgM4X7YspsV3iIXeT3BlbkFJKhHihnhnr7dBlU5SHfjK'

    prompt_text = 'Check WordPress version ' + version + ('. Make json in format: {"vulnerabilities": [VULNERABILITY1, '
                                                          'VULNERABILITY2], '
                                                          '"recommendations": <recommendations for found '
                                                          'vulnerabilities>}. Without marking it as ```json...```')

    client = OpenAI(
        api_key=api_key
    )
    completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt_text
            }
        ],
        model='gpt-3.5-turbo'
    )
    generated_text = completion.choices[0].message.content
    print(generated_text, file=sys.stderr)

    return json.loads(generated_text)


def ask_themes_details(themes):
    api_key = 'sk-proj-tiRDzgM4X7YspsV3iIXeT3BlbkFJKhHihnhnr7dBlU5SHfjK'

    prompt_text = ';'.join(themes) + '\n' + ('Make json in format: {"themes": ["name": <extracted_theme_name>, '
                                             '"version": <extracted_theme_version>, "vulnerabilities": <2 sentences '
                                             'if exists>, "recommendations": "2 sentences if any vulnerabilities '
                                             'exists"], [<other_theme_details_if_exists>]}. Without marking it as '
                                             '```json...```')

    client = OpenAI(
        api_key=api_key
    )

    completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt_text
            }
        ],
        model='gpt-3.5-turbo'
    )
    generated_text = completion.choices[0].message.content
    print(generated_text, file=sys.stderr)

    return json.loads(generated_text)


def ask_plugins_details(plugins):
    api_key = 'sk-proj-tiRDzgM4X7YspsV3iIXeT3BlbkFJKhHihnhnr7dBlU5SHfjK'
    prompt_text = ';'.join(plugins) + '\n' + ('Make json in format: {"plugins": ["name": <extracted_theme_name>, '
                                              '"version": <extracted_plugin_version>, "vulnerabilities": <2 sentences '
                                              'if exists>, "recommendations": "2 sentences if any vulnerabilities '
                                              'exists"], [<other_plugin_details_if_exists>]}. Without marking it as '
                                              '```json...```')

    client = OpenAI(
        api_key=api_key
    )

    completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt_text
            }
        ],
        model='gpt-3.5-turbo'
    )
    generated_text = completion.choices[0].message.content
    print(generated_text, file=sys.stderr)

    return json.loads(generated_text)


def ask_generate_report(jsonData):
    api_key = 'sk-proj-tiRDzgM4X7YspsV3iIXeT3BlbkFJKhHihnhnr7dBlU5SHfjK'
    prompt_text = f'{json.dumps(jsonData)}\nYou are a WordPress security engineer. Generate HTML report from JSON file. Ensure that for all findings you provide your own impact and recommendations. No additional words instead of HTML file is required in output.'

    client = OpenAI(
        api_key=api_key
    )

    completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt_text
            }
        ],
        model='gpt-3.5-turbo'
    )
    generated_text = completion.choices[0].message.content
    print(generated_text, file=sys.stderr)

    return generated_text
