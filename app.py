import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# Load blog posts from JSON file
with open('blog_posts.json', 'r') as file:
    blog_posts = json.load(file)

#Main page
@app.route('/')
def index():
    return render_template('index.html', title='Home', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Create a new post
        new_post = {
            'id': len(blog_posts) + 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post and save to JSON file
        blog_posts.append(new_post)
        with open('blog_posts.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global blog_posts
    # Remove the post with the given id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list to the JSON file
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        json.dump(blog_posts, file, indent=4)

    # Redirect to the home page
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    global blog_posts
    # Fetch the blog post by ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with the new data from the form
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Save the updated list to the JSON file
        with open('blog_posts.json', 'w', encoding='utf-8') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to the home page
        return redirect(url_for('index'))

    # Render the update form with the current post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)