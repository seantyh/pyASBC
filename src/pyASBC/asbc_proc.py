import re

caseRegex = re.compile(r"\(.*?\)")
suffixRegex = re.compile(r"\[.*?\]")
gltRegex = re.compile(
            r'<([\u3400-\u9FFF\uFF00-\uFFEF\u3000-\u303F]+)>',
            re.UNICODE)

def process_text(text_content):        
    if not text_content:
        return []
        # sent_san = whiteRegex.sub("", text_content.strip())

    sent_san = suffixRegex.sub("", text_content.strip())    
    token_list = []
    
    for token in sent_san.split("\u3000"):    
        parts = token.split("(")
        word = parts[0]
        if len(parts) > 1 and len(parts[1])>1:
            pos = parts[1][:-1]
        else:
            pos = ""
        token_list.append((word, pos))
    return token_list