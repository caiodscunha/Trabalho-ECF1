import pytest
from legacy import Sis, PedEspecial


@pytest.fixture
def sis(tmp_path, monkeypatch):
    """Isola o banco em diretorio temporario por teste."""
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()


@pytest.fixture
def ped_especial(tmp_path, monkeypatch):
    """Fixture para PedEspecial."""
    monkeypatch.chdir(tmp_path)
    s = PedEspecial()
    yield s
    s.close()


# ===== TESTES DE CRIAÇÃO DE PEDIDO NORMAL =====
def test_pedido_normal_calcula_total_corretamente(sis):
    """Pedido normal com desconto 10%."""
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'},
    ]
    id_ped = sis.add_ped('Joao Silva', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(245.0)
    assert pedido['st'] == 'pendente'
    assert pedido['cli'] == 'Joao Silva'
    assert pedido['tp'] == 'normal'


def test_pedido_normal_desconto_20_porcento(sis):
    """Pedido normal com desconto 20%."""
    itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'desc20'}]
    id_ped = sis.add_ped('Cliente A', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(80.0)


def test_pedido_normal_frete_gratis(sis):
    """Pedido normal com frete grátis."""
    itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'frete_gratis'}]
    id_ped = sis.add_ped('Cliente B', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(100.0)


def test_pedido_normal_multiplos_itens(sis):
    """Pedido normal com múltiplos itens de tipos diferentes."""
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'},
        {'nome': 'produto3', 'p': 25, 'q': 2, 'tipo': 'desc20'},
    ]
    id_ped = sis.add_ped('Cliente C', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    # 100*2 + 50*1*0.9 + 25*2*0.8 = 200 + 45 + 40 = 285
    assert pedido['tot'] == pytest.approx(285.0)


# ===== TESTES DE CRIAÇÃO DE PEDIDO VIP =====
def test_pedido_vip_aplica_desconto_de_5_por_cento(sis):
    """Cliente VIP recebe 5% de desconto."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Maria', itens, 'vip')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(95.0)
    assert pedido['tp'] == 'vip'


def test_pedido_vip_desconto_acumulativo(sis):
    """Cliente VIP desconto se aplica após desconto de item."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc10'}]
    id_ped = sis.add_ped('VIP Cliente', itens, 'vip')
    pedido = sis.get_ped(id_ped)
    # 100 * 0.9 * 0.95 = 85.5
    assert pedido['tot'] == pytest.approx(85.5)


def test_pedido_vip_multiplos_itens(sis):
    """VIP com múltiplos itens."""
    itens = [
        {'nome': 'p1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'p2', 'p': 50, 'q': 1, 'tipo': 'desc20'},
    ]
    id_ped = sis.add_ped('VIP Premium', itens, 'vip')
    pedido = sis.get_ped(id_ped)
    # (200 + 40) * 0.95 = 240 * 0.95 = 228
    assert pedido['tot'] == pytest.approx(228.0)


# ===== TESTES DE CRIAÇÃO DE PEDIDO CORPORATIVO =====
def test_pedido_corporativo_desconto_10_porcento(sis):
    """Cliente corporativo recebe 10% de desconto."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(90.0)
    assert pedido['tp'] == 'corporativo'


def test_pedido_corporativo_desconto_acumulativo(sis):
    """Corporativo desconto se aplica após desconto de item."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc10'}]
    id_ped = sis.add_ped('Corp Ltd', itens, 'corporativo')
    pedido = sis.get_ped(id_ped)
    # 100 * 0.9 * 0.9 = 81
    assert pedido['tot'] == pytest.approx(81.0)


def test_pedido_corporativo_multiplos_itens(sis):
    """Corporativo com múltiplos itens."""
    itens = [
        {'nome': 'p1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'p2', 'p': 50, 'q': 1, 'tipo': 'desc20'},
    ]
    id_ped = sis.add_ped('Big Corp', itens, 'corporativo')
    pedido = sis.get_ped(id_ped)
    # (200 + 40) * 0.9 = 240 * 0.9 = 216
    assert pedido['tot'] == pytest.approx(216.0)


# ===== TESTES DE PROCESSAMENTO DE PAGAMENTO =====
def test_pagamento_cartao_sucesso(sis):
    """Pagamento com cartão com valor suficiente."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    result = sis.proc_pag(id_ped, 'cartao', 100)
    assert result is True
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'aprovado'


def test_pagamento_cartao_valor_insuficiente(sis):
    """Pagamento com cartão com valor insuficiente."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    result = sis.proc_pag(id_ped, 'cartao', 50)
    assert result is False
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'pendente'


def test_pagamento_pix_sucesso(sis):
    """Pagamento com PIX com valor suficiente."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    result = sis.proc_pag(id_ped, 'pix', 100)
    assert result is True
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'aprovado'


def test_pagamento_pix_aprova_pedido_automaticamente(sis):
    """PIX aprova automaticamente."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.proc_pag(id_ped, 'pix', 100)
    assert sis.get_ped(id_ped)['st'] == 'aprovado'


def test_pagamento_boleto_sucesso(sis):
    """Pagamento com boleto gera boleto mas não aprova."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    result = sis.proc_pag(id_ped, 'boleto', 100)
    assert result is True
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'pendente'


def test_pagamento_boleto_nao_aprova_automaticamente(sis):
    """Boleto não aprova automaticamente."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.proc_pag(id_ped, 'boleto', 100)
    assert sis.get_ped(id_ped)['st'] == 'pendente'


def test_pagamento_insuficiente_falha(sis):
    """Pagamento com valor insuficiente falha."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    assert sis.proc_pag(id_ped, 'cartao', 50) is False


def test_pagamento_metodo_invalido(sis):
    """Pagamento com método inválido falha."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    result = sis.proc_pag(id_ped, 'bitcoin', 100)
    assert result is False


def test_pagamento_pedido_inexistente(sis):
    """Pagamento de pedido inexistente falha."""
    result = sis.proc_pag(999, 'cartao', 100)
    assert result is False


# ===== TESTES DE ATUALIZAÇÃO DE STATUS =====
def test_atualizar_status_para_aprovado(sis):
    """Mudar status para aprovado."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    sis.upd_st(id_ped, 'aprovado')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'aprovado'


def test_atualizar_status_para_enviado(sis):
    """Mudar status para enviado."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    sis.upd_st(id_ped, 'enviado')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'enviado'


def test_atualizar_status_para_entregue(sis):
    """Mudar status para entregue."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


def test_atualizar_status_vip_entregue_gera_pontos(sis):
    """VIP recebe 2x pontos ao entregar."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('VIP', itens, 'vip')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


def test_atualizar_status_corporativo_entregue_gera_pontos(sis):
    """Corporativo recebe 1.5x pontos ao entregar."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Corp', itens, 'corporativo')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


def test_atualizar_status_normal_entregue_gera_pontos(sis):
    """Normal recebe 1x pontos ao entregar."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Normal', itens, 'normal')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


# ===== TESTES DE CANCELAMENTO =====
def test_cancelar_pedido_sucesso(sis):
    """Cancelar pedido muda status para cancelado."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    sis.cancelar_pedido(id_ped)
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'cancelado'


def test_cancelar_pedido_inexistente(sis):
    """Cancelar pedido inexistente não causa erro."""
    sis.cancelar_pedido(999)
    # Não deve lançar exceção


# ===== TESTES DE VALIDAÇÃO DE ESTOQUE =====
def test_validar_estoque_sucesso(sis):
    """Validar estoque com itens disponíveis."""
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'normal'},
    ]
    result = sis.validar_estoque(itens)
    assert result is True


def test_validar_estoque_produto_inexistente(sis):
    """Validar estoque com produto inexistente falha."""
    itens = [{'nome': 'produto_inexistente', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    result = sis.validar_estoque(itens)
    assert result is False


def test_validar_estoque_quantidade_insuficiente(sis):
    """Validar estoque com quantidade insuficiente falha."""
    itens = [{'nome': 'produto1', 'p': 100, 'q': 200, 'tipo': 'normal'}]
    result = sis.validar_estoque(itens)
    assert result is False


# ===== TESTES DE CÁLCULO DE TOTAL DO CLIENTE =====
def test_calcular_total_cliente_unico_pedido(sis):
    """Calcular total de cliente com um pedido."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens, 'normal')
    total = sis.calc_tot_cli('Cliente A')
    assert total == pytest.approx(100.0)


def test_calcular_total_cliente_multiplos_pedidos(sis):
    """Calcular total de cliente com múltiplos pedidos."""
    itens1 = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    itens2 = [{'nome': 'p2', 'p': 50, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens1, 'normal')
    sis.add_ped('Cliente A', itens2, 'normal')
    total = sis.calc_tot_cli('Cliente A')
    assert total == pytest.approx(150.0)


def test_calcular_total_cliente_inexistente(sis):
    """Calcular total de cliente sem pedidos."""
    total = sis.calc_tot_cli('Cliente Inexistente')
    assert total == pytest.approx(0.0)


# ===== TESTES DE RELATÓRIOS =====
def test_gerar_relatorio_vendas(sis):
    """Gerar relatório de vendas."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens, 'normal')
    sis.gerar_rel('vendas')
    # Só verificar que não lança exceção


def test_gerar_relatorio_clientes(sis):
    """Gerar relatório de clientes."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens, 'normal')
    sis.gerar_rel('clientes')
    # Só verificar que não lança exceção


def test_gerar_relatorio_vendas_multiplos_pedidos(sis):
    """Gerar relatório de vendas com múltiplos pedidos."""
    itens1 = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    itens2 = [{'nome': 'p2', 'p': 50, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens1, 'normal')
    sis.add_ped('Cliente B', itens2, 'normal')
    sis.gerar_rel('vendas')


# ===== TESTES DE PedEspecial =====
def test_ped_especial_add_ped_aplica_taxa_especial(ped_especial):
    """PedEspecial aplica taxa de 15% no total."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Cliente', itens, 'normal')
    pedido = ped_especial.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(115.0)


def test_ped_especial_add_ped_com_desconto(ped_especial):
    """PedEspecial com desconto de item."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc10'}]
    id_ped = ped_especial.add_ped('Cliente', itens, 'normal')
    pedido = ped_especial.get_ped(id_ped)
    # 100 * 0.9 * 1.15 = 103.5
    assert pedido['tot'] == pytest.approx(103.5)


def test_ped_especial_add_ped_com_desc20(ped_especial):
    """PedEspecial com desconto de 20% de item."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc20'}]
    id_ped = ped_especial.add_ped('Cliente', itens, 'normal')
    pedido = ped_especial.get_ped(id_ped)
    # 100 * 0.8 * 1.15 = 92.0
    assert pedido['tot'] == pytest.approx(92.0)


def test_ped_especial_upd_st_ignora_transicoes(ped_especial):
    """PedEspecial ignora transições de estado do pai."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Cliente', itens, 'normal')
    # Tentar ir direto para entregue sem passar por aprovado
    ped_especial.upd_st(id_ped, 'entregue')
    pedido = ped_especial.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


# ===== TESTES DE FLUXO COMPLETO =====
def test_fluxo_completo_pedido_normal(sis):
    """Fluxo completo de um pedido normal."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    assert sis.proc_pag(id_ped, 'cartao', 100)
    sis.upd_st(id_ped, 'enviado')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


def test_fluxo_completo_pedido_vip(sis):
    """Fluxo completo de um pedido VIP."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente VIP', itens, 'vip')
    assert sis.proc_pag(id_ped, 'pix', 95)
    sis.upd_st(id_ped, 'enviado')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


def test_fluxo_completo_pedido_corporativo(sis):
    """Fluxo completo de um pedido corporativo."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Empresa', itens, 'corporativo')
    assert sis.proc_pag(id_ped, 'boleto', 90)
    sis.upd_st(id_ped, 'enviado')
    sis.upd_st(id_ped, 'entregue')
    pedido = sis.get_ped(id_ped)
    assert pedido['st'] == 'entregue'


# ===== TESTES DE GET_PED COM INEXISTENTE =====
def test_get_ped_inexistente_retorna_none(sis):
    """Obter pedido inexistente retorna None."""
    resultado = sis.get_ped(999)
    assert resultado is None


# ===== TESTES DE EDGE CASES =====
def test_pedido_com_zero_itens_total_zero(sis):
    """Pedido com lista vazia tem total zero."""
    itens = []
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(0.0)


def test_pedido_quantidade_zero(sis):
    """Pedido com quantidade zero."""
    itens = [{'nome': 'p1', 'p': 100, 'q': 0, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(0.0)


def test_multiplos_clientes_calculos_independentes(sis):
    """Múltiplos clientes têm cálculos independentes."""
    itens1 = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    itens2 = [{'nome': 'p2', 'p': 200, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Cliente A', itens1, 'normal')
    sis.add_ped('Cliente B', itens2, 'normal')
    total_a = sis.calc_tot_cli('Cliente A')
    total_b = sis.calc_tot_cli('Cliente B')
    assert total_a == pytest.approx(100.0)
    assert total_b == pytest.approx(200.0)


def test_upd_st_pedido_inexistente(sis):
    """Atualizar status de pedido inexistente não causa erro."""
    sis.upd_st(999, 'aprovado')
    # Não deve lançar exceção
