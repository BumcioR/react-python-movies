from peewee import *

db = SqliteDatabase('movies.db')

class BaseModel(Model):
    class Meta:
        database = db

class Actor(BaseModel):
    name = CharField()
    surname = CharField()

    def save(self, *args, **kwargs):

        if not self.name or not self.surname:
            raise ValueError("Name and surname cannot be empty")
        return super().save(*args, **kwargs)

class Movie(BaseModel):
    title = CharField()
    director = CharField()
    year = IntegerField()
    description = TextField()
    actors = ManyToManyField(Actor, backref='movies')

    def add_actor(self, actor: Actor):
        """Metoda dodająca aktora do filmu"""
        self.actors.add(actor)
        self.save()

ActorMovie = Movie.actors.get_through_model()

if __name__ == "__main__":
    db.connect()
    db.create_tables([Actor, Movie, ActorMovie])
    db.close()
