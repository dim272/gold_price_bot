class Human:

    def __init__(self, name, age=0):
        self.name = name
        self.age = age

    # @staticmethod - встроенный декоратор класса
    # Он нам может понадобиться, чтобы работать с переменными в классе
    @staticmethod
    def is_age_valid(age):
        return 18 < age < 50


bob = Human("Bob", age=35)

print(bob.is_age_valid(bob.age))
print(bob.is_age_valid(55))
print(Human.is_age_valid(45))