import sys
import os
import json
import requests

import fourchan.url
import fourchan.errors

def fetch_4chan_thread_data(url):
    """Fetch the thread data from 4chan."""
    if type(url) != fourchan.url.FourchanThreadUrl:
        url = fourchan.url.FourchanUrl(url)
        if url == fourchan.url.FourchanInvalidUrl:
            return None, fourchan.errors.ErrorInvalidURL

    board, thread = url.board, url.thread

    thread_url = f"https://a.4cdn.org/{board}/thread/{thread}.json"
    local_thread_data_filename = f"{thread}\\metadata.json"

    # Make the folder where files will be placed. This folder uses the thread_id
    # so multiple archives can be made in the same parent folder.
    if not os.path.exists(thread):
        os.mkdir(thread)

    if os.path.exists(local_thread_data_filename):
        print("Loading local thread data file.")
        posts = json.load(open(local_thread_data_filename))['posts']
    else:
        response = requests.get(thread_url)
        
        if response.status_code != 200:
            return None, ErrorReceiving
        data = response.json()
        posts = data['posts']

        data['board'] = board
        json.dump(data, open(local_thread_data_filename, "w"))

    # Download media.
    template_img_url = f"https://i.4cdn.org/{board}/"
    images_dir = f"{thread}\\media"

    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    for post in posts:
        if "filename" in post:
            filename = str(post['tim']) + post['ext']
            localfilename = os.path.join(images_dir, filename)
            if not os.path.exists(localfilename):
                url = template_img_url + filename
                response = requests.get(url, stream=True)
                #print(f"Downloading {url}\nStatus:", response.status_code)
                if response.status_code == 200:
                    with open(localfilename, "wb") as file:
                        for chunk in response.iter_content(1024):  # Download in chunks
                            file.write(chunk)
            else:
                print(f"File {filename} already exists.")
    
    return posts, None

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
            localname = "media/" + str(post['tim']) + post['ext']
            md_content +=  f"File: <a href=\"{localname}\">{filename}</a>\n\n"
        md_content += "<hr>\n\n"
    return md_content

def save_to_file(md_content, dir, filename="archive.md"):
    """Save the generated Markdown content to a file."""
    with open(os.path.join(dir, filename), "w", encoding="utf-8") as file:
        file.write(md_content)

def main():
    args = len(sys.argv)-1
    # Fetch and generate Markdown
    if args >= 1:
        thread_url = fourchan.url.FourchanUrl(sys.argv[1])
        if type(thread_url) == fourchan.url.FourchanInvalidUrl:
            exit(f"Error: {thread_url.error.Message}")

        thread_data, err = fetch_4chan_thread_data(thread_url)
        if err:
            exit(f"Error: {err.Message}")
        
        markdown_content = generate_markdown(thread_data)
        
        save_to_file(markdown_content, thread_url.thread)
        print(f"Markdown document generated: {thread_url.thread}\\4chan_archive.md")

if __name__ == "__main__":
    main()
