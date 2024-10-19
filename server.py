from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

current_id = 2
annnouncements_data = [
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

#Arrays for sortability
todo_list_data = [
    {
        'Alex' : [
            {
                'task' : 'Initialize Git Repo',
                'date' : '12-25-2024'
            },
            {
                'task' : 'Push Changes',
                'date' : '12-30-2024'
            },
        ]  
    },
    {
        'Barney' : [
            {
                'task' : 'Fork Alex Git Repo',
                'date' : '12-26-2024'
            },
            {
                'task' : 'Resolve Merge Conflict',
                'date' : '12-31-2024'
            },
        ]
    }
]

@app.route('/')
def hello_world(data=todo_list_data):
   return render_template('ToDoList.html', data=data)

@app.route('/add_teammate', methods=['POST'])
def add_teammate():
    global todo_list_data
    sorted_names = request.get_json()

    for i in range(len(todo_list_data)):
        if list(todo_list_data[i].keys())[0] != sorted_names[i]:
            todo_list_data.insert(i, {sorted_names[i] : []})
        elif i == len(todo_list_data) - 1:
            todo_list_data.append({sorted_names[i + 1] : []})

    if len(todo_list_data) == 0:
        todo_list_data.append({sorted_names[0] : []})
    return {
        'success' : True
    }

@app.route('/add_item', methods=['POST'])
def add_item():
    global todo_list_data
    name_and_tasks = request.get_json()
    
    for name, tasks in name_and_tasks.items():
        # print(name, tasks)
        for i in range(len(todo_list_data)):
            if list(todo_list_data[i].keys())[0] == name:
                todo_list_data[i][name] = tasks
                break

    return {
        'success' : True
    }

@app.route('/item_checked', methods=['POST'])
def item_checked():
    global todo_list_data
    name_and_task = request.get_json()
    
    for name, task in name_and_task.items():
        for object in todo_list_data:
            if list(object.keys())[0] == name:
                for value in object.values():
                    for i in range(len(value)):
                        if value[i]['task'] == task:
                            value[i]['checked'] = True                    
                break
    # print(todo_list_data)

    return {
        'success' : True
    }

@app.route('/item_unchecked', methods=['POST'])
def item_unchecked():
    global todo_list_data
    name_and_task = request.get_json()
    
    for name, task in name_and_task.items():
        for object in todo_list_data:
            if list(object.keys())[0] == name:
                for value in object.values():
                    for i in range(len(value)):
                        if value[i]['task'] == task:
                            value[i]['checked'] = False 
                            break                  
                break
    # print(todo_list_data)
    return {
        'success' : True
    }

@app.route('/clear_completed', methods=['POST'])
def clear_completed():
    # print("I AM IN CLEAR COMPLETED")
    global todo_list_data
    name_and_task = request.get_json()

    for name, task in name_and_task.items():
        for object in todo_list_data:
            if list(object.keys())[0] == name:
                for value in object.values():
                    for i in range(len(value)):
                        if value[i]['task'] == task:
                            value.pop(i)
                            break             
                break
    return {
        'success' : True
    }

@app.route('/reset', methods=['POST'])
def reset():
    global todo_list_data
    todo_list_data = []
    # print(todo_list_data)
    return {
        'success' : True
    }

@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    global todo_list_data

    return jsonify(todo_list_data)

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name) 

@app.route('/announcements')
def announcements(data=annnouncements_data):
    return render_template('announcements.html', data=data)

@app.route('/post_announcement', methods=['GET', 'POST'])
def post_announcement():
    global announcements_data
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
    annnouncements_data.append(new_announcement)

    # Send back the WHOLE array of data so the client can redisplay it
    return jsonify(data = annnouncements_data)

@app.route('/api/announcements', methods=['GET'])
def api_announcements():
    global annnouncements_data

    return jsonify(data = annnouncements_data)

@app.route('/api/announcements/<index>', methods=['GET'])
def api_announcements_index(index=0):
    global annnouncements_data

    return jsonify(data=annnouncements_data[index])

@app.route('/api/todo', methods=['GET'])
def api_todo():
    global todo_list_data

    return jsonify(data=annnouncements_data)

@app.route('/api/todo/<index>', methods=['GET'])
def api_todo_index(index=0):
    #This returns, based on alphebatical ordering, the person on <index>. For example, index = 1 would return the second person alphabetically sorted.
    global todo_list_data

    return jsonify(data=annnouncements_data[index])

if __name__ == '__main__':
   app.run(debug = True)




