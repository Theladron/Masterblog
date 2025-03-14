import json


def read_comments():
    with open("blog_posts.json", "r") as handle:
        return json.loads(handle.read())


def add_comment(author, title, content):
    data = read_comments()
    new_id = data["NEXT_POST_ID"]
    data["data"].append({
        "id": new_id,
        "author": author,
        "title": title,
        "content": content,
        "likes": 0
    })
    data["NEXT_POST_ID"] = new_id + 1
    with open("blog_posts.json", "w") as handle:
        handle.write(json.dumps(data, indent=4))


def update_comment(update_id, author, title, content):
    data = read_comments()
    for index, comment in enumerate(data["data"]):
        if comment["id"] == update_id:
            data["data"][index]["author"] = author
            data["data"][index]["title"] = title
            data["data"][index]["content"] = content
    with open("blog_posts.json", "w") as handle:
        handle.write(json.dumps(data, indent=4))


def delete_comment(del_id):
    data = read_comments()
    for index, comment in enumerate(data["data"]):
        if comment["id"] == del_id:
            del data["data"][index]
    with open("blog_posts.json", "w") as handle:
        handle.write(json.dumps(data, indent=4))

def like_comment(post_id):
    data = read_comments()
    for index, comment in enumerate(data["data"]):
        if comment["id"] == post_id:
            data["data"][index]["likes"] += 1
    with open("blog_posts.json", "w") as handle:
        handle.write(json.dumps(data, indent=4))
