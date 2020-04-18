from flask import Flask, request
import requests
app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'Simsimi'# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAACJpmQBpRwBANaZBbCf1TMcNuLE7jC3LYT0ZCKCjVH1b5WradOiKHOJSrzZALDaOUyqFZBWC6SrZBnTuq19lGUYZB3GHKZB3VdSDZAXYOGWZChO3tmNA2g9wIo26D9X4J8dHqpz05PQTXDtMxu8Jf3fxsKiZAQrruYmcaGHuhXgIYl6mte2wCD0sh'# paste your page access token here>"

def get_bot_response():
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "Hello"


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response()
    send_message(sender, response)


# def is_user_message(message):
#     """Check if the message is a message from the user"""
#     return (message.get('message') and message['message'].get('text'))

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        }
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        FB_API_URL,
        params=auth,
        headers=headers,
        json=payload
    )
    
    return response.json()

@app.route("/webhook")
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if x.get('message'):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)
        return "ok"

if __name__ == "__main__":
    app.run()