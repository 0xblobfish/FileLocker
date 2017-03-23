FileLocker is a python tool that allows you to protect your important files using an AES key of 16 or 32 characters long.

The Help menu :

`Usage : python fileLocker.py [options]`<br />
<br />
`Options `<br />
`	-h			Display this menu`<br />
`	-c PATH			PATH is the file you want to crypt`<br />
`	-d PATH			PATH is the file you want to decrypt`<br />
`	-k KEY			KEY is the AES key wich be used tu crypt and decrypt your file, KEY must be 16, 24 or 32 caracter long`<br />
`	-o OUTPUT		OUTPUT is the output file`<br />
`	--random-key LEN	Generate a random key and LEN is the number of caracters (16 or 32)`<br />
`	--compress LEVEL	Where 'LEVEL' is the level of compression [1-9]. By default, the compression level is 1`<br />
