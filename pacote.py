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
        #if elem.split('\036')[0] == 'class: ':
        #print(elem)
        try:
            elem = int(elem)
        except ValueError:
            try:
                elem = float(elem)
            except ValueError:
                elem = elem
        t.append(elem)
        #print(type(elem))
    return t
    #return tuple(t)

if __name__ == '__main__':
    msg = ('oi', 'topic', 99, -17.2, object)
    data = pack(msg)
    b = unpack(data)
    print(b)
    for e in b:
        print(type(e))
