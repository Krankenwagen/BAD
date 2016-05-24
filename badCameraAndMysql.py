# Camera stuff

import picamera
import time
import datetime

camera = picamera.PiCamera()
camera.resolution = (1024, 768)

#camera.capture('name.jpg')
#time.sleep(5) #seconds

filepath = '/home/pi/picamera/' #edit this

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(5)
    for filename in camera.capture_continuous(filepath + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
        print('Captured %s' % filename)
        time.sleep(5)


# MySQL stuffffff

# install mysql !

import MySQLdb

# Open database connection
db = MySQLdb.connect("mysql.metropolia.fi", "kasperst", "sqlkaitsu", "kasperst" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


# Create table as per requirement
create_tables = """CREATE TABLE QRCODES (
         ID INT NOT NULL AUTO_INCREMENT,
         QR_ID CHAR(32) NOT NULL,
         FIRST_NAME CHAR(20) NOT NULL,
         LAST_NAME CHAR(20) NOT NULL,
         EMAIL CHAR(30) NOT NULL,
         PRIMARY KEY (ID)"""

# Prepare SQL query to INSERT a record into the database.
insert_values = """INSERT INTO QRCODES(QR_ID, FIRST_NAME,
         LAST_NAME, EMAIL)
         VALUES ('%s', '%s', '%s', '%s')""" % (QR_ID, FIRST_NAME, LAST_NAME, EMAIL)

# Prepare SQL query to READ data.
select_data = "SELECT * FROM QRCODES \
        WHERE QR_ID = '%s'" % (qr_code)

# Prepare SQL query to UPDATE required records
update_data = "UPDATE QRCODES SET FIRST_NAME = 'example' \
        WHERE FIRST_NAME = 'name'"

# Prepare SQL query to DELETE required records
delete_data = "DELETE FROM QRCODES WHERE FIRST_NAME = '%s'" % (example)

try:
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS QRCODES")

    # Examples for executing the SQL command
    cursor.execute(create_tables)
    cursor.execute(insert_values)
    cursor.execute(update_data)
    cursor.execute(select_data)
    cursor.execute(delete_data)
    # Read results
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        qr_id = row[1]
        fname = row[2]
        lname = row[3]
        email = row[4]

    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

# disconnect from server
db.close()

