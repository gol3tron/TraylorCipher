import sys
import math
import random

class TraylorCipher:
  
  def encrypt(self, stringToEncrypt):
    
    # Our initial E
    traylorString = 'E'
    
    # Step 1. Add make padding
    pad = TraylorCipher.makePad()
    num_padded_Bytes_arrayform = TraylorCipher.numberToBinaryArray(len(pad))
    traylorString += TraylorCipher.arrayToTraylorByte(num_padded_Bytes_arrayform)
    
    # Step 2. Encrypt each letter to a Traylor Byte
    for index in range(len(stringToEncrypt)):
      
      traylorString += TraylorCipher.characterToTraylorByte(stringToEncrypt[index])
      
    # Step 3. Add padding 
    for index in range(len(pad)):
      
      traylorString += TraylorCipher.arrayToTraylorByte(pad[index])

    return traylorString
    
  def decrypt(self, stringToDecrypt):
    
    decryptedString = ''
    
    # Step 1. Strip inital E
    stringToDecrypt = stringToDecrypt[1:]
    
    # Step 2. Strip padding
    # Calculate the number of traylor bytes in the padding
    num_traylor_bytes_in_pad = ord(TraylorCipher.traylorByteToCharacter(stringToDecrypt[0:8]))
    # remove the padding
    stringToDecrypt = stringToDecrypt[:len(stringToDecrypt)-(num_traylor_bytes_in_pad*8)]
    stringToDecrypt = stringToDecrypt[8:] #remove the byte that tells you how much padding there is
    
    # Step 3. Decrypt each Traylor Byte to a character
    # Jump each increment of 8 Traylor Bits
    for index in range(0, len(stringToDecrypt), 8):
      
      decryptedString += TraylorCipher.traylorByteToCharacter(stringToDecrypt[index : index + 8])
    
    return decryptedString
    
  # Helper Functions
  
  # Convert a single character to an 8-letter Traylor "byte"
  @staticmethod
  def characterToTraylorByte(character):
    
    if(len(character) != 1):
      
      raise TraylorException("Invalid character to convert to Traylor Byte.")
    
    asciiValue = ord(character)
    
    binaryArray = TraylorCipher.numberToBinaryArray(asciiValue)
    traylorByte = ''
    
    # Go through binary array, creating Traylor byte
    for index in range(len(binaryArray)):
      
      if(binaryArray[index] == 0):
        
        traylorByte += 'r'
        
      else:
        
        traylorByte += 'R'
        
    return traylorByte
    
  # Convert a 8-bit array to TraylorByte
  @staticmethod
  def arrayToTraylorByte(array):
    
    if(len(array) != 8):
      
      raise TraylorException("Invalid array to convert to Traylor Byte.")
    
    
    binaryArray = array
    traylorByte = ''
    
    # Go through binary array, creating Traylor byte
    for index in range(len(binaryArray)):
      
      if(binaryArray[index] == 0):
        
        traylorByte += 'r'
        
      else:
        
        traylorByte += 'R'
        
    return traylorByte
    
  # Generates padding for encrypted text based on 
  # randomly generated number
  @staticmethod
  def makePad():
    random_seed = random.randint(0,255)
    
    pad = []
    
    for i in range(random_seed):
      next_byte = random.randint(0,255)
      pad.append(TraylorCipher.numberToBinaryArray(next_byte))
      
    return pad
    
  # Convert a Traylor Byte to a single ASCII character
  @staticmethod
  def traylorByteToCharacter(traylorByte):
  
    if(len(traylorByte) != 8):
      
        raise TraylorException("Invalid Traylor Byte length to convert to character.")
        
    bitArray = []      
  
    # Convert Rs to 1s and rs to 0s
    for index in range(len(traylorByte)):
      
      traylorBit = traylorByte[index]
      
      if(traylorBit != 'R' and traylorBit != 'r'):
        
        raise TraylorException("Invalid Traylor Byte content to convert to character.")
      
      # Derive the bit value
      bitValue = 1 if (traylorBit == 'R') else 0
      
      # Add to the bitArray
      bitArray.append(bitValue)
      
    # Convert to number via sub-method
    value = TraylorCipher.binaryArrayToNumber(bitArray)
    
    # Convert to ASCII character and return
    return chr(value)
    
  # Convert a number to a 8-element array of 1s and 0s
  # Where array position corresponds to factor of 2
  @staticmethod
  def numberToBinaryArray(number):
    
    value = 0
    
    # First, convert and check for a number
    try:
    
      value = int(number)
      
    except ValueError:
    
      raise TraylorException("Non-number passed to binary array conversion.")
    
    # 1 byte represents base-10 numbers 0-255.
    # Next, check for a valid number range
    if(number > 255 or number < 0):
      
      raise TraylorException("Invalid number passed to binary array conversion.")
    
    binaryArray = [0, 0, 0, 0, 0, 0, 0, 0]
    
    # Begin at 7, decrement to 0
    for exponent in range(len(binaryArray) - 1, -1, -1):

      powerOf2 = math.pow(2, exponent)

      if(number >= powerOf2):
        
        number -= powerOf2
        binaryArray[exponent] = 1

    return binaryArray
    
  # Convert a 8-element array of 1s and 0s to a number 0-255
  # In the array, array index corresponds to factor of 255
  @staticmethod
  def binaryArrayToNumber(binaryArray):
    
    if(len(binaryArray) != 8):
      
      raise TraylorException("Invalid binary array length.")
      
    runningSum = 0
      
    for exponent in range(len(binaryArray)):
      
      if(binaryArray[exponent] == 1):
        
        runningSum += math.pow(2, exponent)
        continue
      
      if(binaryArray[exponent] != 0):
        
        raise TraylorException("Invalid binary array contents.")
        
    return int(runningSum)
    
class TraylorException(Exception):
    
  pass
  
TraylorCipher.characterToTraylorByte('a')
