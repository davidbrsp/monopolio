#!/usr/bin/python
import random


class Monopolio:
    def __init__(self):
        self.simulacao_dict = {}
        self.text_str = ""
        self.html_str = ""
        self.max_simulacoes = 300
        self.numero_de_casas = 20
        self.max_rodadas = 1000
        self.max_venda = 1000
        self.porcentagem_min_venda = .75
        self.porcentagem_aluguel = .25
        self.bonus_da_rodada = 100
        self.simulacao()
        # print('Meu Monopolio\n')

    def __partida(self, tabuleiro={}, jogadores={}):
        jogadores_falidos = 0
        vencedor = {}
        # reinicia os jogadores
        jogadores = list(map(lambda d: d.update({
                'saldo': 300,
                'casa_atual': 0,
                'faliu': False
            }) or d, jogadores))
        # reinicia o tabuleiro
        tabuleiro = list(map(lambda d: d.update({
            'custo_de_venda': d['custo_de_venda'],
            'valor_do_aluguel': d['valor_do_aluguel'],
            'proprietario': ''
            }) or d, tabuleiro))
        for rodadas in range(1, self.max_rodadas + 1):
            for jogador in jogadores:
                if not jogador['faliu']:
                    # joga o dado
                    dado = random.choice([1, 2, 3, 4, 5, 6])
                    limite_do_tabuleiro = (self.numero_de_casas - 1) - jogador['casa_atual'] - dado
                    # ainda nao chegou na ultima casa
                    if limite_do_tabuleiro >= 0:
                        jogador['casa_atual'] += dado
                    else:
                        # Ao completar uma volta no tabuleiro, o jogador ganha 100 de saldo.
                        jogador['casa_atual'] = -1 * limite_do_tabuleiro
                        jogador['saldo'] += self.bonus_da_rodada
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
                        if (jogador['nome'] == 'aleatorio') and random.choice([True, False]):
                            # if (jogador['nome'] == 'aleatorio') and (rd.uniform(0, 1) > .5):
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
                            if casa['proprietario'] == jogador['nome']:
                                casa.update({'proprietario': ''})
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
            if(rodadas >= self.max_rodadas):
                saldo_max_jogador = 0
                for campeao in jogadores:
                    if (campeao['saldo'] >= saldo_max_jogador) and not campeao['faliu']:
                        saldo_max_jogador = campeao['saldo']
                        vencedor = campeao
        return vencedor['nome'], rodadas

    def simulacao(self):
        turnos = []
        tabuleiro = []
        comportamentos = []
        min_venda = self.max_venda * self.porcentagem_min_venda
        jogadores = [{'nome': 'impulsivo'}, {'nome': 'exigente'}, {'nome': 'cauteloso'}, {'nome': 'aleatorio'}]
        # inicializa o tabuleiro
        count = 0
        while count <= self.numero_de_casas:
            venda = random.uniform(min_venda, self.max_venda)
            tabuleiro.append({
                'custo_de_venda': venda,
                'valor_do_aluguel': venda * self.porcentagem_aluguel
            })
            count += 1
        # executa as simulacoes
        count = 0
        while count <= self.max_simulacoes:
            comportamento, turno = self.__partida(tabuleiro, jogadores)
            turnos.append(turno)
            comportamentos.append(comportamento)
            count += 1
        # Quantos turnos em média demora uma partida
        media_de_turnos = sum(turnos) / len(turnos)
        # Qual a porcentagem de vitórias por comportamento dos jogadores
        jogadores = list(map(lambda d: d.update({
            'porcentagem': comportamentos.count(d['nome']) / self.max_simulacoes
        }) or d, jogadores))
        jogadores = sorted(jogadores, key=lambda k: k['porcentagem'], reverse=True)
        self.simulacao_dict = {
            'parametros': {
                'max_simulacoes': self.max_simulacoes,
                'numero_de_casas': self.numero_de_casas,
                'max_rodadas': self.max_rodadas,
                'max_venda': self.max_venda,
                'porcentagem_min_venda': self.porcentagem_min_venda,
                'porcentagem_aluguel': self.porcentagem_aluguel,
                'bonus_da_rodada': self.bonus_da_rodada,
            },
            # Quantas partidas terminam por time out (1000 rodadas)
            'numero_timeouts': turnos.count(self.max_rodadas),
            'media_de_turnos': int(media_de_turnos),
            'comportamentos_list': [{
                    'nome': i['nome'],
                    'porcentagem': (comportamentos.count(i['nome']) / self.max_simulacoes) * 100
                } for i in jogadores],
            # Qual o comportamento que mais vence
            'mais_vence': jogadores[0]['nome'],
        }
        # self.to_text()
        # self.to_html()

    def to_text(self):
        if self.simulacao_dict:
            self.text_str = f"\nPartidas terminadas por timeout: {self.simulacao_dict['numero_timeouts']}\n"
            self.text_str += f"Media de turnos: {self.simulacao_dict['media_de_turnos']}\n"
            self.text_str += f"Porcentagem de vitorias por comportamento dos jogadores:\n"
            for i in range(4):
                comportamento = self.simulacao_dict['comportamentos_list'][i]
                self.text_str += f"\t {i + 1} {comportamento['nome']}: {round(comportamento['porcentagem'], 2)} %\n"
                # \
                #     f"\t {ordem} {i['nome']}: \t {round((comportamentos.count(i['nome']) / max_simulacoes) * 100, 2)} %\n"
            self.text_str += f"Comportamento que mais vence: {self.simulacao_dict['mais_vence']}\n"
            # return text_str

    def to_html(self):
        # self.html_str = self.text_str.replace('\n', '<p>', 1)
        # self.html_str = self.html_str.replace('\n', '</p>\n<p>', 7)
        # self.html_str = self.html_str.replace('\n', '</p>\n')
        self.html_str = self.text_str.replace('%', '&#37;')


def main():
    # simulacao_dict = Monopolio.simulacao(
    #     max_simulacoes=300, numero_de_casas=20, max_rodadas=1000, max_venda=1000, porcentagem_min_venda=.75,
    #     porcentagem_aluguel=.25)
    mp = Monopolio()
    # mp.simulacao()
    # mp.to_text()
    # mp.to_html()

    # max_simulacoes=300, numero_de_casas=20, max_rodadas=1000, max_venda=1000, porcentagem_min_venda=.75,
    # porcentagem_aluguel=.25)
    # text_str = mp.text_str
    mp.to_text()
    print(mp.text_str)
    # print(mp.html_str)


if __name__ == "__main__":
    main()
