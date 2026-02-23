class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@db:3306/beograd_events"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }

    SECRET_KEY = "dev-secret"
    JWT_SECRET_KEY = "jwt-secret"
    MAIL_USERNAME = "beograd.events.app@gmail.com"
    MAIL_PASSWORD = "zqhj wtqp fulh lvze"
    MAIL_HOST = "smtp.gmail.com"
    MAIL_PORT = 587
    
