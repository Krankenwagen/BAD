from qrcode import *
import time
import uuid
import sys
import qrtools

count = 0


def qr_code_fn(id, email, name):
    qr = QRCode(version=5, error_correction=ERROR_CORRECT_M)
    qr.add_data(id, str(email))
    print (str(id))
    print (str(email))
    qr.make()
    im = qr.make_image()
    im.save(str(name)+ str(count) + ".png")
    restart_fn()


def purchase_code_fn():
    global count
    count =+ 1
    name = raw_input("Please enter your name: ")
    email_prompt = raw_input("Please enter your email address: ")
    userid = uuid.uuid4()
    qr_code_fn(userid, email_prompt, name)
    


def restart_fn():
    restart_prompt = raw_input("Would you like to run another process? ").lower()
    if restart_prompt == "yes" or restart_prompt == "y":
        launch_fn()

    elif restart_prompt =="n" or restart_prompt == "no":
        sys.exit("Closing....")
    else:
        restart_fn()


def launch_fn():
    print("Welcome to BAD industries, what action would you like to take?").lower()
    user_prompt = raw_input("-> ")
    if user_prompt == "generate" or user_prompt == "gen" or user_prompt == "1" or user_prompt == "create qr" or user_prompt =="g":
        purchase_code_fn()
    elif user_prompt == "decode" or user_prompt == "dec" or user_prompt =="2" or user_prompt =="decode qr" or user_prompt =="q":
        print "will run future decode function"
        print("exit")
    elif user_prompt == "help" or user_prompt =="h":
        print("You can pick from: ")
        print("1) Generate QR Code")
        print("2) Decode QR code")
        print("3) Exit")
        launch_fn()
    elif user_prompt == "exit" or user_prompt == "3" or user_prompt == "quit" or user_prompt == "e":
        sys.exit()
        
    else:
        print ("If you would like to look at the available options please type help")
        launch_fn()
        
        
    
    

launch_fn()
    
    
