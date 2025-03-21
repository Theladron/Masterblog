from flask import Flask, render_template, request, redirect, url_for

import blog_posts_storage

app = Flask(__name__)


@app.route('/')
def index():
    """
    Home route of the Website. Shows comments with title and author,
    provides like, update and delete buttons, aswell as link to add comments
    :return: static index html
    """
    blog_posts = blog_posts_storage.read_comments()["data"]
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Shows Add-Page upon redirection, adds new blogpost
    in the data storage once submitted
    :return: static add html if redirected to, back to home site once submitted
    """
    if request.method == 'POST':
        name = request.form.get("name")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts_storage.add_comment(name, title, content)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    deletes the chosen Blogpost from the data storage
    :param post_id:
    :return: back to home site
    """
    blog_posts_storage.delete_comment(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Provides editing options and updates title, author and comment once submitted
    :param post_id: unique id of the blogpost
    :return: Post not found if id is invalid, back to update url if
    redirected, back to home site if submitted
    """
    data = blog_posts_storage.read_comments()["data"]
    post = next((post for post in data if post["id"] == post_id), None)
    print(post)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts_storage.update_comment(post_id, author, title, content)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """Ups the like-counter of a post by 1"""
    blog_posts_storage.like_comment(post_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
