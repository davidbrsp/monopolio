import urllib.request
import json


class FrontMonopolio:

    def __init__(self):
        self.simulacao_dict = {}
        self.text_str = ""
        self.html_str = ""
        self.url = 'http://localhost:9000/api/monopolio'

    def get_simulacao(self):
        request_json = urllib.request.urlopen(self.url)
        self.simulacao_dict = json.load(request_json)

    def to_text(self):
        if self.simulacao_dict:
            self.text_str = f"\nPartidas terminadas por timeout: {self.simulacao_dict['numero_timeouts']}\n"
            self.text_str += f"Media de turnos: {self.simulacao_dict['media_de_turnos']}\n"
            self.text_str += f"Porcentagem de vitorias por comportamento dos jogadores:\n"
            for i in range(4):
                comportamento = self.simulacao_dict['comportamentos_list'][i]
                self.text_str += f"\t {i + 1} {comportamento['nome']}: {round(comportamento['porcentagem'], 2)} %\n"
            self.text_str += f"Comportamento que mais vence: {self.simulacao_dict['mais_vence']}\n"

    def to_html(self):
        if self.simulacao_dict:
            self.html_str = \
                f"\n<p>Partidas terminadas por timeout: <b>{self.simulacao_dict['numero_timeouts']}</b></p>\n"
            self.html_str += f"\n<p>Media de turnos: <b>{self.simulacao_dict['media_de_turnos']}</b></p>\n"
            self.html_str += f"\n<p>Porcentagem de vitorias por comportamento dos jogadores:</p>\n"
            for i in range(4):
                comportamento = self.simulacao_dict['comportamentos_list'][i]
                self.html_str += \
                    f"\n<p>{i + 1} <b>{comportamento['nome']}</b>: {round(comportamento['porcentagem'], 2)} %</p>\n"
            self.html_str += f"\n<p>Comportamento que mais vence: <b>{self.simulacao_dict['mais_vence']}</b></p>\n"

        # if self.text_str:

        #     # self.html_str = self.text_str.replace('\n', '<p>', 1)
        #     # self.html_str = self.html_str.replace('\n', '</p>\n<p>', 7)
        #     # self.html_str = self.html_str.replace('\n', '</p>\n')
        #     self.html_str = self.text_str.replace('%', '&#37;')
        # else:
        #     self.to_text()
        #     self.to_html()


def main():
    # input_dict = {
    #     "numero_timeouts": 0,
    #     "media_de_turnos": 91,
    #     "comportamentos_list": [{
    #         "nome": "exigente",
    #         "porcentagem": 30.0
    #     }, {
    #         "nome": "impulsivo",
    #         "porcentagem": 28.99
    #     }, {
    #         "nome": "aleatorio",
    #         "porcentagem": 21.33
    #     }, {
    #         "nome": "cauteloso",
    #         "porcentagem": 20.0
    #     }],
    #     "mais_vence": "exigente"
    # }
    # request = urllib.request.urlopen('http://localhost:9000/api/monopolio')
    # input_dict = json.load(request)
    fm = FrontMonopolio()
    fm.to_text()
    print(fm.text_str)


if __name__ == "__main__":
    main()
