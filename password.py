
import hashlib

def encryption(password):
    return hashlib.sha256(password.encode()).hexdigest() 

print(encryption('Appu@1232'))