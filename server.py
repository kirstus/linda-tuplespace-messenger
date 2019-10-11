import hashlib, binascii, os

tuplespace = {}

# tuple = (autor, topico, msg, [ ... ,]* topic_msg_number, author_msg_in_topic_number)

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def outp(t, passwd):
    if len(t) not in tuplespace:
        ts = {  'author': {},
                'topic': {},
                'passwd': {}}
        tuplespace[len(t)] = ts

    indice = tuplespace[len(t)]
    author = t[0]
    topic = t[1]
    
    #t = t + (1,2)
    if author is '':
        print('Nome do autor não pode ser em branco!')
        return False
    elif type(author) is not str:
        print('autor não pode ser um número!')
        return False

    if passwd is '':
        print('senha não pode ser em branco!')
    elif type(passwd) is not str:
        print('senha não pode ser um número!')
        return False
    
    if topic is '':
        print('Nome do tópico não pode ser em branco!')
        return False
    elif type(topic) is not str:
        print('topico não pode ser um número!')
        return False

    author = hash(author)
    topic = hash(topic)
    print('hashes: ', author, topic)

    if author not in indice['author']:
        td = {topic: []}
        indice['author'][author] = td

    if topic not in indice['topic']:
        ad = {author: []}
        indice['topic'][topic] = ad

    if author not in indice['passwd'].keys():
        indice['passwd'][author] = hash_password(passwd)
    elif validate_user(t, passwd) == False:
        return False

    indice['author'][author][topic] = t
    indice['topic'][topic][author] = t

def validate_args(t):
    if len(t) not in tuplespace:
        return False
    indice = tuplespace[len(t)]
    author = t[0]
    topic  = t[1]

    if type(author) is not str and type(author) is not type:
        print('autor não pode ser um número!')
        return False
    
    if type(author) is not str and type(author) is not type:
        print('topico não pode ser um número!')
        return False

    if type(author) is type and type(topic) is type:
        print('deve ser fornecido ao menos um dos parâmetros posicionais de identificação (autor|tópico)')
        return False

    h_author = hash(author)
    h_topic  = hash(topic)

    
    if type(author) is type:
        ts = indice['topic'][h_topic]
    elif type(topic) is type:
        ts = indice['author'][h_author]

    #verifica se mais autores participararam desse topico do que esse autor participou de topicos, de modo a otimizar a busca indexada
    elif(len(indice['author'][h_author]) < len(indice['topic'][h_topic])):
        print('muitos autores participararam desse topico') #??
        ts = indice['author'][h_author]
    else:
        print('esse autor participou de muitos topicos')
        ts = indice['topic'][h_topic]
    
    return ts

def validate_user(t,passwd):
    indice = tuplespace[len(t)]
    author = hash(t[0])
    if author not in indice['passwd'].keys():
        print('O usuário não possui uma senha associada')
        return False
    elif verify_password(indice['passwd'][author],passwd) == False:
        print('A senha está incorreta.')
        return False
    return True


def rdp(t):
    ts = validate_args(t)
    if ts == False:
        return False
    #compara os elementos da sua Query com os Elementos do tuplespace
    for key in ts:
        match = 1
        print(ts[key])
        for q,e in zip(t,ts[key]):
            print(q,e)
            if type(q) == type:
                if q != object and q != type(e):
                    print('não deu match de tipo')
                    match = 0
                    break
            elif q != e:
                match = 0
                break

        if match==1:
            return ts[key]
    return False

def inp(t,passwd):
    ts = validate_args(t)
    if ts == False:
        return False
    if validate_user(t,passwd) == False:
        return False

    indice = tuplespace[len(t)]
    ts1 = indice['author'][hash(t[0])]
    ts2 = indice['topic'][hash(t[1])]

    for key in ts:
        match = 1
        print(ts[key])
        for q,e in zip(t,ts[key]):
            print(q,e)
            if type(q) == type:
                if q != object and q != type(e):
                    print('não deu match de tipo')
                    match = 0
                    break
            elif q != e:
                match = 0
                break
        
        if match==1:    #remove todas as menções à tupla, e retorna essa tupla
            ret = ts.pop(key)
            return ret

    return False

#### FALTA
# numerar as tuplas, por topico e por autor por topico.
# ordenar as listas por meio desses numeros de mensagem
# fazer busca binaria para encontrar as tuplas a serem eliminadas


    
senhaa = 'senha a'
senhab = 'koolpass'
b = ('claudinho','assunto',3)
print(type(object))
print(type(str))
print(type(b))
a = (2,2,5)
c = (object, 'assunto', object)
print(b[1])
outp(a,senhaa)
outp(b,senhab)
print('procura b')
print('achou:',rdp(b))
print('procura c')
print('achou:',rdp(c))
print('inp1: ', inp(b,senhab))
print('inp2: ', inp(b,senhab))
b = b + (9,0)
print(b)
