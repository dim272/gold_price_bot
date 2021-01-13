class Event:

    def __init__(self, description, date):
        self.description = description
        self.even_date = date

    def __str__(self):
        return f"Событие: \"{self.description}\" Когда: {self.even_date}"

    # @classmethod - встроенный декоратор класса.
    # Он принимает:
    # what, when - данные пользователя
    # cls - название класса - Event
    # создаёт экземпляр класса с этими данными
    @classmethod
    def from_string(cls, what, when):
        description = what
        date = when
        return cls(description, date)


event = Event.from_string("Начало нового сериала", "1 декабря 2020 года")

print(event)
print(event.from_string("Начало нового сериала", "1 декабря 2021 года"))
print(Event.from_string("Начало нового сериала", "10 декабря 2021 года"))
