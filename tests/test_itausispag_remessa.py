import os
import unittest
from decimal import Decimal
from cnab240.bancos import itauSispag
from cnab240.tipos import Arquivo, Lote

TESTS_DIRPATH = os.path.abspath(os.path.dirname(__file__))
ARQS_DIRPATH = os.path.join(TESTS_DIRPATH, 'arquivos')


class TestCnab240ItauSisPagRemessa(unittest.TestCase):

    def setUp(self):
        self.banco = itauSispag
        self.data_header = {
            'numero_inscricao': 15594050000111,
            'numero_agencia': 00001,
            'numero_conta': 17600,
            'agencia_conta_dv': 6,
            'nome_empresa': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCD',
            'nome_banco': 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCD',
            'arquivo_codigo': 1,
            'arquivo_data_de_geracao': 01012017,
            'arquivo_hora_de_geracao': 222222
        }

        self.data_lote_header = {
            'numero_inscricao': self.data_header['numero_inscricao'],
            'numero_agencia': self.data_header['numero_agencia'],
            'numero_conta': self.data_header['numero_conta'],
            'agencia_conta_dv': self.data_header['agencia_conta_dv'],
            'nome_empresa': self.data_header['nome_empresa'],
        }

        self.data_lote_trailer = {'total_valor_pagtos': Decimal('0.00')}

        self.data_pgto1 = {
            'servico_numero_registro': 1,
            'servico_codigo_movimento': 001,
            'banco_favorecido': 341,
            'numero_agencia_conta': '0073',
            'nome_favorecido': 'Paulo Romano',
            'seu_numero': '001',
            'data_pagto': 01012017,
            'valor_pagto': Decimal('100.55'),
        }

        self.arquivo = Arquivo(self.banco, **self.data_header)

    def test_atualizacao_total_valor_pagtos(self):
        self.lote_header = self.banco.registros.HeaderLotePagamento(**self.data_lote_header)
        self.lote_trailer = self.banco.registros.TrailerLotePagamento(**self.data_lote_trailer)

        self.lote1 = Lote(self.banco, header=self.lote_header, trailer=self.lote_trailer)

        self.arquivo.adicionar_lote(self.lote1)

        self.arquivo.incluir_pagamento(**self.data_pgto1)
        self.arquivo.incluir_pagamento(**self.data_pgto1)

        self.assertEqual(self.lote1.trailer.total_valor_pagtos, Decimal('201.10'))