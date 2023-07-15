from peewee import SqliteDatabase, Model, CharField, IntegerField

db = SqliteDatabase('ruta.db')

class Persona(Model):
    nombre = CharField()
    edad = IntegerField()

    class Meta:
        database = db

# crear la tabla si no existe
db.create_tables([Persona])
my_table = Persona.create(nombre = "la vie",edad = 20)
my_table.save()
# definir la función que representa la condición de filtrado
def mayores_de_edad(persona):
    return persona.edad > 18

# realizar la consulta usando la función de filtrado
personas_mayores = Persona.select().where(mayores_de_edad == True)

# iterar sobre los resultados
for persona in personas_mayores:
    print(persona.nombre, persona.edad)