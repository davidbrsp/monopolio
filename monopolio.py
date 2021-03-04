#!/usr/bin/python
import random as rd

def partida(tabuleiro={}, numero_de_casas=20, jogadores={}, max_rodadas=1000):
    for jogador in jogadores:
        jogador.update({'saldo': 300, 'casa_atual': 0, 'faliu' : False})
    jogadores_falidos = 0
    vencedor = {}
    for casa in tabuleiro:
        tabuleiro[casa].update({'proprietario': ''})
    for rodadas in range(1, max_rodadas + 1):
        for jogador in jogadores:
            if not jogador['faliu']:
                # joga o dado
                dado=int(rd.uniform(1, 7))
                # print(f"{i} {dado}")
                if (jogador['casa_atual'] + dado <= (numero_de_casas - 1)):
                    jogador['casa_atual'] += dado
                else:
                    jogador['casa_atual'] += dado - (numero_de_casas - 1)
                    # Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.
                    jogador['saldo'] += 100
                casa_atual = tabuleiro[jogador['casa_atual']]
                # analisa a compra de propriedade caso ela não tenham dono e o jogador tenha o dinheiro da venda
                if not casa_atual['proprietario'] and (jogador['saldo'] >= casa_atual['custo_de_venda']):
                    compra = False
                    # compra sempre
                    if jogador['nome'] == 'impulsivo':
                        compra = True
                    # compra se o aluguel for maior que 50
                    if (jogador['nome'] == 'exigente') and (casa_atual['valor_do_aluguel'] > 50):
                        compra = True
                    # compra se sobrar 80 de saldo depois da compra
                    if (jogador['nome'] == 'cauteloso') and ((jogador['saldo'] - casa_atual['custo_de_venda']) >= 80):
                        compra = True
                    # 50% de chance de comprar
                    if (jogador['nome'] == 'aleatorio') and (rd.uniform(0, 1) > .5):
                        compra = True
                    if compra:
                        # Ao comprar uma propriedade, o jogador perde o dinheiro e ganha a posse da propriedade.
                        jogador['saldo'] -= casa_atual['custo_de_venda']
                        tabuleiro[jogador['casa_atual']].update({'proprietario': jogador['nome']})
                # Ao cair em uma propriedade que tem proprietário, ele deve pagar ao proprietário o valor do aluguel
                # da propriedade.
                if casa_atual['proprietario'] != jogador['nome']:
                    for proprietario in jogadores:
                        if proprietario['nome'] == casa_atual['proprietario']:
                            jogador['saldo'] -= casa_atual['valor_do_aluguel']
                            proprietario['saldo'] += casa_atual['valor_do_aluguel']
                            break
                # Um jogador que fica com saldo negativo perde o jogo, e não joga mais.
                if jogador['saldo'] < 0:
                    jogador['faliu'] = True
                    jogadores_falidos += 1
                    # Perde suas propriedades e portanto podem ser compradas por qualquer outro jogador
                    for casa in tabuleiro:
                        if tabuleiro[casa]['proprietario'] == jogador['nome']:
                            tabuleiro[casa].update({'proprietario': ''})
                    # impede que o ultimo jogado venha a falir na ultima jogada
                    if jogadores_falidos == 3:
                        break
        # Termina quando restar somente um jogador com saldo positivo, a qualquer momento da partida. Esse jogador
        # é declarado o vencedor.
        if jogadores_falidos == 3:
            for campeao in jogadores:
                if not campeao['faliu']:
                    vencedor = campeao
                    break
            break
        # o jogo termina na milésima rodada com a vitória do jogador com mais saldo.
        # O critério de desempate é a ordem de turno dos jogadores nesta partida.
        if(rodadas >= max_rodadas):
            saldo_max_jogador = 0
            for campeao in jogadores:
                if (campeao['saldo'] >= saldo_max_jogador) and not campeao['faliu']:
                    saldo_max_jogador = campeao['saldo']
                    vencedor = campeao
    return vencedor['nome'], rodadas

def simulacao(max_simulacoes=300, numero_de_casas=20, max_rodadas=1000, max_venda=1000, porcentagem_min_venda=.75,porcentagem_aluguel=.25):
    tabuleiro = {}
    jogadores = [{'nome': 'impulsivo'}, {'nome': 'exigente'}, {'nome': 'cauteloso'}, {'nome': 'aleatorio'}]
    min_venda = max_venda * porcentagem_min_venda
    turnos = []
    comportamentos = []
    ordem = 0
    for i in range(numero_de_casas):
        # venda = rd.uniform(min_venda, max_venda * int(rd.uniform(1, 20)))
        venda = rd.uniform(min_venda, max_venda)
        tabuleiro.update({i: {'custo_de_venda': venda, 'valor_do_aluguel': venda * porcentagem_aluguel,}})
    for i in range(max_simulacoes):
        comportamento, turno = partida(tabuleiro, numero_de_casas, jogadores, max_rodadas)
        turnos.append(turno)
        comportamentos.append(comportamento)
    vencedores = [{
            'apelido': 'Jogador 1 (Impulsivo)',
            'porcentagem': comportamentos.count('impulsivo') / max_simulacoes
        },{
            'apelido': 'Jogador 2  (Exigente)',
            'porcentagem': comportamentos.count('exigente') / max_simulacoes
        },{
            'apelido': 'Jogador 3 (Cauteloso)',
            'porcentagem': comportamentos.count('cauteloso') / max_simulacoes
        },{
            'apelido': 'Jogador 4 (Aleatorio)',
            'porcentagem': comportamentos.count('aleatorio') / max_simulacoes
        }]
    for jogador in jogadores:
        jogador.update({'apelido': jogador['nome'], 'porcentagem': comportamentos.count(jogador['nome']) / max_simulacoes})
    media_de_turnos = sum(turnos) / len(turnos)
    jogadores = sorted(jogadores, key=lambda k: k['porcentagem'], reverse=True)
    print(f"Partidas terminadas por timeout: {turnos.count(1000)}")
    print(f"Media de turnos: {int(media_de_turnos)}")
    print(f"Porcentagem de vitórias por comportamento dos jogadores:")
    for i in jogadores:
        ordem += 1
        print(f"\t {ordem}º {i['nome']}: \t {round((comportamentos.count(i['nome']) / max_simulacoes) * 100, 2)} %")
    print(f"Comportamento que mais vence: {vencedores[0]['apelido']}")

def main():
    simulacao(max_simulacoes=300, numero_de_casas=20, max_rodadas=1000, max_venda=1000, porcentagem_min_venda=.75,porcentagem_aluguel=.25)
    # print("Hello World!")

if __name__ == "__main__":
    main()
