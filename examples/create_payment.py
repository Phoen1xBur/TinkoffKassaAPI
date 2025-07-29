from datetime import datetime

from Terminal import Terminal, Order
from config import Terminal_id, Terminal_password


terminal = Terminal(Terminal_id, Terminal_password)

amount = 1000  # 1000 копеек - 10 рублей
payment_id = f'Python#{datetime.now().isoformat()}'  # Уникальный идентификатор платежа
name = 'Тестовый платеж'  # Наименование платежа
order = Order(amount, payment_id, name)

print(f'Информация по оплате:\n{order.to_dict()}')

terminal.set_transaction(order)

print(f'Информация по оплате после инициализации платежа:\n{order.to_dict()}')
print(f'Ссылка на оплату: {order.PaymentURL}')
