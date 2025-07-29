from hashlib import sha256
import requests as r
from enum import StrEnum


# Tinkoff methods and parameters
class Tinkoff:
    URL = 'https://securepay.tinkoff.ru/v2/'
    Init = 'Init'
    GetOrderStatus = 'CheckOrder'
    GetPaymentStatus = 'GetState'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


class PaymentStatus(StrEnum):
    NEW = 'Новый платеж сформирован'
    FORM_SHOWED = 'Платежная форма открыта'


class Payment:
    Success: bool
    Amount: int
    Status: PaymentStatus
    PaymentId: str

    def update(self, json):
        for key, value in json.items():
            setattr(self, key, value)


class Order:
    """
    Класс заказа, для формирования и хранения данных о заказе

    :param int Amount: Сумма транзакции в копейках.
    :param str OrderId: Номер транзакции со стороны клиента.
    :param str Description: Описание транзакции.

    :param str PaymentId: Номер транзакции со стороны банка.
    :param str PaymentURL: URL адрес, для оплаты.
    :param boolean Success: Успешность операции.
    :param str ErrorCode: Описание ошибки, в случае success = False
    :param str Status: Статус транзакции. ["NEW", "CANCELED", "PREAUTHORIZING", "FORMSHOWED"]
    """
    Amount: int
    OrderId: str
    Description: str

    PaymentId: str = ''
    PaymentURL: str = ''
    Success: bool = False
    ErrorCode: str = ''
    Message: str = ''
    Details: str = ''
    Status: str = ''
    Payments: list[dict] = []

    def __init__(self, amount: int, order: str, description: str):
        """
        Инициализация

        :param amount: Сумма заказа в копейках.
        :param order: Номер заказа со стороны клиента.
        :param description: Описание заказа. (Обязательно для СПБ)
        """
        self.Amount = amount
        self.OrderId = order
        self.Description = description

    def to_dict(self):
        return self.__dict__

    def update(self, json):
        for key, value in json.items():
            setattr(self, key, value)

    def error_response(self, code: int):
        self.Success = False
        self.ErrorCode = 'Ошибка со стороны банка'
        self.Status = f'Код ошибки: {code}'


class Terminal:
    Terminal_id: int
    Terminal_pass: str

    orders = []  # orders[Order]

    def __init__(self, terminal_id, terminal_pass):
        self.Terminal_id = terminal_id
        self.Terminal_pass = terminal_pass

    @staticmethod
    def check_response(data: r.api) -> bool:
        pass

    def _sign(self, query: dict) -> dict:
        # Создание копии словаря, для дальнейшей работы с ним
        q = query.copy()
        # Добавляем в словарь значение с паролем
        q['Password'] = self.Terminal_pass
        token: str = ''
        # Проходимся по отсортированному словарю, для создания токена
        for key, value in sorted(q.items()):
            if type(value) != str and type(value) != int:
                continue
            token += str(value)
        # хешируем токен
        token = sha256(token.encode('utf-8')).hexdigest()
        query['Token'] = token
        return query

    def set_transaction(self, order: Order) -> None:
        url = Tinkoff.URL + Tinkoff.Init
        query = {
            'TerminalKey': self.Terminal_id,
            'Amount': order.Amount,
            'OrderId': order.OrderId,
            'Description': order.Description
        }
        data = r.post(url, json=self._sign(query), headers=Tinkoff.headers)
        if data.status_code != 200:
            order.error_response(data.status_code)
            return
        order.update(data.json())

    def get_order_status(self, order: Order) -> None:
        """
        Обновление информации по заказу То же самое что get_payment_status, получает ту же самую информацию,
        только относительно OrderId (Внутреннего уникального идентификатора)
        :param order: Информация по заказу.
        :return: Обновляется order
        """
        url = Tinkoff.URL + Tinkoff.GetOrderStatus
        query = {
            'TerminalKey': self.Terminal_id,
            'OrderId': order.OrderId,
        }

        data = r.post(url, json=self._sign(query), headers=Tinkoff.headers)
        if data.status_code != 200:
            order.error_response(data.status_code)
            return

        order.update(data.json())

    def get_payment_status(self, order: Order) -> None:
        """
        Обновление информации по заказу То же самое что get_order_status, получает ту же самую информацию,
        только относительно PaymentId (Внешнего - Банковского уникального идентификатора)
        :param order: Информация по заказу.
        :return: Обновляется order
        """
        url = Tinkoff.URL + Tinkoff.GetPaymentStatus
        query = {
            'TerminalKey': self.Terminal_id,
            'PaymentId': order.PaymentId,
        }

        data = r.post(url, json=self._sign(query), headers=Tinkoff.headers)
        if data.status_code != 200:
            order.error_response(data.status_code)
            return

        order.update(data.json())
