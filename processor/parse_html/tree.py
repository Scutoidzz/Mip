class Node:
    def __init__(self, tag=None, attributes=None, text=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.text = text
        self.children = []


    