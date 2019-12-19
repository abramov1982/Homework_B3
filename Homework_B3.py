'''
Внимание! Что бы получить резальтат работы скрипта в консоли необходимо
поменять значение в output="index.html" на None. В скрипте есть комментарий
на этой строчке.
'''


class HTML:
    def __init__(self, output = None):
        self.output = output
        self.children = []
    
    def __iadd__(self, other):
        self.children.append(other)
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)
    
    def __str__(self):
        html = "<html>"
        for child in self.children:
            html +=str(child)
        html += "\n</html>"
        return html


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []
    
    def __iadd__(self, other): 
        self.children.append(other)
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs): 
        return self
    
    def __str__(self): 
        html = "\n<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "</%s>" % self.tag
        return html



class Tag:
    def __init__ (self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.is_single = is_single
        self.attrs = {}
        self.children = []
            
        if klass is not None:
            self.attrs[" class"] = " ".join(klass)
            
        for key, value in kwargs.items():
            if "_" in key:
                key = key.replace("_", "-")
            self.attrs[key] = value
            
    def __enter__ (self):
        return self
        
    def __exit__ (self, *args, **kwargs):
        return self
        
    
    def __iadd__ (self,other):
        self.children.append(other)
        return self

    def __str__ (self):
        attributes = []
        
        for att, value in self.attrs.items():
            attributes.append('{}="{}"' .format(att, value))  
        attributes = " ".join(attributes)
        
        if len(self.children) > 0:
            open_tag = "  <{}{}>".format(self.tag, attributes)
            inner_text = "{}\n".format(self.text)
            for child in self.children:
                inner_text += str("  " + str(child))
            close_tag = "  </{}>\n".format(self.tag)
            return open_tag + inner_text + close_tag
        else:
            if self.is_single:
                return "  <{} {}>\n".format(self.tag, attributes)
            else:
                return "  <{tag}{attributes}>{text}</{tag}>\n".format(tag=self.tag,
                                                                   attributes = attributes,
                                                                   text=self.text
                                                                   )


with HTML(output="index.html") as doc: # Менять output в этой строчке! None выведет результат в консоль.
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body