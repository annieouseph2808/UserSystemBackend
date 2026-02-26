import hmac
import hashlib
import base64
import json
import time
from django.conf import settings

#encoding and decoding the data functions
def base64url_encode(data:bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def base64url_decode(data:str)->bytes:
    padding = 4 -len(data)%4 #base64 strings must br multiples of 4
    if padding !=4:
        data+="="*padding #adding = to make it multiple of 4
    return base64.urlsafe_b64decode(data)



#signing - creats the signature using the payload and header
def _sign(header:str,payload:str)->str:
    secret = settings.JWT_SECRET.encode("utf-8") #fetches the secret from the settings.py
    message = f"{header}.{payload}".encode("utf-8") #encodes the payload_message returning bytes
    signature = hmac.new(secret,message,hashlib.sha256).digest() #creates signature using header+payload with the secret using any encryption algorithm--here sha256
    return base64url_encode(signature) # the signature is then encoded


#using header+payload+signature => create token
#token generation function
def generate_token(payload: dict) -> str:
    header = {
        "alg":settings.JWT_ALGORITHM,
        "typ":"JWT"
    }
    encoded_header = base64url_encode(json.dumps(header,separators=(",",":")).encode())

    payload = payload.copy()
    payload["exp"] = int(time.time())+(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES*60) #adding expiry
    payload["iat"] = int(time.time()) #adding the issued at time

    encoded_payload = base64url_encode(json.dumps(payload,separators=(",",":")).encode())

    signature = _sign(encoded_header,encoded_payload)

    return f"{encoded_header}.{encoded_payload}.{signature}" # token format header payload signature


#Decoding the generated token functions
def decode_token(token:str)->dict:
    try:
        encoded_header, encoded_payload, provided_signature = token.split(".") #token is splited to get header payload etc
    except ValueError:
        raise ValueError("Invalid token format")
    expected_signature = _sign(encoded_header,encoded_payload) #using the header payload expected signature is calculated

    if not hmac.compare_digest(expected_signature,provided_signature): # signatures are compared verified
        raise ValueError("Authentication Error: Invalid Signature provided")
    
    #decoding the payload to get the exp , data and issuedAt
    try:
        payload = json.loads(base64url_decode(encoded_payload)) # this will have user info, expiry and issueAt
    except Exception:
        raise ValueError("Decoding Payload Failed")
    #checks for expiry date
    if "exp" not in payload:
        raise ValueError("Token has no expiry claim")
    #if expired check compared to now()
    if time.time()>payload["exp"]:
        raise ValueError("Token Expired")
    
    return payload # retuens the payload from which the user_id can be obtained 