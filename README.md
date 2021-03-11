

Para executar a simulacao basta mudar para o diretorio ./src e fazer:

**python ServerMonopolio.py**

Caso queira também é possível usar Docker para executar a aplicacao, para isso basta fazer no diretorio raiz:

**docker build --pull --rm -f "Dockerfile" -t monopolio:latest "."**

**docker run --rm -d  -p 8000:8000/tcp -p 9000:9000/tcp monopolio:latest**

Para realizar alguns testes (unit e mock):

**python testmonopolio.py**

* **Maximo de simulacoes** (Default: 300)

    Numero maximo e partidas a serem simuladas

* **Numero de casas** (Default: 20)

    numero de casas do tabuleiro

* **Maximo de rodadas** (Default: 1000)

    numero maximo de rodadas de cada partida

* **Valor maximo de venda** (Default: 1000.)

    valor maximo da venda as propriedades

* **Porcentagem minima de venda** (Default: .75)

    percentual do valor maximo para ser atribuida ao valor minimo de venda da propriedade

* **Porcentagem do aluguel** (Default: .25)

    porcentagem do valor de venda que sera o maximo preco pela qual a propriedade pode ser alugada

* **Bonus da rodada** (Default: 100)

    Quando o jogador ganha a cada rodada

Melhorias a serem implantadas (trabalho em progresso):

* Ainda de forma experimental, é possível usar o arquivo ".src/form.html" aberto diretamente no navegador (duplo clique no arquivo em muitos sistemas) para solicitar para a api diferentes resultados. O proximo passo e colocar esse arquivo para ser servido diretamente pelo http.server.

* Melhorar o testes (unit mock)

* Refatorar o metodo *partida()*