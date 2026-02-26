from jwt_utils import decode_token
from rest_framework import status
from rest_framework.response import Response

class JWTAuthGeneric:
    #this class to be called for every views function instead of mulitple calls calling this once will ensure proper jwt authentication
    def dispatch(self,request,*args, **kwargs):
        auth_header = request.headers.get("Authorization","")
        if not auth_header.startswith("Bearer "): # token is to be given in format "Bearer: encrpted stuff"
            return Response({"error":"Improper token format expected Bearer initially"},status=status.HTTP_401_UNAUTHORIZED)
        
        actual_token = auth_header.split(" ",1)[1] #gets the second item which is the token
        try:
            payload = decode_token(actual_token) #calling the cutom decoding function
        except ValueError as e:
            return Response({"error":str(e)},status=status.HTTP_401_UNAUTHORIZED)
        #automatic fucntion which is called before every get post etc requests before that we needed to authorize 
        return super().dispatch(request,*args,**kwargs) #later calls the actual dispatch method after authorization