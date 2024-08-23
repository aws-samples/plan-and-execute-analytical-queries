import json
import time
from collections import OrderedDict

import boto3

from functions import *
from consts import *

funcs = {
    'get_patients': get_patients,
    'get_allergies': get_allergies,
    'get_immunization': get_immunization,
    'filter': filter,
    'count': count,
    'join': join,
    'order_by': order_by,
    'group_by': group_by,
    'limit': limit,
    'select': select,
    'distinct': distinct,
}


def execute_plan(msg):
    tool_use = msg['content'][0]['toolUse']
    plans = tool_use['input']['plans']

    evidences = OrderedDict()
    for plan in plans:
        function_name = plan['function_name']
        evidence_number = plan['evidence_number']

        kwargs = {}
        for k, v in zip(plan['parameters'], plan['parameter_values']):
            if isinstance(v, str) and v.startswith('#E'):
                en = int(''.join([c for c in v if c.isdigit()]))
                v = evidences[en]
            kwargs[k] = v

        func = funcs[function_name]
        evidences[evidence_number] = func(**kwargs)

    final_result = next(reversed(evidences.values()))
    if isinstance(final_result, pd.DataFrame):
        content = {
            'text': final_result.to_json(orient='records')
        }
    else:
        content = {
            'text': f"{final_result}"
        }
    return {
        'role': 'user',
        'content': [{
            'toolResult': {
                'toolUseId': tool_use['toolUseId'],
                'content': [content]
            }
        }]
    }


client = boto3.client('bedrock-runtime', region_name='us-east-1')

model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"


def generate_plan(msgs):
    resp = client.converse(
        modelId=model_id,
        messages=msgs,
        system=[{'text': system_prompt}],
        toolConfig={
            "tools": [plan_tool],
            "toolChoice": {'any': {}}
        },
        inferenceConfig={
            'temperature': 0,
        },
    )
    return resp['output']['message']


def generate_response(msgs):
    resp = client.converse(
        modelId=model_id,
        messages=msgs,
        system=[{'text': system_prompt}],
        toolConfig={
            "tools": [plan_tool],
        },
        inferenceConfig={
            'temperature': 0,
        },
    )
    return resp['output']['message']


if __name__ == '__main__':
    msgs = [
        {
            "role": "user",
            "content": [{"text": "Question: How many customers do I have in Chicopee?"}],
            # "content": [{"text": "Question: What are the immunization codes?"}],
            # "content": [{"text": "Question: Give me the first and last name of the patient with least vaccines and their vaccine count?"}],
        }
    ]

    msg = generate_plan(msgs)
    msgs.append(msg)

    # while True:
    #     new_msg = validate_plan(msg)
    #     if new_msg is None:
    #         break
    #     msgs.append(new_msg)
    #     msg = generate_plan(msgs)
    #     msgs.append(msg)

    print(json.dumps(msg, indent=4))
    msgs.append(execute_plan(msg))

    # bedrock throttle
    for i in range(30):
        print(f'{i}', end=' ')
        time.sleep(1)

    msg = generate_response(msgs)

    print(json.dumps(msg, indent=4))
    print(msg['content'][0]['text'])

