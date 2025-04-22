import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

def load_blog_posts(file_path='blog_posts.json'):
    """
    Load blog posts from a JSON file with error handling.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of blog posts, or an empty list if the file is not found or invalid.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file is not found or invalid

def save_blog_posts(posts, file_path='blog_posts.json'):
    """
    Save blog posts to a JSON file with error handling.

    Args:
        posts (list): List of blog posts to save.
        file_path (str): Path to the JSON file.

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(posts, file, indent=4)
        return True
    except IOError:
        return False

# Main page
@app.route('/')
def index():
    blog_posts = load_blog_posts()  # Load fresh data
    return render_template('index.html', title='Home', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_blog_posts()  # Load fresh data
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not author or not title or not content:
            return "All fields are required", 400

        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        if not save_blog_posts(blog_posts):
            return "Error saving the blog post", 500

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()  # Load fresh data
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    if not save_blog_posts(blog_posts):
        return "Error saving the updated blog posts", 500

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()  # Load fresh data
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        abort(404, description="Post not found")

    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not author or not title or not content:
            return "All fields are required", 400

        post['author'] = author
        post['title'] = title
        post['content'] = content

        if not save_blog_posts(blog_posts):
            return "Error saving the updated blog post", 500

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

# Custom error handler for 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)