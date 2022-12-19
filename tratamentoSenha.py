import hashlib

def codificando(senha):
    result = hashlib.md5(senha.encode())
    return str(result.hexdigest())