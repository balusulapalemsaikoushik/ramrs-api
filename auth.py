from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, PyJWKClient, PyJWKClientError
import jwt

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Auth0JWTBearerTokenValidator:
    def __init__(self):
        self.issuer = settings.ISSUER
        self.audience = settings.AUDIENCE
        self.algorithm = settings.ALGORITHMS[0]
        jwks_uri = f"{self.issuer}.well-known/jwks.json"
        self.jwks_client = PyJWKClient(jwks_uri, lifespan=3600)
    
    def validate(self, token: str):
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
            payload = jwt.decode(
                jwt=token,
                key=signing_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )
            return payload
        except PyJWKClientError as e:
            raise HTTPException(status_code=500, detail="Error fetching signing keys.")
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials.")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Authentication error.")

auth0_validator = Auth0JWTBearerTokenValidator()

def validate_token(token: str = Depends(oauth2_scheme)) -> dict:
    return auth0_validator.validate(token)

def has_scope(claims: dict, required_scope: str):
    if claims.get("scope"):
        for scope in claims["scope"].split():
            if scope == required_scope:
                return True
    return False
