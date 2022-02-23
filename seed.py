from models import db ,User, Post, Tag, PostTag
from app import app

# Create all tables 
db.drop_all()
db.create_all()

# If table isn't empty, empty it
PostTag.query.delete()
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add users
Michael = User(first_name = 'Michael', last_name = 'Jordan', image_url='https://static01.nyt.com/images/2020/04/20/sports/20lastdance-sopan-1/merlin_171693069_1a044fc4-ffa8-44af-95d0-6f9842de6577-mobileMasterAt3x.jpg')
Lebron = User(first_name = 'Lebron', last_name = 'James', image_url='https://kingjamesgospel.com/wp-content/uploads/getty-images/2017/07/688480574.jpeg' )
Stephen = User(first_name = 'Stephen', last_name = 'Curry', image_url='https://images.actionnetwork.com/1200x675/blog/2021/12/stephencurry-38.jpg')
Kobe = User(first_name = 'Kobe', last_name = 'Bryant', image_url='https://img.republicworld.com/republic-prod/stories/promolarge/xhdpi/kys6wvk8dv9cakv6_1617458316.jpeg')

# Add and commit Users
db.session.add_all([Michael, Lebron, Stephen, Kobe])

db.session.commit()


#Add blog posts
mike1 = Post(title = 'The Last Dance', content = "I'm the greatest basketball player of all time.", user_id = 1)
mike2 = Post(title = '6 Rings', content = "I'm the greatest champion of all time.", user_id = 1)
mike3 = Post(title = 'Jordan Brand', content = "I'm the greatest brand of all time.", user_id = 1)


lebron1 = Post(title ='The Kid from Akron',content= "I'm the greatest basketball player of all time.", user_id = 2)
lebron2 = Post(title ="I'm Back",content= "Coming home to Cleveland.", user_id = 2)
lebron3 = Post(title ='The Big Three',content= "Dwyane Wade, Lebron James, Chris Bosh. One of the greatest trios of all time.", user_id = 2)


stephen1 = Post(title ='I Changed the Game of Basketball', content = "I'm the greatest shooter of all time.", user_id = 3)
stephen2 = Post(title ='Splash Brothers', content = "Steph Curry and Klay Thompson are the greatest backcourt duo of all time", user_id = 3)
stephen3 = Post(title ='2017-2018 Warriors', content = "Greatest team ever assembled.", user_id = 3)


kobe1 = Post(title ='Mamba Mentality', content = "I am a Laker for life.", user_id = 4)
kobe2 = Post(title ='Dear Basketball', content = "I am a Laker for life.", user_id = 4)
kobe3 = Post(title ='Kobe & Shaq', content = "Most dominant duo to ever the share the court", user_id = 4)

# Add and commit blog posts
db.session.add_all([mike1, mike2, mike3])
db.session.add_all([lebron1, lebron2, lebron3])
db.session.add_all([stephen1, stephen2, stephen3])
db.session.add_all([kobe1, kobe2, kobe3])

db.session.commit()


# Add Tags 
sports = Tag(name = 'Sports')
athlete = Tag(name = 'Athlete')
amazing = Tag(name = 'Amazing')
new = Tag(name = 'New')
important = Tag(name = 'Important')
fun = Tag(name = 'Fun')
cool = Tag(name='Cool')


# Add and commit tags
db.session.add_all([sports, athlete, amazing, new, important, fun, cool])

db.session.commit()


# Add Post - Tag relationship
pt1 = PostTag(post_id = 1 , tag_id = 1 )
pt2 = PostTag(post_id = 1 , tag_id = 2 )
pt3 = PostTag(post_id = 1 , tag_id = 3 )
pt4 = PostTag(post_id = 2 , tag_id = 1 )
pt5 = PostTag(post_id = 2 , tag_id = 2 )
pt6 = PostTag(post_id = 3 , tag_id = 2 )

# Add and commit post-tags
db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6])

db.session.commit()