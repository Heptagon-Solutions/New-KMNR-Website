from flask_mysqldb import MySQL

# Imported here for easier importing into other files that need error handling
from MySQLdb import Error as DatabaseError

db = MySQL()
