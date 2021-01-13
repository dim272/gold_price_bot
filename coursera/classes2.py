class Planet:  # Planet - это класс
    """This class for planets"""

    # count - это атрибут класса, который мы задали самостоятельно
    count = 0

    def __init__(self, name, population=None):  # __init__ - один из магических методов класса
        self.name = name
        self.population = population or []
        Planet.count += 1


earth = Planet('Earth')  # earth - это экземпляр класса Planet
earth.mass = 1000  # mass - это атрибут экземпляра earth, которого нет у всего класса Planet
mars = Planet('Mars')  # mars - это ещё один экземпляр класса Planet, у которого есть все атрибуты класса,
# но нет атрибута mass

print(Planet.count)  # выдаст атрибут count класса Planet
print(earth.count)  # ищет атрибут count экзмепляра earth, если не находит, то выдаёт атрибут count класса Planet
print(Planet.__dict__)  # выдаст словарь класса
print(earth.__dict__)  # выдаст словарь экземпляра
print(Planet.__doc__)  # выдаст докстринг класса - данные указанные в тройных кавычках
print(earth.__class__)  # даст понять к какому классу принадлежит экземпляр earth
