from datetime import datetime

from Terminal import Terminal, Order
from config import Terminal_id, Terminal_password


terminal = Terminal(Terminal_id, Terminal_password)

payment_id = f'Python#2025-07-29T14:24:18.893292'  # Уникальный идентификатор платежа
order = Order(0, payment_id, '')

terminal.get_order_status(order)

print(f'Информация по оплате:\n{order.to_dict()}')

while len(order.Payments) > 0:
    payment = order.Payments.pop(0)
    print(payment['Status'])
    print('Расшифровка статуса:')
    # https://www.tbank.ru/kassa/dev/payments/#tag/Scenarii-oplaty-po-karte/Statusnaya-model-platezha
    match payment['Status']:
        case 'NEW':
            print('Новый заказ. С ним никаких действий еще не происходило')
        case 'FORM_SHOWED':
            print('Мерчант перенаправил клиента на страницу платежной формы PaymentURL и страница загрузилась у клиента в браузере')
        case 'AUTHORIZING':
            print('Платеж обрабатывается MAPI и платежной системой.')
        case '3DS_CHECKING':
            print('Платеж проходит проверку 3D-Secure.')
        case '3DS_CHECKED':
            print('Платеж успешно прошел проверку 3D-Secure.')
        case 'AUTHORIZED':
            print('Платеж авторизован, деньги заблокированы на карте клиента.')
        case 'PAY_CHECKING':
            print('Платеж обрабатывается.')
        case 'CONFIRMING':
            print('Подтверждение платежа обрабатывается MAPI и платежной системой.')
        case 'CONFIRMED':
            print('Платеж подтвержден, деньги списаны с карты клиента.')
        case 'REVERSING':
            print('Мерчант запросил отмену авторизованного, но еще неподтвержденного платежа. Возврат обрабатывается MAPI и платежной системой.')
        case 'PARTIAL_REVERSED':
            print('Частичный возврат по авторизованному платежу завершился успешно.')
        case 'REVERSED':
            print('Полный возврат по авторизованному платежу завершился успешно.')
        case 'REFUNDING':
            print('Мерчант запросил отмену подтвержденного платежа. Возврат обрабатывается MAPI и платежной системой.')
        case 'PARTIAL_REFUNDED':
            print('Частичный возврат по подтвержденному платежу завершился успешно.')
        case 'REFUNDED':
            print('Полный возврат по подтвержденному платежу завершился успешно.')
        case 'CANCELED':
            print('Мерчант отменил платеж.')
        case 'DEADLINE_EXPIRED':
            print('1. Клиент не завершил платеж в срок жизни ссылки на платежную форму PaymentURL. Этот срок мерчант передает в методе Init в параметре RedirectDueDate.\n2. Платеж не прошел проверку 3D-Secure в срок.')
        case 'REJECTED':
            print('Банк отклонил платеж.')
        case 'AUTH_FAIL':
            print('Платеж завершился ошибкой или не прошел проверку 3D-Secure.')
        case _:
            print('Необработанный статус')

