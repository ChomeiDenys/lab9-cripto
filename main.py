import hashlib

mystring = input('Enter String to hash for md5: ')
#UTF-8
hash_object = hashlib.md5(mystring.encode())
print("Result: " + hash_object.hexdigest())

mystring = input('Enter String to hash for sha1: ')
hash_object = hashlib.sha1(mystring.encode())
print("Result: " + hash_object.hexdigest())

mystring = input('Enter String to hash for sha224: ')
hash_object = hashlib.sha224(mystring.encode())
print("Result: " + hash_object.hexdigest())
