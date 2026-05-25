# Loja Verde — Refatoração Guiada por SOLID, Clean Code e Padrões GoF

**Disciplina:** Padrões e Arquitetura de Software — PUC-Campinas — 1º Semestre 2026

**Professor:** Prof. Dr. Douglas H. S. Abreu

---

## Descrição

Refatoração de um sistema legado de e-commerce (Loja Verde) aplicando os cinco princípios SOLID, práticas de Clean Code e cinco padrões GoF: Strategy, Repository, Observer, Factory Method e Decorator.

O sistema legado consistia em uma única classe Sis com acumulando conexão SQLite, cálculo de preços, persistência, notificações, pagamentos e relatórios, além de uma subclasse PedEspecial que violava o LSP. Após a refatoração, o sistema mantém compatibilidade total com a API legada via facade, com 63 testes passando e 95% de cobertura.

---

## Métricas

| Métrica | Ferramenta | Critério | Resultado |
|---|---|---|---|
| Testes passando | pytest | 100% | 63/63 |
| Cobertura | coverage.py | >= 85% | 95% |
| Lint / PEP 8 | ruff | 0 erros | 0 erros |
| Tipagem estática | mypy --strict | 0 erros | 0 erros em 31 arquivos |
| Complexidade média | radon cc | média A ou B | A (1.55) |

---

## Estrutura do Projeto

```
Trabalho-ECF1/
├── legacy.py                        # Redirect para src/facades/legacy.py (API legada)
├── src/
│   ├── facades/
│   │   └── legacy.py                # Sis e PedEspecial refatoradas (Facade)
│   ├── factories/
│   │   └── order_factory.py         # StandardOrderFactory, SpecialOrderFactory
│   ├── interfaces/                  # 8 ABCs: IOrderRepository, IPaymentStrategy, etc.
│   ├── models/
│   │   └── order.py                 # Dataclass Order
│   ├── observers/
│   │   ├── notification_observer.py # Email, SMS, AccountManager, Points observers
│   │   └── whatsapp_observer.py     # Extensão: WhatsApp observer
│   ├── repositories/
│   │   └── sqlite_order_repository.py
│   ├── services/
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── notification_service.py
│   │   ├── inventory_service.py
│   │   └── report_service.py
│   ├── strategies/
│   │   ├── payment_strategy.py      # Cartao, Pix, Boleto
│   │   ├── discount_strategy.py     # DefaultItemPriceCalculator, descontos por cliente
│   │   ├── crypto_payment_strategy.py  # Extensão: Crypto (taxa 2%)
│   │   └── volume_discount_strategy.py # Extensão: Decorator de desconto por volume
│   └── main.py                      # Ponto de entrada (py -3.13 -m src.main)
├── tests/
│   ├── golden_master/
│   │   └── test_legacy_behavior.py  # 48 testes de caracterização
│   └── unit/
│       ├── test_crypto_payment.py
│       ├── test_volume_discount.py
│       └── test_whatsapp_notification.py
├── docs/
│   ├── analise.docx                 # Documento de análise completo (seções 1-9)
│   ├── analise_sprint0.docx         # Análise Sprint 0
│   ├── diagrama.puml                # Diagrama UML completo (PlantUML)
│   ├── diagramas/                   # Diagramas parciais por padrão GoF (.puml)
│   ├── imagens/                     # PNGs gerados dos diagramas GoF
│   └── gerar_analise.py             # Script que gera o analise.docx
├── pyproject.toml
├── Makefile
└── README.md
```

---

## Padrões GoF Aplicados

| Padrão | Onde |
|---|---|
| **Strategy** | `IPaymentStrategy` + CartaoStrategy, PixStrategy, BoletoStrategy, CryptoPaymentStrategy; `IItemPriceCalculator` + DefaultItemPriceCalculator; `IClientDiscountStrategy` + VipClientDiscount, CorporativoClientDiscount |
| **Repository** | `IOrderRepository` + SqliteOrderRepository |
| **Observer** | `IOrderEventObserver` + Email, SMS, AccountManager, Points, WhatsApp observers; NotificationService como publisher |
| **Factory Method** | `IOrderFactory` + StandardOrderFactory, SpecialOrderFactory |
| **Decorator** | VolumeDiscountCalculator envolve qualquer IItemPriceCalculator |

---

## Extensões Obrigatórias

Todas implementadas sem modificar nenhuma classe existente:

- **Criptomoeda** — `src/strategies/crypto_payment_strategy.py` (taxa de 2%)
- **WhatsApp** — `src/observers/whatsapp_observer.py` (todos os tipos de cliente)
- **Desconto por volume** — `src/strategies/volume_discount_strategy.py` (15% off para 3+ unidades, padrão Decorator)

---

## Como Executar

```bash
# Pré-requisito: Python 3.13

# Instalar dependências
py -3.13 -m pip install pytest pytest-cov ruff mypy radon python-docx plantuml

# Executar o sistema
py -3.13 -m src.main

# Testes
py -3.13 -m pytest --tb=no -q

# Testes com cobertura
py -3.13 -m pytest --cov=src --cov-report=term-missing

# Lint
py -3.13 -m ruff check src/

# Tipagem
py -3.13 -m mypy --strict --explicit-package-bases src/

# Complexidade
py -3.13 -m radon cc src/ -a -s

# Ou tudo via Makefile
make all
```

```bash
# Gerar imagens dos diagramas GoF
py -3.13 docs/diagramas/gerar_imagens.py

# Gerar documento de análise Word
py -3.13 docs/gerar_analise.py
```

---

## Referências

- Martin, R. C. *Clean Code*. Prentice Hall, 2008.
- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Gamma, E. et al. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994.
- Fowler, M. *Refactoring: Improving the Design of Existing Code*. 2ª ed. Addison-Wesley, 2018.

---

**Status:** Sprint 2 — Concluído
**Data:** Maio de 2026
