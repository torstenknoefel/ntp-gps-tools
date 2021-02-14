#!/usr/bin/env python3
#
# Hack to initalize a u-blox gps receiver connected to a Raspberry Pi 
# with a supplied config created by the u-center application
#
# Cobbled together by Torsten Knoefel http://torsten.knoefel.blog


import serial



def UBXChecksum(payload):
  """Creates a checksum of the payload and returns it"""
  CK_A = CK_B = 0
  for b in payload[2:]:       # Ignore first sync bytes of command string
    CK_A += b
    CK_B += CK_A
  return CK_A & 0xff, CK_B & 0xff
    
def sendUBXCommand(ser, payload):
  """Adds checksum to payload command and sends it to the serial port. Returns true if message received."""
  # First, lets create the checksum and add it to the end
  CK_A = CK_B = 0
  for b in payload[2:]:       # Ignore first sync bytes of command string
    CK_A += b
    CK_B += CK_A
  payload.append(CK_A & 0xff)
  payload.append(CK_B & 0xff)
  ser.reset_output_buffer()
  written = ser.write(payload)
  print(str(written) + " bytes written...")
  AkorNak = ser.read(10)
  print('{}'.format(AkorNak))
  print(''.join('{:02x}'.format(a) for a in payload))

def main():
  with open('/etc/ublox/config.txt', 'r') as config:
    with serial.Serial(
      port='/dev/gps0',
      baudrate=9600,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      write_timeout=1,
      xonxoff=False,
      rtscts=False,
      dsrdtr=False
    ) as ser:
      for line in config:
        words = line.split()
        if (len(words) > 0):
#          print(words[0])
          cmd = [0xB5, 0x62]
          for word in words[2:]:
            cmd.append(int(word, base=16))
          payload = bytearray(cmd)
          sendUBXCommand(ser, payload)
#          print(payload)

if __name__ == '__main__':
    main()

