import textwrap
idown = ("default") #QR code from a website purchase
lock = False

def sendMail(FROM,TO,SUBJECT,TEXT,SERVER):
    import smtplib
    """this is some test documentation in the function"""
    message = textwrap.dedent("""\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT))
    
while (lock == False):
    print("Scan QR code")
    idvisitor = ("default")
    if (idown == idvisitor):
        lock = True #when true send signal that lock can be opened
        server = smtplib.SMTP(SERVER) #send mail
        server.sendmail(FROM, TO, message)
        server.quit()
    else:
        print("Unknown QR code, please try again")
