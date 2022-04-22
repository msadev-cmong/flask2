from flask import Flask, request, redirect, app

app = Flask(__name__)


nextId = 4
topics = [
    {'id': 1, 'title':'서울', 'body':'전국 상황은~'},
    {'id': 2, 'title':'부산', 'body':'연령별 상황은~'},
    {'id': 3, 'title':'대구', 'body':'유형별 상황은~'},
    {'id': 4, 'title':'인천', 'body':'전국 상황은~'},
    {'id': 5, 'title':'광주', 'body':'전국 상황은~'},
    {'id': 6, 'title':'대전', 'body':'전국 상황은~'},
    {'id': 7, 'title':'울산', 'body':'전국 상황은~'},
    {'id': 8, 'title':'세종', 'body':'전국 상황은~'},
    {'id': 9, 'title':'경기', 'body':'전국 상황은~'},
    {'id': 10, 'title':'강원', 'body':'전국 상황은~'},
    {'id': 11, 'title':'충북', 'body':'전국 상황은~'},
    {'id': 12, 'title':'충남', 'body':'전국 상황은~'},
    {'id': 13, 'title':'전북', 'body':'전국 상황은~'},
    {'id': 14, 'title':'전남', 'body':'전국 상황은~'},
    {'id': 15, 'title':'경북', 'body':'전국 상황은~'},
    {'id': 16, 'title':'경남', 'body':'전국 상황은~'},
    {'id': 17, 'title':'창원', 'body':'전국 상황은~'},
    {'id': 18, 'title':'제주', 'body':'전국 상황은~'},
]


def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            <h1><a href="/">소방통계</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''


def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags


@app.route('/')
def index():
    return template(getContents(), '<h2>응급상황</h2>안전요령')


@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET': 
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')


app.run(debug=True)