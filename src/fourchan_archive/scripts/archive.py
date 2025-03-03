import sys
import os
import re
import json
import requests

def fetch_4chan_thread_data(url):
    """Fetch the thread data from 4chan."""
    match = re.match("https://boards\\.4chan\\.org/(.+)/thread/(.+)", url)
    board = match[1]
    thread = match[2]
    url = f"https://a.4cdn.org/{board}/thread/{thread}.json"
    localName = f"{board}-{thread}.json"

    if os.path.exists(localName):
        print("Loading local file.")
        posts = json.load(open(localName))
    else:
        response = requests.get(url)
        
        if response.status_code != 200:
            print("Failed to retrieve data.")
            return []
        posts = response.json()['posts']

        json.dump(posts, open(localName, "w"))

    # Download image data.
    template_img_url = f"https://i.4cdn.org/{board}/"
    if not os.path.exists(thread):
        os.mkdir(thread)
        for post in posts:
            if "filename" in post:
                filename = str(post['tim']) + post['ext']
                url = template_img_url + filename
                response = requests.get(url, stream=True)
                print(f"Downloading {url}\nStatus:", response.status_code)
                if response.status_code == 200:
                    with open(thread + "\\" + filename, "wb") as file:
                        for chunk in response.iter_content(1024):  # Download in chunks
                            file.write(chunk)
    
    return posts

def generate_markdown(posts):
    """Generate a Markdown document from 4chan threads."""
    op = str(posts[0]['no'])
    md_content = "# 4chan Thread Archive\n\n"
    md_content += "Thread " + op + "\n\n"

    for post in posts:
        id = f"<a name=\"p{post['no']}\" href=\"#{post['no']}\">{post['no']}</a>"
        md_content += "## " + post['name'] + " No. " + id
        if "com" in post:
            md_content += "\n\n" + post['com'] + "\n\n"
        else:
            md_content += "\n\n[no comment left]\n\n"
        if "filename" in post:
            filename = post['filename'] + post['ext']
            localname = str(post['tim']) + post['ext']
            md_content +=  f"File: <a href=\"{op}/{localname}\">{filename}</a>\n\n"
        md_content += "<hr>\n\n"
    return md_content

def save_to_file(md_content, filename="4chan_archive.md"):
    """Save the generated Markdown content to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(md_content)

def main():
    args = len(sys.argv)-1
    # Fetch and generate Markdown
    if args == 1:
        url = sys.argv[1]
        threads = fetch_4chan_thread_data(url)
        markdown_content = generate_markdown(threads)
        save_to_file(markdown_content)

        print("Markdown document generated: 4chan_archive.md")

if __name__ == "__main__":
    main()
