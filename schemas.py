from pydantic import BaseModel

class SecretCreate(BaseModel):
    secret_text: str
