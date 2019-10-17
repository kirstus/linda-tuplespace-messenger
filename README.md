
### Especificações da parte 1: 
Sistema em python que implemente uma espaço de dados compartilhado persistente, nos moldes do Linda Tuplespace (com as operações in, rd e out) que permita a implementação de um mini-blog com postagens de conteúdos por tópicos, sua leitura por tópicos e a retirada da mensagem somente por quem postou.

Para executar a parte 1, basta executar o servidor `server.py` e o cliente `client.py`, onde você deve especificar seu nome de usuário, senha e tópico que deseja enviar as mensagens. Após isso, toda mensagem digitada será adicionada em uma tupla apropriada e enviada ao servidor.
O armazenamento é persistente, portanto todas as tuplas e logins serão salvos, a menos que o usuário autor dessas tuplas deseje remove-las.

### Especificações parte 2:  
Wrapper usando REST api neste sistema que permita a conexão de clientes remotos a este microblog se conectarem  através de REST. 

Para executar a parte 2, basta rodar o executável `app.py` e realizar as operações REST como nos exemplos abaixo, ou conectar-se por meio de um navegador no _endpoint_ de preferência.
Listar todos os autores:
`curl http://127.0.0.1:5000/messenger/authors`
Listar todos os tópicos:
`curl http://127.0.0.1:5000/messenger/topics`
Listar as mensagens de um tópico:
`curl http://127.0.0.1:5000/messenger/topics/sd`
Escrever uma mensagem em um tópico:
 ` curl -i -H "Content-Type: application/json" -X PUT -d '{"passwd": "100a", "author": "eu", "topic": "sd", "msg": "mensagemm"}'  http://127.0.0.1:5000/messenger/topics/sd `
Remover uma mensagem de sua autoria de um tópico: 
`curl -i -H "Content-Type: application/json" -X DELETE -d '{"passwd": "b"}'  http://127.0.0.1:5000/messenger/topics/sd/6`


