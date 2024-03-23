import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC4eb1ff2cfc2148e76532e45162266bfc'
    TWILIO_SYNC_SERVICE_SID = 'IS7d0f7bf81593c72257214039dd3a373a'
    TWILIO_API_KEY = 'SKe8200e5f4184db2e1ca8256787baafa8'
    TWILIO_API_SECRET = '3lZZmNlWkBETNTlfov5wzvrGgBYsfafD'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    textFromNotepad = request.form['text']
    with open('workfile.txt', 'w') as f :
        f.write(textFromNotepad)
    pathToStoreText = 'workfile.txt'
    return send_file(pathToStoreText, as_attachment= True)






    
    
        

    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
