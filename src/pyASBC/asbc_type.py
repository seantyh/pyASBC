from .asbc_proc import process_text

class Author:
    def __init__(self, elem):
        for child in elem.iterchildren():
            setattr(self, child.tag, child.text)
    def __repr__(self):
        return "<object Author>"

class Text:
    def __init__(self, elem):
        self.sentences = []
        for sentence in elem.xpath("sentence"):
            try:
                self.sentences.append(process_text(sentence.text))
            except Exception as ex:
                raise Exception(str(ex), sentence.sourceline)                

    def __repr__(self):
        return f"<Text: {len(self.sentences)} sentences>"

class Article():
    def __init__(self, elem):
        for key, value in elem.items():
            setattr(self, key, value)
        for child in elem.iterchildren():
            if child.tag == "author":
                setattr(self, child.tag, Author(child))
            elif child.tag == "text":
                try:
                    setattr(self, child.tag, Text(child))
                except Exception as ex:
                    ex_info = (elem.attrib.get("no"), *ex.args)
                    raise Exception(ex_info)                    
            else:
                setattr(self, child.tag, child.text)