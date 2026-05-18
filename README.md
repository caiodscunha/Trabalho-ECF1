# Loja Verde - Refatoração Guiada por SOLID, Clean Code e Padrões GoF

## Descrição

Este projeto é a refatoração de um sistema legado de e-commerce seguindo os cinco princípios SOLID, práticas de Clean Code, e aplicação de pelo menos quatro padrões de design do Gang of Four (GoF).

## Sprint 0: Estabelecer Rede de Segurança ✓

### Entregas Realizadas

- ✅ **Suíte de Testes Golden Master**: 47 testes cobrindo todos os fluxos obrigatórios
  - Criação de pedido normal, VIP e corporativo
  - Processamento de pagamento (cartão, PIX, boleto)
  - Atualização de status
  - Cancelamento e geração de relatórios

- ✅ **Cobertura de Testes**: 88% (exceeds 80% requirement)
  - Coverage report gerado por `pytest-cov`
  - Linhas não cobertas são funções auxiliares de teste

- ✅ **Análise Textual SOLID**: Identificadas violações em cada princípio
  - **SRP**: Múltiplas responsabilidades em uma classe
  - **OCP**: Novos métodos de pagamento/desconto requerem modificação
  - **LSP**: PedEspecial viola contrato do pai
  - **ISP**: Interface monolítica Sis
  - **DIP**: Dependência em SQLite e print() concretos

### Estrutura do Projeto

```
Trabalho-ECF1/
├── src/
│   └── legacy.py              # Código legado funcional
├── tests/
│   └── golden_master/
│       └── test_legacy_behavior.py    # 47 testes de caracterização
├── docs/
│   └── analise_sprint0.md     # Análise textual SOLID (2 pág)
├── .gitignore
├── pyproject.toml
├── Makefile
└── README.md
```

## Como Executar

### Pré-requisitos

- Python 3.13+
- pip

### Instalação

```bash
# Instalar dependências de desenvolvimento
py -3.13 -m pip install pytest pytest-cov

# Ou usar o Makefile (requer make/mingw)
make install
```

### Executar Testes

```bash
# Todos os testes com cobertura
py -3.13 -m pytest tests/ -v --cov=src --cov-report=term-missing

# Apenas testes Golden Master
py -3.13 -m pytest tests/golden_master/ -v

# Com HTML report
py -3.13 -m pytest tests/ --cov=src --cov-report=html
```

### Usar Makefile

```bash
make test       # Executar testes
make cov        # Cobertura com HTML
make lint       # Lint com ruff
make type       # Type checking com mypy
make complexity # Análise de complexidade
make all        # Todos os checks acima
make clean      # Limpar arquivos gerados
```

## Violações SOLID Identificadas

### Single Responsibility Principle (SRP)

**Problema**: Classe `Sis` com 5+ responsabilidades diferentes
- Cálculo de totais com regras de negócio
- Persistência em banco de dados SQLite
- Notificação de clientes
- Processamento de pagamentos
- Geração de relatórios

**Impacto**: Mudanças simples afetam múltiplas partes. Impossível testar sem banco de dados.

---

### Open/Closed Principle (OCP)

**Problema**: Novos métodos de pagamento/descontos requerem modificação de código existente

```python
def proc_pag(self, id, m, vl):
    if m == 'cartao': ...
    elif m == 'pix': ...
    elif m == 'boleto': ...
    else: return False  # Requer if/elif aqui para novo método!
```

**Impacto**: Não é possível adicionar "Pagamento em criptomoeda" sem editar `Sis`.

---

### Liskov Substitution Principle (LSP)

**Problema**: `PedEspecial` viola contrato do pai `Sis`
- `add_ped` não aplica desconto de tipo de cliente
- `upd_st` ignora transições de estado

**Impacto**: Código polimórfico quebra. `PedEspecial` não pode substituir `Sis` de forma segura.

---

### Interface Segregation Principle (ISP)

**Problema**: Interface monolítica `Sis` força clientes a depender de tudo

Clientes que querem apenas calcular total precisam:
- SQLite connection
- Cursor database
- Todos os métodos de notificação
- Geração de relatórios

**Impacto**: Testes dependem de banco de dados real. Mock de toda classe necessário.

---

### Dependency Inversion Principle (DIP)

**Problema**: Dependências em implementações concretas

```python
def __init__(self):
    self.db = sqlite3.connect('loja.db')  # Dependência em sqlite3!

def add_ped(self, n, its, t):
    if t == 'normal':
        print(...)  # Dependência em print()!
```

**Impacto**: Trocar SQLite por PostgreSQL = reescrita total. Impossível usar notificação real.

---

## Próximas Etapas (Sprint 1 e 2)

- [ ] Sprint 1: Refatoração em camadas (Models, Repositories, Services)
- [ ] Sprint 1: Padrão Repository para persistência
- [ ] Sprint 2: Padrão Strategy para pagamentos e descontos
- [ ] Sprint 2: Padrão Observer para notificações
- [ ] Sprint 2: Padrão Factory para criação de pedidos
- [ ] Extensões: Criptomoeda, WhatsApp, Desconto por volume

## Referências

- Martin, R. C. *Clean Code*. Prentice Hall, 2008.
- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Gamma, E. et al. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994.
- Fowler, M. *Refactoring: Improving the Design of Existing Code*. 2ª ed. Addison-Wesley, 2018.

---

**Status**: Sprint 0 - Concluído ✓
**Data**: Maio de 2026