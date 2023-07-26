from flask import Flask, jsonify,request
from flask_cors import CORS
import openai
import json
import os

app = Flask(__name__)
CORS(app)
openai.api_key  = os.environ.get('API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


@app.route("/", methods=['GET'])
def index():
    return jsonify({"message": "Hello World"})


@app.route("/api/get-themes",methods=['POST'])
def get_themes():
    if request.method == "POST":
        if request.json:
            d = []
            data = request.json
            for string in data:
                prompt = f"""
                ```{string['data']}```
                generate a list of themes from the above interview and return output in json format having themes for this interview
                """
                response = get_completion(prompt)
                converted = json.loads(response)
                # res = {}
                # res[str(string['id'])] = converted['themes']
                d.append(converted['themes'])
            print(d)
    
            
            return jsonify({"data": d})
    return ("",404)


if __name__ == "__main__":
    app.run(debug=True)