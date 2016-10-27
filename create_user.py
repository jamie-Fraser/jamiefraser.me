from app.models import User
from app import app, db

jamie = User()
jamie.nickname = "jamie"
jamie.set_password("workworkwork")
jamie.email = "jamie@jamiefraser.me"
jamie.about_me = "My name is Jamie"

db.session.add(jamie)
db.session.commit()
