
def sanitization(web):                      # tokenizing method
    web = web.lower()
    token = []
    dot_token_slash = []
    raw_slash = str(web).split('/')
    for i in raw_slash:
        raw1 = str(i).split('-')            # removing slash to get token
        slash_token = []
        for j in range(0,len(raw1)):
            raw2 = str(raw1[j]).split('.')  # removing dot to get the tokens
            slash_token = slash_token + raw2
        dot_token_slash = dot_token_slash + raw1 + slash_token # all tokens
    token = list(set(dot_token_slash))      # to remove same words  
    if 'com' in token:
        token.remove('com')                 # remove com
    return token