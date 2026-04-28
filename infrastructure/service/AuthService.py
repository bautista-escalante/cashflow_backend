from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
security = HTTPBearer()

class AuthService:

    @staticmethod
    def generar_token(user_id: int):

        return encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(hours=2)
            },
            os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM")
        )

    @staticmethod
    def validar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            token = credentials.credentials
            
            return decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=[os.getenv("ALGORITHM")]
            )
            
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")

        except InvalidTokenError:
            raise HTTPException(status_code=400, detail="Token inválido")
        