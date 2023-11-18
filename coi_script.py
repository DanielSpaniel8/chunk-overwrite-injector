# # # sw-coi is a tool to inject lua code into .scene and .scl files in swordigo 
  

from os import system as command




# open the injection file and get the lines

coi = open('./test.coi', 'r')

lines = coi.readlines()

coi.close()

# define some working variables

targetFile = ''
injectionOffset = ''
chunkLength = ''
chunk = ''
chunkString = b''



# copy the apk

command('cp ./in.apk ./coi-temp.zip')

# make a temporary folder and extract the files

command('mkdir ./coi-temp')

command('unzip ./coi-temp.zip -d coi-temp')

def inject():   # inject lua chunk into target file

    global chunkString
    global chunk

    # get bytes from the target file
    with open(('./coi-temp/' + targetFile), 'rb') as file:

        targetBytes = file.read()

    # convert chunk from base16 to ASCII

    for i in range(int( len(chunk) / 2 )):

        # take first byte then remove it from the chunk
        thisByte = chunk[0:2]

        chunkString += bytes.fromhex(thisByte)

        chunk = chunk[2:]


    # add the chunk bytes to the original file
    targetBytes = bytearray(targetBytes)
    

    # remove the part of the original file that will be replaced
    targetBytesSecondHalf = targetBytes[ int(injectionOffset) + int(chunkLength) : ]
    
    targetBytes = targetBytes[ : int(injectionOffset) ]

    targetBytes += targetBytesSecondHalf



    targetBytes[ int(injectionOffset) : int(chunkLength) ] = chunkString

    with open(('./coi-temp/' + targetFile), 'wb') as file:

        file.write(targetBytes)
        
        

# get injection info and run injection

for line in lines:

    if line[0] == '#':   # set target file

        targetFile = line[1:-1]

    if line[0] == '?':   # set offset for injection

        injectionOffset = line[1:-1]

    if line[0] == '-':   # set length of chunk to inject

        chunkLength = line[1:-1]

    if line[0] == '|':   # get lua code chunk to inject

        chunk = line[1:-1]

        inject()   # run injection function




# rezip files

import zipfile
import os

# Create a zip file using Python's zipfile module
with zipfile.ZipFile('./out.apk', 'w') as out_zip:
    for foldername, subfolders, filenames in os.walk('./coi-temp'):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, './coi-temp')
            out_zip.write(filepath, arcname)

# Remove the temporary folder and the zip file
command('rm -R coi-temp')

command('rm coi-temp.zip')
