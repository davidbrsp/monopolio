# Monopolio

Para executar a simulacao basta mudar para o diretorio ./src e fazer:

``` bash
python ServerMonopolio.py
```

Caso queira também é possível usar Docker para executar a aplicacao, para isso basta fazer no diretorio raiz:

``` bash
docker build --pull --rm -f "**Dockerfile**" -t monopolio:latest "."
```

``` bash
docker run --rm -d  -p 8000:8000/tcp -p 9000:9000/tcp monopolio:latest
```

Para realizar alguns testes (unit e mock)

``` bash
 python testmonopolio.py
```

## Parametros

* **Maximo de simulacoes** (Default: **300**)

    Numero maximo e partidas a serem simuladas.

* **Numero de casas** (Default: **20**)

    Numero de casas do tabuleiro.

* **Maximo de rodadas** (Default: **1000**)

    Numero maximo de rodadas de cada partida.

* **Valor maximo de venda** (Default: **1000.0**)

    Valor maximo da venda as propriedades.

* **Porcentagem minima de venda** (Default: **.75**)

    Percentual do valor maximo para ser atribuida ao valor minimo de venda da propriedade

* **Porcentagem do aluguel** (Default: **.25**)

    Porcentagem do valor de venda que sera o maximo preco pela qual a propriedade pode ser alugada.

* **Bonus da rodada** (Default: **100**)

    Quanto o jogador ganha ao final de cada rodada.

## Melhorias a serem implementadas (trabalho em progresso)

* [ ] Ainda de forma experimental, é possível usar o arquivo ".src/form.html" aberto diretamente no navegador (duplo clique no arquivo em muitos sistemas) para solicitar para a api diferentes resultados. O proximo passo e colocar esse arquivo para ser servido diretamente pelo http.server.

* [ ] Melhorar o testes (unit mock)

* [ ] Refatorar o metodo *partida()*
