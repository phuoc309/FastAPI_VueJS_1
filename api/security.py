from datetime import datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        # print(payload)
        userid = str(payload.get('userid'))
        try:
            with open(r"C:/Users/Lenovo/PycharmProjects/Otani_intern/fastapi-postgresql-crud/web/src/components/user.txt", "w") as f:
                f.write(userid)
        except Exception as e:
            print(e)

        # print(userid)
        # if payload.get('username') < int(datetime.now()):
        #     raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )