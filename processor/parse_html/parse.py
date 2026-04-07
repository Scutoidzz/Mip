from parse_html.tree import Node

void_tags = ["br", "img", "input", "hr", "nerb", "meta", "link", "video"]

def parser(html: str):
    root = Node(tag="root")
    stack = [root]
    i = 0
    while i < len(html):
        if html[i] == "<":
            end = html.find(">", i)
            if end != -1:
                tag_str = html[i:end+1]
                tag, attrs, is_closing, is_self_closing = parse_element(tag_str)
                
                if is_closing:
                    if stack and stack[-1].tag == tag:
                        stack.pop()
                elif tag in void_tags or is_self_closing:
                    node = Node(tag=tag, attributes=attrs)
                    stack[-1].children.append(node)
                else:
                    node = Node(tag=tag, attributes=attrs)
                    stack[-1].children.append(node)
                    stack.append(node)
                i = end + 1
            else:
                i += 1
        else:
            end = html.find("<", i)
            if end == -1:
                end = len(html)
            text = html[i:end].strip()
            if text:
                node = Node(text=text)
                stack[-1].children.append(node)
            i = end
    return root
    

def parse_element(element: str):
    is_closing = element.startswith("</")
    is_self_closing = element.endswith("/>")
    element = element.split(">")[0].replace("/", "")
    tag = element.split(" ")[0].replace("<", "")
    attributes = element.split(" ")[1:]
    attribute_dict = {}
    for i in attributes:
        if "=" in i:
            parts = i.split("=", 1)
            if len(parts) == 2 and parts[1].startswith("'\""):
                attribute_dict[parts[0]] = parts[1].strip('"\'')
    return tag, attribute_dict, is_closing, is_self_closing