"""
################################################################################################
self-test when this file is run as program
################################################################################################
"""

import sys
sys.path.append('..')
import mailconfig
print('config:', mailconfig.__file__)

# get from __init__
from Internet.Email.mailtools import (MailFetcherConsole, MailSender,
                                      MailSenderAuthConsole, MailParser)

if not mailconfig.smtpuser:
    sender = MailSender(tracesize=5000)
else:
    sender = MailSenderAuthConsole(mailconfig.smtpservername, mailconfig.popusername, tracesize=5000)

sender.sendMessage(From=mailconfig.popusername,
                   To=[mailconfig.smtpuser],
                   Subj='Testing mailtoos package',
                   extrahdrs=[('X-Mailer', 'mailtools')],
                   bodytext='Here is my source code\n',
                   attaches=['selftest.py'])
                  # bodytextEncoding='utf-8'                  # other test
                  # attachesEncodings=['latin-1'],            # check title
                  # attaches=['monkeys.jpg']                  # check base64
                  # to='i18n adddr list...'                   # test Mime/Unicode


def status(*args):
    print(args)

fetcher = MailFetcherConsole()
hdrs, sizes, loadedall = fetcher.downloadAllHeaders(status)
for num, hdr in enumerate(hdrs[:5]):
    print(hdr)
    if input('load mail?') in ['y', 'Y']:
        print(fetcher.downloadMessage(num+1).rstrip(), '\n', '-'*70)

last5 = len(hdrs) - 4
msgs, sizes, loadedall = fetcher.downloadAllMessages(status, loadfrom=last5)
for msg in msgs:
    print(msg[:200], '\n', '-'*70)

parser = MailParser()
for i in range(0, len(msgs)):
    fulltext = msgs[i]
    message = parser.parseMessage(fulltext)
    ctype, maintext = parser.findMainText(message)
    print('Parsed:', message['Subject'])
    print(maintext)
input('Press Enter to exit')
