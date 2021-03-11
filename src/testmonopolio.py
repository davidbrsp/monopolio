from unittest.mock import Mock
import unittest

# from Monopolio import Monopolio as monopolio
import Monopolio

Monopolio = Mock()

# mp = Monopolio()

# mp.simulacao()

# print(mp.text_str)


class TestMonopolio(unittest.TestCase):
    def test_simulacao(self):
        mp = Monopolio()
        mp.__init__()
        # monopolio = Mock()
        # mp = monopolio
        # mp.simulacao_dict = {}
        # mp.text_str = ""
        # mp.html_str = ""
        # mp.max_simulacoes = 300
        mp.numero_de_casas = 20
        # mp.max_rodadas = 1000
        # mp.max_venda = 1000
        # mp.porcentagem_min_venda = .75
        # mp.porcentagem_aluguel = .25
        # mp.bonus_da_rodada = 100
        mp.simulacao()
        assert mp.numero_de_casas > 0 and type(mp.numero_de_casas) == int
        # assert mp.numero_de_casas > 0 and isinstance(mp.numero_de_casas, int)
        assert mp.simulacao.call_count == 1


if __name__ == '__main__':
    unittest.main()
