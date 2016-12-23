#! /usr/bin/python3

import os, re, sys
import argparse

from smtplib import SMTP_SSL as SMTP  # Invokes secure protocol
from email.mime.text import MIMEText  # Use this for unsecure protocol

USERNAME = ''  # Username to log in to the SMTP server
PASSWORD = ''  # Password for the login
SMTPserver = ''  # Domain of SMTP server
sender = ''  # Sender's address


class OrderContent:
    size = ['S', 'M', 'L', 'XL', '2XL', '3XL']
    color = ['pink', 'black', 'white']
    sleeve = ['long', 'short']
    sex = ['M', 'W']

#  Message to send in the body of the email
def message(quantity, size, sex, color, sleeve, tracking):
    content = '''\
    \t\tItem:  %s %s %s \n
    \t\tSize: %s \n
    \t\tQuantity: %s\n
    In order to track your purchase, please visit https://tools.usps.com, and provide the following number: \n
    \t\tTracking number:  %s \n
    Thank you!\n
    ''' % (sex, color, sleeve, size, quantity, tracking)
    return content


def main():

    # Main arguments I want are DESTINATION ADDRESS and ORDER NUMBER
    parser = argparse.ArgumentParser(description='Emailer program')
    parser.add_argument('ORDER_NUMBER')
    parser.add_argument('DESTINATION')
    parser.add_argument('TRACKING')
    args = parser.parse_args()
    order_number = args.ORDER_NUMBER
    destination = args.DESTINATION
    tracking = args.TRACKING
    subject = 'Order #%s' % order_number
    text_subtype = 'plain'
    print('\nCustomer email:  %s\nOrder number: %s\nTracking number: %s\n\n' % (destination, str(order_number), str(tracking)))

    answer = 'N'
    while (answer.upper() == 'N'):
        quantity = 0
        while(quantity <= 0):
            quantity = int(input('\nEnter quantity -> '))
        size = ''
        while size.upper() not in OrderContent.size:
            print('\nSizes = [S, M, L, XL, 2XL, 3XL]')
            size = input('Enter size -> ')
        else:
            size = size.upper()
        sex = ''
        while sex.upper() not in OrderContent.sex:
            sex = input('\nEnter sex [M, W] -> ')
        else:
            if(sex.upper() == 'M'):
                sex = 'Men\'s'
            if(sex.upper() == 'W'):
                sex = 'Women\'s'
        color = ''
        while color.lower() not in OrderContent.color:
            color = input('\nEnter color [black, white, pink] -> ')
        else:
            color = color.lower()
        sleeve = ''
        while sleeve.lower() not in OrderContent.sleeve:
            sleeve = input('\nEnter sleeve [short, long] -> ')
        else:
            if (sleeve.lower() == 'short'):
                sleeve = 'short sleeve'
            if (sleeve.lower() == 'long'):
                sleeve = 'long sleeve'
        print('\nIs this the message you want to send? \n')
        print('***\n')
        print(message(quantity, size, sex, color, sleeve, tracking) + '\n')
        print('***\n')
        answer = input('Y or N: ')
    print('Sending message...')

    try:
        msg = MIMEText(message(quantity, size, sex, color, sleeve, tracking), text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            print('SUCCESS!, closing connection')
            conn.quit()

    except Exception as exc:
        sys.exit("mail failed; %s" % str(exc))

if __name__ == '__main__':
    main()