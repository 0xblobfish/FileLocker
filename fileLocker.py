#!/usr/bin/python
# -*-coding:utf-8-*-
import base64
import binascii
import os
import random
import string
import subprocess
import sys
import time
import zlib
from Crypto.Cipher import AES

version = '1.0'
banner = "\n\n   ___ _ _          __            _             \n  / __(_) | ___    / /  ___   ___| | _____ _ __ \n / _\ | | |/ _ \  / /  / _ \ / __| |/ / _ \ '__|\n/ /   | | |  __/ / /__| (_) | (__|   <  __/ |   \n\/    |_|_|\___| \____/\___/ \___|_|\_\___|_|   \n                                                v" + version + "\n\n"

BLOCK_SIZE = 32
PADDING = '('

msg_help = "\nUsage : python F1le_L0cker.py [options]\n\nOptions :\n\t-h\t\t\tDisplay this menu\n\t-c PATH\t\t\tPATH is the file you want to crypt\n\t-d PATH\t\t\tPATH is the file you want to decrypt\n\t-k KEY\t\t\tKEY is the AES key wich be used tu crypt and decrypt your file, KEY must be 16, 24 or 32 caracter long\n\t-o OUTPUT\t\tOUTPUT is the output file\n\t--random-key LEN\tGenerate a random key and LEN is the number of caracters (16 or 32)\n\t--compress LEVEL\tWhere \'LEVEL\' is the level of compression [1-9]. By default, the compression level is 1\n"

clear = lambda: os.system('')

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

compresslevel = 1

EncodeAES = lambda c, s: zlib.compress(base64.b64encode(c.encrypt(pad(binascii.hexlify(s)))), compresslevel)
DecodeAES = lambda c, s: binascii.unhexlify(str(c.decrypt(base64.b64decode(zlib.decompress(s))).rstrip(PADDING)))


def random_string(i):
    return ''.join(random.choice(string.ascii_uppercase + string.lowercase) for _ in range(i))


def help_display(error):
    clear()
    print(banner)
    print(msg_help)
    print(error)
    sys.exit(1)


arguments = sys.argv
specified_path = ''
specified_key = ''
crypt = True

if '-h' in arguments:
    help_display('')

if len(arguments) < 4:
    help_display('[x] Error, not enough arguments')
elif '-k' in arguments and '--random-key' in arguments:
    help_display('[x] Error, you can\'t give a custom key and use the \'--random-key\' option')
elif '-c' in arguments == False or '-d' in arguments == False:
    help_display('[x] Error, you must specified a path or file to crypt')
clear()
print(banner)
print('[i] Initialisation...')

if '-c' in arguments:
    crypt = True
    try:
        specified_path = os.path.abspath(arguments[int(arguments.index('-c')) + 1])
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)
if '-d' in arguments:
    crypt = False
    try:
        specified_path = os.path.abspath(arguments[int(arguments.index('-d')) + 1])
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)

try:
    test = open(specified_path, 'r')
    test.close()
except:
    print('[x] Error, the file specified is not found or access denied\nExiting script....\n')
    sys.exit(1)

if '-k' in arguments:
    try:
        specified_key = arguments[int(arguments.index('-k')) + 1]
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)
    if len(specified_key) != 16 and len(specified_key) != 32 and len(specified_key) != 24:
        print(
            '[x] Error, the specified key is incorrect, you must specified a key with 16, 24 or 32 caracters\nExiting script....\n')
        sys.exit(1)
    else:
        BLOCK_SIZE = int(len(specified_key))

elif '--random-key' in arguments:
    try:
        key_len = arguments[int(arguments.index('--random-key')) + 1]
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)

    if key_len != '16' and key_len != '32' and key_len != '24':
        print(
        '[x] Error, the specified lenght of the random key is incorrect, it must be 16, 24 or 32\nExiting script....\n')
        sys.exit(1)
    else:
        specified_key = random_string(int(key_len))
        BLOCK_SIZE = int(key_len)

if '--compression' in arguments:
    try:
        compresslevel = int(arguments[int(arguments.index('--compression')) + 1])
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)

    if compresslevel < 1 or compresslevel > 9 or compresslevel / 10 != 0:
        print('[x] Error, the specified compression level is incorrect! It must be 1 to 9\nExiting script....\n')
        sys.exit(1)

if '-o' in arguments:
    try:
        outpath = os.path.abspath(arguments[int(arguments.index('-o')) + 1])
    except:
        print('[x] Error in your syntax, please use \'-h\' option\nExiting script....\n')
        sys.exit(1)

else:
    if crypt:
        outpath = specified_path[:-int(len(specified_path.split('/')[-1]))] + 'crypted_' + specified_path.split('/')[-1]
    else:
        outpath = specified_path[:-int(len(specified_path.split('/')[-1]))] + 'decrypted_' + specified_path.split('/')[
            -1]

if crypt:
    decrypted_path = specified_path
    crypted_path = outpath
    print('[i] Crypting \'' + specified_path + '\'')
    print('[i] Using the ' + str(BLOCK_SIZE) + ' bit len key : \'' + specified_key + '\'')
    print('[i] Using the compression level : \'' + str(compresslevel) + '\'')
    cipher = AES.new(specified_key)
    crypt_file = open(crypted_path, 'w')
    clean_file = open(decrypted_path, 'r')
    crypt_file.write(EncodeAES(cipher, clean_file.read()))
    clean_file.close()
    crypt_file.close()
    print('[*] File crypted and saved in ' + crypted_path)
    sys.exit(0)

else:
    crypted_path = specified_path
    decrypted_path = outpath
    print('[i] Decrypting \'' + specified_path + '\'')
    print('[i] Using the ' + str(BLOCK_SIZE) + ' bit len key : \'' + specified_key + '\'')
    print('[i] Using the compression level : \'' + str(compresslevel) + '\'')
    cipher = AES.new(specified_key)
    crypt_file = open(crypted_path, 'r')
    clean_file = open(decrypted_path, 'w')
    try:
        clean_file.write(DecodeAES(cipher, crypt_file.read()))
    except:
        print('[x] Error, incorrect key !\nExiting script....\n')
        clean_file.close()
        crypt_file.close()
        sys.exit(1)
    clean_file.close()
    crypt_file.close()
    print('[*] File decrypted and saved in ' + decrypted_path)
    sys.exit(0)
