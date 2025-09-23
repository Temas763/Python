from smartphone import Smartphone

catalog = []

catalog.append(Smartphone("Samsung", "Galaxy S23", "+79123456789"))
catalog.append(Smartphone("Apple", "iPhone 15", "+79234567890"))
catalog.append(Smartphone("Xiaomi", "Redmi Note 12", "+79345678901"))
catalog.append(Smartphone("Google", "Pixel 8", "+79456789012"))
catalog.append(Smartphone("OnePlus", "11 Pro", "+79567890123"))

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
