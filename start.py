from qrcode import *
import time
import datetime
import textwrap
import smtplib
import uuid
import sys
import os
import qrtools
import MySQLdb
import picamera
import RPi.GPIO as GPIO

# ----------------- SETUP ------------------------------------------------

GPIO.setmode(GPIO.BCM)

cameraSwitchPin = 17
adminSwitchPin = 18
ledPin = 8

# Setup pins
GPIO.setup(cameraSwitchPin, GPIO.IN)
GPIO.setup(adminSwitchPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)

# Setup camera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
save_path = '/home/pi/picamera/' #edit this

count = 0
door_locked = True
admin_email = 'mail@example.com'
smtpObj = smtplib.SMTP(host, port, local_hostname) # SMTP object

# MySQL credentials
dict = { 'host' : 'mysql.metropolia.fi',
        'username' : 'kasperst',
        'password' : 'sqlkaitsu',
        'db_name' : 'kasperst' }

# Create db
sql_create()

# ----------------- FUNCTIONS ------------------------------------------------
def camera_fn():
    print "Button pressed, three (3) sec to take photo"
    time.sleep(3)
    camera.capture(save_path + 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')
    
    # Decode QR code here
    print "will run future decode function"
    
    # SQL READ function associated here
    person_info = sql_read(id) # Tuple
    if (!person_info == NULL):
        # Open door
        print "Access granted"
        GPIO.output(ledPin, GPIO.HIGH) # LED on (door open)
        # Send email notification
        send_email(person_info)
    else:
        print "Access denied"

def admin_fn():
    print("Welcome to BAD industries, what action would you like to take?").lower()
    user_prompt = raw_input("-> ")
    if user_prompt == "generate" or user_prompt == "gen" or user_prompt == "1" or user_prompt == "create qr" or user_prompt =="g":
        purchase_code_fn()
    elif user_prompt == "update database" or user_prompt == "update" or user_prompt =="2" or user_prompt =="update db" or user_prompt =="u":
        print "will run future update function"
        # SQL UPDATE function associated here
        print("exit")
    elif user_prompt == "delete user" or user_prompt == "delete" or user_prompt =="3" or user_prompt =="del" or user_prompt =="d":
        print "will run future delete function"
        # SQL DELETE function associated here
        print("exit")
    elif user_prompt == "help" or user_prompt =="h":
        print("You can pick from: ")
        print("1) Generate QR Code")
        print("2) Update data")
        print("3) Delete data")
        print("4) Exit")
        admin_fn()
    elif user_prompt == "exit" or user_prompt == "4" or user_prompt == "quit" or user_prompt == "e":
        sys.exit()
        
    else:
        print ("If you would like to look at the available options please type help")
        admin_fn()

# ----------------- QR CODE FUNCTIONS ------------------------------------------------
def qr_code_fn(id, email, name):
    qr = QRCode(version=5, error_correction=ERROR_CORRECT_M)
    qr.add_data(id, str(email))
    print (str(id))
    print (str(email))
    qr.make()
    im = qr.make_image()
    im.save(str(name)+ str(count) + ".png")
    # Save to db
    sql_insert(id, name, email)
    restart_fn()


def purchase_code_fn():
    global count
    count =+ 1
    name = raw_input("Please enter your name: ")
    email_prompt = raw_input("Please enter your email address: ")
    userid = uuid.uuid4()
    qr_code_fn(userid, email_prompt, name)
    
# ----------------- OTHER FUNCTIONS ------------------------------------------------

def restart_fn():
    restart_prompt = raw_input("Would you like to run another process? ").lower()
    if restart_prompt == "yes" or restart_prompt == "y":
        admin_fn()

    elif restart_prompt =="no" or restart_prompt == "n":
        sys.exit("Closing....")
    else:
        restart_fn()

def send_email(info):
    name = info[0]
    email = info[1]
    # Send for admin also

# ----------------- MYSQL FUNCTIONS ------------------------------------------------

# CREATE
def sql_create():
    create_tables = """CREATE TABLE QRCODES (
        ID INT NOT NULL AUTO_INCREMENT,
        QR_ID CHAR(32) NOT NULL,
        NAME CHAR(50) NOT NULL,
        EMAIL CHAR(30) NOT NULL,
        PRIMARY KEY (ID)"""

    try:
        db = MySQLdb.connect(dict['host'], dict['username'], dict['password'], dict['db_name'])
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS QRCODES")
        cursor.execute(create_tables)
    except:
        print "Error: unable to create db tables"
        db.rollback()
    db.close()

# INSERT
def sql_insert(id, name, email):
    insert_values = """INSERT INTO QRCODES(QR_ID, NAME, EMAIL)
        VALUES ('%s', '%s', '%s')""" % (id, name, email)

    try:
        db = MySQLdb.connect(dict['host'], dict['username'], dict['password'], dict['db_name'])
        cursor = db.cursor()
        cursor.execute(insert_values)
        db.commit()
    except:
        print "Error: unable to insert in db"
        db.rollback()
    db.close()

# UPDATE
def sql_update(id, name, email):
    update_data = """UPDATE QRCODES SET NAME = '%s', EMAIL = '%s'
        WHERE QR_ID = '%s'""" % (name, email, id)

    try:
        db = MySQLdb.connect(dict['host'], dict['username'], dict['password'], dict['db_name'])
        cursor = db.cursor()
        cursor.execute(update_data)
        db.commit()
    except:
        print "Error: unable to update in db"
        db.rollback()
    db.close()

# DELETE
def sql_delete(id):
    delete_data = "DELETE FROM QRCODES WHERE QR_ID = '%s'" % (id)

    try:
        db = MySQLdb.connect(dict['host'], dict['username'], dict['password'], dict['db_name'])
        cursor = db.cursor()
        cursor.execute(delete_data)
        db.commit()
    except:
        print "Error: unable to delete from db"
        db.rollback()
    db.close()

# READ
def sql_read(id):
    select_data = "SELECT * FROM QRCODES \
        WHERE QR_ID = '%s'" % (id)

    try:
        db = MySQLdb.connect(dict['host'], dict['username'], dict['password'], dict['db_name'])
        cursor = db.cursor()
        cursor.execute(select_data)
        # Results
        results = cursor.fetchall()
        for row in results:
            name = row[2]
            email = row[3]
        return (name, email)
    except:
        print "Error: unable to read from db"
        #db.rollback()
        return NULL
    db.close()

# ----------------- MAIN LOOP ------------------------------------------------
# Main loop, detect button press (some kind of observer here rather than infinite loop?)
while True:
    GPIO.output(ledPin, GPIO.LOW) # LED off (door closed)

    if GPIO.input(cameraSwitchPin):
        camera_fn()
    elif GPIO.input(adminSwitchPin):
        admin_fn()
    else:
        pass