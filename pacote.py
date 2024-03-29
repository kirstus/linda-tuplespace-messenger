tipo = {    'object' : object,
            'str' : str,
            'int' : int,
            'float' : float}

def pack(t):
    data = ''
    for elem in t:
        if type(elem) is type:
            data += 'class: ' + '\036' + str(elem).split("'")[1] + '\037,'
        else:
            data += str(elem) + '\037,'
    return data[:-2]

def unpack(data):
    t = []
    for elem in data.split('\037,'):
        try:
            elem = int(elem)                #int
        except ValueError:
            try:
                elem = float(elem)          #float
            except ValueError:
                elem = elem                 #str
                aux = elem.split('\036')
                if aux[0] == 'class: ':
                    #print(aux[1])
                    elem = tipo[aux[1]]     #tipos
        t.append(elem)
        #print(type(elem))
    return t
    #return tuple(t)

def clean(t):
    l = []
    for elem in t:
        if type(elem) is type:
            elem = str(elem)
        l.append(elem)
    return l

def to_json(t):
    l = clean(t)
    d = {   'author':   l[0],
            'topic':    l[1],
            'message':  l[2],
            'timestamp':l[3],
            'id':       l[4]
        }
    return d


if __name__ == '__main__':
    msg = ('oi', 'topic', 99, -17.2, object)
    data = pack(msg)
    b = unpack(data)
    print(b)
    for e in b:
        print(type(e))
    print(to_json(msg))
    print(type(msg) is tuple)
