from models import User, db
from app import app

# Create all tables 
db.drop_all()
db.create_all()


# If table isn't empty, empty it
User.query.delete()

# Add users
Michael = User(first_name = 'Michael', last_name = 'Jordan', image_url='https://static01.nyt.com/images/2020/04/20/sports/20lastdance-sopan-1/merlin_171693069_1a044fc4-ffa8-44af-95d0-6f9842de6577-mobileMasterAt3x.jpg')
Lebron = User(first_name = 'Lebron', last_name = 'James', image_url='https://kingjamesgospel.com/wp-content/uploads/getty-images/2017/07/688480574.jpeg' )
Stephen = User(first_name = 'Stephen', last_name = 'Curry', image_url='https://images.actionnetwork.com/1200x675/blog/2021/12/stephencurry-38.jpg')
Kobe = User(first_name = 'Kobe', last_name = 'Bryant', image_url='https://img.republicworld.com/republic-prod/stories/promolarge/xhdpi/kys6wvk8dv9cakv6_1617458316.jpeg')


# Add new objects to session, so they'll persists
db.session.add(Michael)
db.session.add(Lebron)
db.session.add(Stephen)
db.session.add(Kobe)

# Commit--otherwise, this never gets saved
db.session.commit()