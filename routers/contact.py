from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from email.message import EmailMessage
import aiosmtplib
import os
import dotenv

dotenv.load_dotenv()

SMTP_CONFIG = {
    "hostname": os.getenv("SMTP_HOSTNAME", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", 465)),
    "username": os.getenv("SMTP_USERNAME", "fac.demarco37@gmail.com"),
    "password": os.getenv("SMTP_PASSWORD", "ifoc prlz usgx mvno"),
    "from_email": os.getenv("SMTP_FROM_EMAIL", "fac.demarco37@gmail.com"),
    "to_email": os.getenv("SMTP_TO_EMAIL", "fac.demarco37@gmail.com"),
    "start_tls": True,
    "use_tls": False,
}

router = APIRouter()

class ContactForm(BaseModel):
    name: str = Field(..., description="Nombre de la persona que envía el mensaje")
    email: EmailStr = Field(..., description="Correo de la persona que envía el mensaje")
    telefono: str = Field(..., description="Telefono de la persona que envía el mensaje")
    m2: str = Field(..., description="Metros cuadrados a construir")
    message: str = Field(..., description="Mensaje de la persona")

@router.post("/send-email", status_code=status.HTTP_201_CREATED)
async def send_email(contact: ContactForm):
    email = EmailMessage()
    email["From"] = SMTP_CONFIG["from_email"]
    email["To"] = SMTP_CONFIG["to_email"]
    telefono = contact.telefono.replace(" ", "")
    m2 = contact.m2.replace(" ", "")
    email["Subject"] = f"Mensaje desde la web de: {contact.name}"
    email.set_content(
        f"Nombre: {contact.name}\n"
        f"Email: {contact.email}\n\n"
        f"Telefono: {telefono}\n\n"
        f"M2: {m2}\n\n"
        f"Mensaje:\n{contact.message}"
    )

    try:
        await aiosmtplib.send(
            email,
            hostname=SMTP_CONFIG["hostname"],
            port=SMTP_CONFIG["port"],
            username=SMTP_CONFIG["username"],
            password=SMTP_CONFIG["password"],
            use_tls=True
        )
        return JSONResponse(content={"message": "Email enviado con éxito"})
    except Exception as e:
        return JSONResponse(content={"message": f"Error al enviar el correo. Intente más tarde. {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)