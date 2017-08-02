try:
    from PIL import Image, ImageMath
    from webcolors import hex_to_rgb, rgb_to_hex
except:
    input("Please install PIL and webcolors(pip3 install Image and pip3 install webcolors).\nPress enter to exit.")
    exit()
import translate, os
from time import strftime

def str2bin(string):
    return translate.lp2b(string)

def bin2str(binary):
    return translate.lb2p(binary)

def rgb2hex(r, g, b):
    return rgb_to_hex((r, g, b))

def hex2rgb(hexcode):
    return hex_to_rgb(hexcode)

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1]+digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

def hide(filename, message):
    img = Image.open('files/' + filename)
    binary = str2bin(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        temp = ''
        for item in datas:
            if (digit < len(binary)):
                newpix = encode(rgb2hex(item[0], item[1], item[2]),binary[digit])
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)
        img.putdata(newData)
        try:
            img.save('files/' + filename + ".converted", "PNG")
        except:
            os.mkdir('files/')
            img.save('files/' + filename + ".converted", "PNG")
        print("Message successfully hidden.")
        return 'files/' + filename
    print("Incorrect image mode. Message not hidden.")
    return None

def retr(filename):
    img = Image.open('files/' + filename + ".converted")
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(rgb2hex(item[0], item[1], item[2]))
            if digit == None:
                pass
            else:
                binary += str(digit)
                if (binary[-16:] == '1111111111111110'):
                    print("Message retrived, it was\n" + bin2str(binary[:-16]))
                    return bin2str(binary[:-16])
        print("Message retrived, it was\n" + bin2str(binary))
        return bin2str(binary)
    print("Incorrect image mode. Message not retrieved.")
    return None

def main():
    mode = input("'hide' or 'retrieve' image?\n> ")
    path = input("What is the image path?\n> ")
    if mode == 'hide':
        message = input("What message would you like to hide?\n> ")
        hide(path, message)
    elif mode == 'retrieve':
        retr(path)

if __name__ == '__main__':
    main()
