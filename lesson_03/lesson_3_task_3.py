from address import address
from mailing import mailing

mailing = mailing(
    to_address=address("123456", "Москва", "Ленина", "10", "25"),
    from_address=address("654321", "Сочи", "Пушкина", "5", "13"),
    cost=250,
    track="TRACK123456"
)

to_addr = mailing.to_address
from_addr = mailing.from_address

print(f"Отправление {mailing.track} из {from_addr.index}, {from_addr.city}, "
      f"{from_addr.street}, {from_addr.house} - {from_addr.apartment} в "
      f"{to_addr.index}, {to_addr.city}, {to_addr.street}, {to_addr.house} - "
      f"{to_addr.apartment}. Стоимость {mailing.cost} рублей.")
