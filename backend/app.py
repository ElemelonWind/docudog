from flask import Flask
from flask_restful import Resource, Api, reqparse
import urllib.request as urllib3
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv 
import os
import requests

app = Flask(__name__)
api = Api(app)

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

class GetLinks(Resource):
    def get(self):
        return {'status': 'success', 'message': 'API' }, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, help='URL to fetch links')
        args = parser.parse_args()
        url = args['url']

        def getLinks(url):
            session = requests.Session()
            response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            newlinks = []
            for link in links:
                print(link)
                try:
                    if link['href'].startswith('/'):
                        link['href'] = url + link['href']
                    if link['href'].startswith('#'):
                        continue
                    newlinks.append(link['href'])
                except:
                    newlinks.append(link)
            return newlinks

        try:
            links = getLinks(url)
            return {'status': 'success', 'message': 'Links fetched successfully', 'data': links}, 200
        except:
            return {'status': 'error', 'message': 'Error fetching links'}, 400
    
class SendMessage(Resource):
    def get(self):
        return {'status': 'success', 'message': 'API' }, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prompt', type=str, help='Message to send')
        parser.add_argument('history', type=list, help='History of messages', location='json')
        parser.add_argument('links', type=list, help='Links fetched', location='json')
        args = parser.parse_args()

        prompt = args['prompt']
        history = args['history']
        links = args['links']
        
        def chat_context (history, model, prompt, links):
            chat = model.start_chat(history=history)
            linkstrings=""
            for content in links:
                linkstrings += content + ", "

            response=chat.send_message(content=("Please answer this prompt: " + prompt + "\nAlso use the following links for context if applicable, if not please ignore: " + linkstrings))
            return response;
    
        response = chat_context(history, model, prompt, links).text

        return {'status': 'success', 'message': response}, 200
    
api.add_resource(GetLinks, '/getlinks')
api.add_resource(SendMessage, '/sendmessage')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")