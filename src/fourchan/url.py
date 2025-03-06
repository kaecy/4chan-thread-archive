import re
from fourchan import errors

class FourchanThreadUrl:
    def __init__(self, board, thread):
        self.board = board
        self.thread = thread

class FourchanInvalidUrl:
    def __init__(self, error):
        self.error = error

class FourchanUrl:
    def __new__(cls, url):
        match = re.match("https://boards\\.4chan\\.org/(.+)/thread/(.+)", url)
        if match:
            return FourchanThreadUrl(match[1], match[2])
        else:
            return FourchanInvalidUrl(errors.ErrorInvalidURL)
