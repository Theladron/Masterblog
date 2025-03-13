from flask import Flask, render_template, request, redirect, url_for
import blog_posts_storage

app = Flask(__name__)



@app.route('/')
def index():
    blog_posts = blog_posts_storage.read_comments()["data"]
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get("name")
        title = request.form.get("title")
        content = request.form.get("content")
        blog_posts_storage.add_comment(name, title, content)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts_storage.delete_comment(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = ""
    data = blog_posts_storage.read_comments()["data"]
    for comment in data["data"]:
        if comment["id"] == post_id:
            post = comment.get["content"]
    if not post:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        for index, comment in enumerate(data["data"]):
            if comment["id"] == post_id:
                data["data"][index]["content"] = "abc"
                blog_posts_storage.update_comment()
                return redirect(url_for('index'))
    # Update the post in the JSON file
    # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)