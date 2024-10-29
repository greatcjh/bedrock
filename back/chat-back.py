from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

session = boto3.Session(region_name='us-east-1')
bedrock = session.client(service_name='bedrock-runtime')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    initial_message = {
        "role": "user",
        "content": [
            { "text": user_message }
        ],
    }

    response = bedrock.converse(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=[initial_message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0
        },
    )

    response_message = response['output']['message']
    return jsonify({'message': response_message['content'][0]['text']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)