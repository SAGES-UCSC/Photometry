class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def getNames(self):
        return self.name

    def getSpecies(self):
        return self.species

    def __str__(self):
        return "%s is a %s" % (self.name, self.species)

class Dog(Pet):
    def __init__(self, name, chases_cats):
        Pet.__init__(self, name, "Dog")
        self.chases_cats = chases_cats

    def chasesCats(self):
        return self.chases_cats

class Cat(Pet):
    def __init__(self, name, hates_dogs):
        Pet.__init__(self, name, "Cat")
        self.hate_dogs = hates_dogs

    def hatesDogs(self):
        return self.hates_dogs


mister_pet = Pet("Mister", "Dog")
mister_dog = Dog("Mister", True)

fido = Dog("Fido", True)
rover = Dog("Rover", False)
mittens = Cat("Mittens", True)
fluffy = Cat("Fluffy", False)

print fido
print rover
