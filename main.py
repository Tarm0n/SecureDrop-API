from fastapi import FastAPI, Depends, HTTPException, responses, BackgroundTasks
from schemas import SecretCreate
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from crypto import encrypt_secret, decrypt_secret
import models, secrets
import datetime


#create all tables in models
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "SecureDrop API",
    description = "A secure, one-time secret sharing API",
    version = "1.0.0"
)


@app.get("/")
def root():
    return responses.RedirectResponse(url="/docs")


def delete_entry():
    db = SessionLocal()
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        db.query(models.Secret).filter(models.Secret.expires_at < now).delete()
        db.commit()
    finally:
        db.close()


# session manager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/secrets/")
def create_secret(secret: SecretCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    key = secrets.token_urlsafe(16)

    encrypted = encrypt_secret(secret.secret_text)

    # create new entrys
    secr = models.Secret(secret_key=key, encrypted_data=encrypted, expires_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24))

    # add entry to database and commit
    db.add(secr)
    db.commit()
    db.refresh(secr)

    background_tasks.add_task(delete_entry, db)

    return {"message" : "Secret gespeichert", "link_key" : secr.secret_key}

@app.get("/secrets/{secret_key}")
def get_url(secret_key:str, db:Session = Depends(get_db)):
    db_secret = db.query(models.Secret).filter(models.Secret.secret_key == secret_key).first()

    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    
    decrypted = decrypt_secret(db_secret.encrypted_data)

    db.delete(db_secret)
    db.commit()

    return {"string": decrypted}