from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

current_id = 2
data = [
    {
        "id": 1,
        "subject": "Announcement 1 Subject",
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam metus felis, ultrices a vulputate sed, eleifend in eros. Sed varius faucibus nisi, eget consectetur dui tristique id."
    },
    {
        "id": 2,
        "subject": "Announcement 2 Subject",
        "body": "Mauris et auctor turpis. Integer mollis pulvinar facilisis. Suspendisse vulputate finibus tempus. Praesent nec nibh sed lorem imperdiet porttitor volutpat quis lectus. Curabitur eu dapibus purus. Sed semper lacus nunc, ut hendrerit arcu porta eu. Morbi pulvinar nulla quis nisi scelerisque, vitae posuere dui rhoncus."
    },
]

@app.route('/')
def hello_world():
   return 'Hello, World!'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name) 

@app.route('/announcements')
def announcements(name=None):
    return render_template('announcements.html', data=data)

@app.route('/post_announcement', methods=['GET', 'POST'])
def post_announcement():
    global data
    global current_id

    json_data = request.get_json()
    subject = json_data["subject"]
    body = json_data["body"]

    # Add new announcement entry to main 'data' array with
    # a new id and with the subject & body that the user sent in JSON
    # format via POST
    current_id += 1
    new_id = current_id
    new_announcement = {
        "id": current_id,
        "subject": subject,
        "body": body
    }
    data.append(new_announcement)

    # Send back the WHOLE array of data so the client can redisplay it
    return jsonify(data = data)

if __name__ == '__main__':
   app.run(debug = True)




