from Crypto.Cipher import DES3
# from Crypto import Random


def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)

    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write(des3.decrypt(chunk))

# make a file selection option
fileName = input("filename: ")
length = len(fileName)
fileType = fileName[(length - 9): (length-4)]
if fileType == ".docx":
    fileDec = fileName[0:(length - 9)] + "DEC" + ".docx"
else:
    fileDec = fileName + ".dec"
# fileName += ".enc"
key = input("key: ")

while len(key) < 16:
    key += '0'
iv = input("IV: ")

# with open(fileName, 'rb') as f:
   # print('fileName: %s' % f.read())
decrypt_file(fileName, fileDec, 8192, key, iv)
# with open(fileDec, 'rb') as f:
    # print('fileDec: %s' % f.read())
print("Decrypt Complete!")
print("File created: " + fileDec)