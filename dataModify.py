from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()

# connect session to active the action
Session = sessionmaker(bind=engine)
session = Session()


class daydata_cont_cbot(Base):
    __tablename__ = 'daydata_cont_cbot'
    code = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    oi = Column(Integer)
    sp = Column(Float)

month = {"F": 1,"G":2,"H": 3,"J":4,"K": 5,"M":6 ,"N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12}

for row in session.query(daydata_cont_cbot).all():

    if row.code[0:2] == 'BO'or row.code[0:2] == 'SM':
        a = month[row.code[2]]

        ye = row.date.year
        mo = row.date.month
        da = row.date.day

        if a == mo:
            if da < 15:
                wantY = ye
            else:
                wantY = ye + 1
        elif a > mo:
            wantY = ye
        else:
            wantY = ye + 1

        wantY = str(wantY)[2:]

        b = row.code[0:3] + wantY + 'E' + row.code[3:]

        print(b,row.code,row.date)

        row.code = b

        # session.commit()
        # session.commit()
    else:
        a = month[row.code[1]]

        ye = row.date.year
        mo = row.date.month
        da = row.date.day

        if a == mo:
            if da < 15:
                wantY = ye
            else:
                wantY = ye + 1
        elif a > mo:
            wantY = ye
        else:
            wantY = ye + 1

        wantY = str(wantY)[2:]

        b = row.code[0:2] + wantY + 'E' + row.code[2:]

        print(b,row.code,row.date)

        row.code = b

session.commit()

print(len(session.query(daydata_cont_cbot, "code", "date", "open").all()))

# f h k n q u v  x  z
# 1 3 5 7 8 9 10 11 12


