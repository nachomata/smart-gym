
import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from pn532pi import Pn532Hsu

# Set the desired interface to True
SPI = False
I2C = True
HSU = False

if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
# When the number after #elif set as 1, it will be switch to HSU Mode
elif HSU:
    PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
    nfc = Pn532(PN532_HSU)

# When the number after #if & #elif set as 0, it will be switch to I2C Mode
elif I2C:
    PN532_I2C = Pn532I2c(1)
    nfc = Pn532(PN532_I2C)


def setup():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if (not versiondata):
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    #  Got ok data, print it out!
    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    #  configure board to read RFID tags
    nfc.SAMConfig()

    print("Waiting for an ISO14443A Card ...")


def loop():
    #  Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
    #  'uid' will be populated with the UID, and uidLength will indicate
    #  if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if (success):
        #  Display some basic information about the card
        print("Found an ISO14443A card")
        print("UID Length: {:d}".format(len(uid)))
        print("UID Value: {}".format(binascii.hexlify(uid)))
    return False


def read_nfc():
    error = True
    while error:
        try:
            setup()
            error = False
        except Exception as e:
            print(f"retrying setup because: {e}")
            time.sleep(2)
            print(f"trying setup again...")
    
        error = True
        try:
            success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
            error = not success
            if success:
                return uid
        except Exception as e:
            print(f"reading again because: {e}")
            time.sleep(2)
            print("continuing...")
    
if __name__ == '__main__':
    error = True
    while error:
        try:
            setup()
            error = False
        except Exception as e:
            print(f"retrying setup because: {e}")
            time.sleep(2)
            print(f"trying setup again...")
        
    error = True
    while error:
        try:
            found = loop()
            while not found:
                print("now we wait for a card")
                time.sleep(5)
                print("reading again")
                found = loop()
        except Exception as e:
            print(f"reading again because: {e}")
            time.sleep(2)
            print("continuing...")
        