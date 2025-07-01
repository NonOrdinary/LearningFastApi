class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def birthday(self):
        self.age += 1

    def __repr__(self):
        # Called by print() and the interactive prompt
        return f"Person(name={self.name!r}, age={self.age})"

s = Person("sunny",22)
print(s)