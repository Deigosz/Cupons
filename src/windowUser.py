import streamlit as st
from utils import Utils
from main import Automacao


class CupomGenerator:
    def get_inputs(self):
        self.dforigem = Utils()
        self.dforigem = self.dforigem.get_origem()
        self.dfdestino = Utils()
        self.dfdestino = self.dfdestino.get_destino()
        self.dfconvenio = Utils()
        self.dfconvenio = self.dfconvenio.get_convenio()

        self.username = st.text_input("Usuário")
        self.password = st.text_input("Senha", type="password")

        self.convenio_url_map = dict(zip(self.dfconvenio['Nome'], self.dfconvenio['URL']))
        self.convenio = st.selectbox("Selecione o Convenio:", [''] + list(self.dfconvenio['Nome']))
        self.urlconveio = self.convenio_url_map.get(self.convenio, None)


        self.origem = st.selectbox('Selecione a Origem:', [''] + list(self.dforigem['Origem']))
        self.destino = st.selectbox('Selecione o Destino:', [''] + list(self.dfdestino['Destino']))
        self.desconto = st.radio("Tipo do Cupom", ("Desconto em Valor", "Desconto em Porcentagem"))
        self.quantidade = st.number_input("Quantidade", min_value=1, value=1, max_value=50)
        self.percent = st.number_input('Digite a Valor/Porcentagem', min_value=1, value=1, max_value=100)


    def generate_cupom(self):
        if self.username and self.password and self.quantidade and self.desconto and self.percent:
            cupom_info = {
                'user': self.username,
                'pass': self.password,
                'qtd': self.quantidade,
                'type': self.desconto,
                'value': self.percent,
                'ori': self.origem,
                'dest': self.destino,
                'convenio':self.urlconveio
            }
            Automacao(cupom_info)
            st.success("Cupom gerado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

    def render(self):
        st.markdown("<h1 style='text-align: center;'>Bot de Cupom</h1>", unsafe_allow_html=True)
        with st.form(key='form'):
            self.get_inputs()
            if st.form_submit_button('Gerar'):
                self.generate_cupom()

if __name__ == '__main__':
    generator = CupomGenerator()
    generator.render()
