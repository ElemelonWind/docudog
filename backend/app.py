from flask import Flask
from flask_restful import Resource, Api, reqparse
import urllib.request as urllib3
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class GetLinks(Resource):
    def get(self):
        return {'status': 'success', 'message': 'API' }, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, help='URL to fetch links')
        args = parser.parse_args()
        url = args['url']

        def getLinks(url):
            page=urllib3.urlopen(url)
            soup = BeautifulSoup(page.read(), features="lxml")
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

        links = getLinks(url)
        print(links)
        return {'status': 'success', 'message': 'Links fetched successfully', 'data': links}, 200
    
api.add_resource(GetLinks, '/getlinks')

if __name__ == '__main__':
    app.run(debug=True)