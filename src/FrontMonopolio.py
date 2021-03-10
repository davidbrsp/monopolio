import urllib.request


class FrontMonopolio:

    def __init__(self, kwarg_dict):
        self.simulacao_dict = kwarg_dict
        self.text_str = ""
        self.html_str = ""
        self.to_html()

    def to_text(self):
        str_url = 'http://localhost:8000/api/monopolio'
        # try:
        url = urllib.request.urlopen(str_url)
        # except as ex:
        #     print(ex)
        # with urllib.request.urlopen(str_url) as url:
        #     ffm.simulacao_dict = json.loads(url.read().decode())
        #     # print(data)
        ffm.simulacao_dict = json.loads(url.read())
        ffm.to_text()

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
        if self.text_str:
            # self.html_str = self.text_str.replace('\n', '<p>', 1)
            # self.html_str = self.html_str.replace('\n', '</p>\n<p>', 7)
            # self.html_str = self.html_str.replace('\n', '</p>\n')
            self.html_str = self.text_str.replace('%', '&#37;')
        else:
            self.to_text()
            self.to_html()

def main():
    input_dict = {
            "numero_timeouts": 0,
            "media_de_turnos": 91,
            "comportamentos_list": [{
                    "nome": "exigente",
                    "porcentagem": 30.0
                }, {
                    "nome": "impulsivo",
                    "porcentagem": 28.99
                }, {
                    "nome": "aleatorio",
                    "porcentagem": 21.33
                }, {
                    "nome": "cauteloso",
                    "porcentagem": 20.0
                }],
            "mais_vence": "exigente"
        }
    fm = FrontMonopolio(input_dict)
    print(fm.text_str)

if __name__ == "__main__":
    main()
