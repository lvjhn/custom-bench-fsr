from faker import Faker 

Faker.seed(0)
fake = Faker()

COLORS = [
    "red", 
    "orange", 
    "yellow", 
    "green", 
    "blue", 
    "indigo", 
    "violet"
]

def random_rainbow_color(): 
    return fake.random_element(elements=COLORS)


