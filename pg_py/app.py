from database import Database
from user import User

Database.initialise()





my_user = User('seubs101780@yahoo.com', 'Jonny', 'Jonnington The 3rd', None)

my_user.save_to_db()

user_from_db = User.load_from_db_by_mail('finisher@yahoo.com')

print(user_from_db)