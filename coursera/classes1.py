solar_system = []

planet_names = [
    'Mercury', 'Venus', 'Earth', 'Mars',
    'Jupiter', 'Saturn', 'Uranus', 'Neptune'
]


class Planet:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Planet {self.name}'


for name in planet_names:
    planet = Planet(name)
    solar_system.append(planet)

print(solar_system)

mars = Planet('Mars')
print(mars.name)
mars.name = 'Venus'
print(mars.name)
