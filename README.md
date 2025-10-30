# Mi Refugio Web

Proyecto universitario orientado a apoyo y educacion emocional en Chile.

Aplicacion Django que respalda la plataforma Mi Refugio, enfocada en acompanamiento y educacion emocional en Chile.

## Requisitos
- Python 3.11+
- PostgreSQL 13+ (se usa AWS RDS en produccion)
- Pipenv o pip

## Variables de entorno
Configura un archivo `.env` en la raiz del proyecto:

```
DEBUG=0
SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=mi-refugio.cl,mi-refugio-web.onrender.com

DB_NAME=mirefugio
DB_USER=usuario_rds
DB_PASS=clave_segura
DB_HOST=tu_endpoint_rds
DB_PORT=5432

RECAPTCHA_SITE_KEY=clave_publica_recaptcha
RECAPTCHA_SECRET=clave_secreta_recaptcha
CONTACT_BYPASS_RECAPTCHA=0

TBK_API_KEY_ID=597055555532
TBK_API_KEY_SECRET=579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
TBK_ENV=integration
TBK_RETURN_URL=https://tu-dominio/donar/retorno/

DONATION_MIN_CLP=500
DB_CONN_MAX_AGE=60
```

## Instalacion local
1. Crear y activar un entorno virtual.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Aplicar migraciones: `python manage.py migrate`
4. Crear un superusuario: `python manage.py createsuperuser`
5. Levantar el servidor: `python manage.py runserver`

## Estatica y despliegue
- Ejecuta `python manage.py collectstatic` antes de desplegar.
- Whitenoise sirve los archivos estaticos en produccion.
- Asegurate de exponer `RECAPTCHA_SITE_KEY` en tu frontend para que el formulario de contacto funcione.

## Notas
- Las donaciones usan Webpay (transbank-sdk). Cambia `TBK_ENV` a `production` y carga tus credenciales reales antes de ponerlo en vivo.
- La app asume una base de datos PostgreSQL con schema `web` en RDS; ajusta `DATABASES["default"]["OPTIONS"]["options"]` si tu esquema es distinto.
