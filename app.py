import json
from flask import Flask, render_template

app = Flask(__name__)
# Load blog posts from JSON file
with open('blog_posts.json', 'r') as file:
    blog_posts = json.load(file)

@app.route('/')
def index():
    return render_template('index.html', title='Home', posts=blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)