## Byne challenge

O desafio consiste em arquitetar e desenvolver múltiplos serviços, seguindo as seguintes diretivas:

- Serviço 1: Gerar números pares aleatórios entre 0 e 1000;
- Serviço 2: Gerar números ímpares aleatórios entre 0 e 1000;
- Serviço 3: A cada 500ms, requisitar números do serviço 1 e 2 e fazer a multiplicação entre dois números recebidos. Caso o número multiplicado seja maior que 100000, publicar esse número;
- Serviço 4: Deve receber números publicados e servir esses números para clientes;
- Um cliente poderá se conectar ao serviço 4 e receber a lista dos últimos 100 números publicados;
- A definição de API do cliente fica a seu critério
- O histórico de números publicados deverá ser mantido;
- Testes unitários deverão ser implementados;
- Deverá ser utilizado Python como linguagem para implementação dos serviços;
- A entrega deve ser feita através de um repositório git público de sua escolha;
- A data limite é até 03/07/20 às 23:59:59.

É importante lembrar que nossos produtos possuem foco em uso contínuo 24/7, com ciclo de vida esperado de 10 anos. Tolerância a falhas, redundância e simplicidade são essenciais.

O Gustavo estará disponível para lhe apoiar ou qualquer esclarecimento nos contatos abaixo:

docker-compose up --scale odd_number=2 --scale even_number=2

#Desenvolvimento

A arquitetura que eu escolhi para resolver este desafio foi focada na disponibilidade, resiliência, segurança e performance.

- Os serviços 1 e 2 são duas WEB APIs REST, para consumir as APIs é necessário um token JWT assinado, os serviços são acessados através de um
Loadbalancer que além de distribuir a carga entre os containers dos serviços, proporciona fácil escalabilidade via algum orquestador de containers
como kunernets por exemplo.

- O serviço 3 é um produtor que requisita os serviços 1 e 2, alimentando um banco de dados não relacional (Redis), as consultas aos serviços
são feitas de forma assincrona para diminir o tempo total de execução de consumo das APIs.

- O serviço 4 é uma API REST por que me pareceu fazer mais sentido a nivel de redundância e  Tolerância a falhas, já que podemos usar o mesmo
aprouch dos serviços 1 e 2, usar um load balancer com algumas instancias da API que serve os clients. 

- O historico é mantido no banco não relacional em uma estrutura de LIST, uma lista de strings ordenadas pela ordem de inserção.

- Para rodar os testes apenas digite o comando abaixo na raiz do projeto
    
    
    $ pytest -vv
 
 
Clonando o repositório

    git clone https://github.com/AlexandreProenca/byne_challenge byne


Para iniciar os serviços 
    
    docker-compose up --scale odd_number=2 --scale even_number=2
    

Testar Loadbalancer para números páres

    curl -X GET http://localhost:8082/number/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWNyb3NlcnZpY2VfaWQiOiIxMjM0NTY3ODkwIn0.l9u4wnxv7h0o8JwMgVCZ6p_bC19bBf5xQYIg3SsKCC0
        
Testar Loadbalancer para números ímpares

    curl -X GET http://localhost:8081/number/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWNyb3NlcnZpY2VfaWQiOiIxMjM0NTY3ODkwIn0.l9u4wnxv7h0o8JwMgVCZ6p_bC19bBf5xQYIg3SsKCC0
    
Testar consumo dos 100 ultimos números
  
     curl -X GET http://localhost:8083/numbers/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWNyb3NlcnZpY2VfaWQiOiIxMjM0NTY3ODkwIn0.l9u4wnxv7h0o8JwMgVCZ6p_bC19bBf5xQYIg3SsKCC0
