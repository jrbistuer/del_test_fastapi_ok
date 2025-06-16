from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# mysql+pymysql://test:test@localhost:3306/primerapi
# mysql://avnadmin:AVNS_kM-WueW1pmjX-l6YWRt@mysql-3e797e5d-jrbistuer-1949.e.aivencloud.com:14718/defaultdb?ssl-mode=REQUIRED
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_kM-WueW1pmjX-l6YWRt@mysql-3e797e5d-jrbistuer-1949.e.aivencloud.com:14718/primerapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


""" Service URI
mysql://avnadmin:AVNS_kM-WueW1pmjX-l6YWRt@mysql-3e797e5d-jrbistuer-1949.e.aivencloud.com:14718/defaultdb?ssl-mode=REQUIRED

Database name
defaultdb

Host
mysql-3e797e5d-jrbistuer-1949.e.aivencloud.com

Port
14718

User
avnadmin

Password
AVNS_kM-WueW1pmjX-l6YWRt

SSL mode
REQUIRED

CA certificate
Show """


