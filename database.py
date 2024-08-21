from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

##  Our declarative base, which remember, declarative base is how we get those inherited properties for our models.
## So going to grab that declarative base. And we're actually going to go ahead and use it really quick and create our base class.

class Base(DeclarativeBase): #Creating our Base model that will be inherited by all other models
    pass


## The main thing we want from declarative base is the mapped and mapped column features that it comes with. So when we're setting up our database, we have that map premise already set up for us so that we can kind of create those those fields pretty easily.


db = SQLAlchemy(model_class=Base) #Instantiating our db

## this is really just telling us what to expect from our models. They will all be children of this base class that we've just created.

Base.query = db.session.query_property()