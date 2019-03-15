#!/usr/bin/python
# -*- coding:utf-8 -*-
# from sqlalchemy import select, create_engine, Table, Column, INT, String, FLOAT, TEXT, DATE, DATETIME, MetaData
#
# metadata = MetaData()
# loan = Table('loan', metadata,
#              Column('loanId', INT, primary_key=True, unique=True),
#              Column('userId', INT),
#              Column('title', TEXT),
#              Column('amount', INT),
#              Column('interest', FLOAT),
#              Column('months', INT),
#              Column('readyTime', DATE),
#              Column('interestPerShare', FLOAT),
#              Column('creditLevel', String(8)),
#              Column('repayType', INT),
#              Column('repaySource', TEXT),
#              Column('leftMonths', INT),
#              Column('status', TEXT),
#              )
# borrower = Table('borrower', metadata,
#                  Column('userId', INT, primary_key=True, unique=True),
#                  Column('nickName', TEXT),
#                  Column('realName', TEXT),
#                  Column('idNo', TEXT),
#                  Column('gender', String(8)),
#                  Column('mobile', TEXT),
#                  Column('birthDay', DATE),
#                  Column('graduation', TEXT),
#                  Column('marriage', TEXT),
#                  Column('salary', TEXT),
#                  Column('hasHouse', INT),
#                  Column('hasCar', INT),
#                  Column('houseLoan', TEXT),
#                  Column('carLoan', TEXT),
#                  Column('officeDomain', TEXT),
#                  Column('city', TEXT),
#                  Column('workYears', TEXT),
#                  Column('auditItems', TEXT),
#                  Column('totalCount', INT),
#                  Column('successCount', INT),
#                  Column('alreadyPayCount', INT),
#                  Column('borrowAmount', INT),
#                  Column('notPayPrinciple', INT),
#                  Column('notPayTotalAmount', INT),
#                  Column('overdueAmount', INT),
#                  Column('overdueCount', INT),
#                  Column('overdueTotalAmount', INT),
#                  )
# investment = Table('investment', metadata,
#                    Column('loanId', INT, primary_key=True),
#                    Column('userId', INT),
#                    Column('userNickName', TEXT),
#                    Column('amount', INT),
#                    Column('lendTime', DATETIME),
#                    )
# repayment = Table('loanrepayment', metadata,
#                   Column('loanId', INT, primary_key=True),
#                   Column('repayTime', DATE),
#                   Column('repayType', TEXT),
#                   Column('unRepaidAmount', FLOAT),
#                   Column('repaidFee', FLOAT),
#                   Column('actualRepayTime', TEXT),
#                   )
from sqlalchemy import Column, Date, DateTime, Float, String, Text, create_engine
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata


class Borrower(Base):
    __tablename__ = 'borrower'

    userId = Column(INTEGER(11), primary_key=True, unique=True)
    nickName = Column(Text)
    realName = Column(Text)
    idNo = Column(Text)
    gender = Column(String(8))
    mobile = Column(Text)
    birthDay = Column(Date)
    graduation = Column(Text)
    marriage = Column(Text)
    salary = Column(Text)
    hasHouse = Column(INTEGER(11))
    hasCar = Column(INTEGER(11))
    houseLoan = Column(Text)
    carLoan = Column(Text)
    officeDomain = Column(Text)
    city = Column(Text)
    workYears = Column(Text)
    auditItems = Column(Text)
    totalCount = Column(INTEGER(11))
    successCount = Column(INTEGER(11))
    alreadyPayCount = Column(INTEGER(11))
    borrowAmount = Column(INTEGER(11))
    notPayPrincipal = Column(INTEGER(11))
    notPayTotalAmount = Column(INTEGER(11))
    overdueAmount = Column(INTEGER(11))
    overdueCount = Column(INTEGER(11))
    overdueTotalAmount = Column(INTEGER(11))


class Investment(Base):
    __tablename__ = 'investment'

    loanId = Column(INTEGER(11), primary_key=True)
    userId = Column(INTEGER(11))
    userNickName = Column(Text)
    amount = Column(INTEGER(11))
    lendTime = Column(DateTime)


class Loan(Base):
    __tablename__ = 'loan'

    loanId = Column(INTEGER(11), primary_key=True, unique=True)
    userId = Column(INTEGER(11))
    title = Column(Text)
    amount = Column(INTEGER(11))
    interest = Column(Float)
    months = Column(INTEGER(11))
    readyTime = Column(Date)
    interestPerShare = Column(Float)
    creditLevel = Column(String(8))
    repayType = Column(INTEGER(11))
    repaySource = Column(Text)
    leftMonths = Column(INTEGER(11))
    status = Column(Text)


class Loanrepayment(Base):
    __tablename__ = 'loanrepayment'

    loanId = Column(INTEGER(11), primary_key=True)
    repayTime = Column(Date)
    repayType = Column(Text)
    unRepaidAmount = Column(Float)
    repaidFee = Column(Float)
    actualRepayTime = Column(Text)


class DBWorker:
    engine = create_engine("mysql+pymysql://%s:%s:%s/%s" % ("root", "Lh201903@rm-uf68k89dyx2957tf62o.mysql.rds.aliyuncs.com", "3306", "rrd"))
    DBsession = sessionmaker(bind=engine)

    def get_session(self):
        return self.DBsession()

    def insert(self, table):
        session = self.get_session()
        session.add(table)
        session.commit()
        session.close()

    def insert_all(self, tables):
        session = self.get_session()
        session.add_all(tables)
        session.commit()
        session.close()
