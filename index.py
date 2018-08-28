    # /index.py

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

app = Flask(__name__)


## Th default route shows a web page . use for testing only
@app.route('/')
def index():
    return render_template('index.html')

## www.xxx/webhook is what you put into the dialogflow
## Within it, it will match to the action name and invole the neccessary function

@app.route('/webhook', methods=['POST'])

def webhook():
    data = request.get_json(silent=True)
    action = data['queryResult']['action']
    
    if (action == 'get_car_recommendation'): 
        return get_car_recommendation(data)
        
    if (action == 'get_movie_detail'): 
        return get_movie_detail(data)    
        
    
def get_movie_detail(data):
   # data = request.get_json(silent=True)
    movie = data['queryResult']['parameters']['movie']
    api_key = os.getenv('OMDB_API_KEY')

    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    
    movie_detail = json.loads(movie_detail)
    response =  """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
    """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])
    
    # response = "THIS IS SOME MOVIE DETAIL"
    reply = {
        "fulfillmentText": response
        }

    return jsonify(reply)


def get_car_recommendation(data):
#    data = request.get_json(silent=True)
    budget = data['queryResult']['parameters']['budget']
    engineSize = data['queryResult']['parameters']['engineSize']
    

    
    response  = "Based on your budget of no more than %s and engineSize of %s" % (budget, engineSize)
    response = response + ", we suggest you get a bicycle"
     
 #   response = "get a bicyce"
    reply = {
        "fulfillmentText": response
        }
    return jsonify(reply)

    

# run Flask app



if __name__ == "__main__":
        app.run()