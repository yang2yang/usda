# 尝试解析Json串

import json

from sqlalchemy import Column, String, Date, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SpotmarketCda(Base):
    __tablename__ = 'spotmarket_cda'

    commodity = Column(String, primary_key=True)
    location = Column(String, primary_key=True)
    price = Column(Float)
    exportDate = Column(Date, primary_key=True)
    bushelPrice = Column(Float)


engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)
session = Session()



with open('E_MAN.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="E_MAN",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('N_ALTA.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="N_ALTA",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()



with open('NE_SASK.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="NE_SASK",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('NW_SASK.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="NW_SASK",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('PEACE.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="PEACE",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('S_ALTA.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="S_ALTA",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('SE_SASK.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="SE_SASK",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('SW_SASK.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="SW_SASK",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()


with open('W_MAN.json', 'r') as f:
    datadata = json.load(f)

    for i in datadata['data']:
        print("price=" + i["price"])
        print("exportDate=" + i["exportDate"])
        print("bushelPrice=" + i["bushelPrice"])

        p = SpotmarketCda(commodity="CDA_CANOLA",location="W_MAN",price=i["price"],exportDate=i["exportDate"],bushelPrice=i["bushelPrice"])
        session.add(p)
        session.commit()