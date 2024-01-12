from jwt import decode

def verify(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return False
    try:
        payload = decode(token,'secret',algorithms = ['HS256'])
    except :
        return False
    if payload:
        return True