"""Testes da extensao: canal de notificacao WhatsApp para todos os clientes.

OCP verificado: apenas src/observers/whatsapp_observer.py foi adicionado.
Nenhuma classe existente (NotificationService, observers de email/SMS) foi
modificada para habilitar o canal WhatsApp.
"""
import pytest

from src.observers.whatsapp_observer import WhatsAppOrderObserver
from src.services.notification_service import NotificationService


@pytest.fixture
def notification_service_with_whatsapp():
    notifications = NotificationService()
    notifications.subscribe(WhatsAppOrderObserver("5511999999999"))
    return notifications


def test_whatsapp_notifica_pedido_recebido_cliente_normal(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_received("Joao", "normal")
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Joao: Pedido recebido!" in captured.out


def test_whatsapp_notifica_pedido_recebido_cliente_vip(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_received("Maria", "vip")
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Maria: Pedido recebido!" in captured.out


def test_whatsapp_notifica_pedido_recebido_cliente_corporativo(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_received("Empresa", "corporativo")
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Empresa: Pedido recebido!" in captured.out


def test_whatsapp_notifica_pedido_aprovado(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_approved("Joao", "normal")
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Joao: Pedido aprovado!" in captured.out


def test_whatsapp_notifica_pedido_enviado(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_sent("Joao")
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Joao: Pedido enviado!" in captured.out


def test_whatsapp_notifica_pedido_entregue(
    notification_service_with_whatsapp, capsys
):
    notification_service_with_whatsapp.notify_order_delivered("Joao", "normal", 100.0)
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Joao: Pedido entregue!" in captured.out
