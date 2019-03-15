#!/usr/bin/python
# -*- coding:utf-8 -*-
import http.cookiejar
import json
import time

import requests
import re

from rd import r
from db import Borrower, Investment, Loan, Loanrepayment, DBWorker


class Spider:
    url = 'https://renrendai.com/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    session = requests.session()
    dbWorker = DBWorker()

    def __init__(self):
        cookies = http.cookiejar.LWPCookieJar()
        # 使用浏览器cookies来导入
        # self.__get_cookie()
        # noinspection PyBroadException
        try:
            cookies.load('cookies', ignore_discard=True, ignore_expires=True)
            self.session.cookies = cookies
            self.__make_sure_login()
        except Exception:
            print('cookies load fail, wait for login...')
            self.__make_sure_login()

    @staticmethod
    def parse_ids(ids) -> [str]:
        return [str(each) for each in ids]

    def get_html(self, base_url: str = url, header=None) -> requests.Response:
        if header is None:
            header = self.header
        return self.session.get(base_url, headers=header, timeout=30)

    def step0(self):
        for i in range(50):
            result = self.get_html('https://renrendai.com/loan/list/loanList?startNum=%s&limit=10' % i)
            if result.status_code == 200:
                response = result.json()
                for each in response['data']['list']:
                    if r.sismember('done', each['loanId']):
                        return
                    r.sadd('yet', each['loanId'])
            time.sleep(1)

    def step1(self, loan_id: str):
        response = self.get_html(base_url='https://renrendai.com/' + loan_id)
        if response.status_code == 302:
            print(302)
            return 302
        elif response.status_code == 200:
            result = re.findall(r"var info = '(.*)';", response.content.decode())
            if not result:
                print('error info')
                return 1
            else:
                res = json.loads(result[0].replace('\\u0022', '"').replace('\\u005C', '\\'))
                self.step1_save(res)
                pass
            return 200
        else:
            print(response.status_code)
            return response.status_code

    def step1_save(self, result):
        loan = result['loan']
        user = result['borrower']
        record = result['userLoanRecord']
        loan_data = Loan(
            loanId=loan['loanId'],
            userId=user['userId'],
            title=loan['title'],
            amount=loan['amount'],
            interest=loan['interest'],
            months=loan['months'],
            readyTime=time.localtime(int(loan['readyTime'] / 1000)),
            interestPerShare=loan['interestPerShare'],
            creditLevel=user['creditLevel'],
            repayType=loan['repayType'],
            repaySource=result['repaySource'],
            leftMonths=loan['leftMonths'],
            status=loan['status'],
        )
        borrower = []
        try:
            borrower.append(str(user['userId']))
        except:
            borrower.append('')
        try:
            borrower.append(user['nickName'])
        except:
            borrower.append('')
        try:
            borrower.append(user['realName'])
        except:
            borrower.append('')
        try:
            borrower.append(user['idNo'])
        except:
            borrower.append('')
        try:
            borrower.append(user['gender'])
        except:
            borrower.append('')
        try:
            borrower.append(user['mobile'])
        except:
            borrower.append('')
        try:
            borrower.append(user['birthDay'])
        except:
            borrower.append('')
        try:
            borrower.append(user['graduation'])
        except:
            borrower.append('')
        try:
            borrower.append(str(user['marriage']))
        except:
            borrower.append('')
        try:
            borrower.append(user['salary'])
        except:
            borrower.append('')
        try:
            borrower.append(str(user['hasHouse']))
        except:
            borrower.append('')
        try:
            borrower.append(str(user['hasCar']))
        except:
            borrower.append('')
        try:
            borrower.append(str(user['houseLoan']))
        except:
            borrower.append('')
        try:
            borrower.append(str(user['carLoan']))
        except:
            borrower.append('')
        try:
            borrower.append(user['officeDomain'])
        except:
            borrower.append('')
        try:
            borrower.append(user['city'])
        except:
            borrower.append('')
        try:
            borrower.append(user['workYears'])
        except:
            borrower.append('')
        try:
            borrower.append(user['auditItems'])
        except:
            borrower.append('')
        try:
            borrower.append(str(record['totalCount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['successCount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['alreadyPayCount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['borrowAmount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['notPayPrincipal']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['notPayTotalAmount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['overdueAmount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['overdueCount']))
        except:
            borrower.append('')
        try:
            borrower.append(str(record['overdueTotalAmount']))
        except:
            borrower.append('')
        self.dbWorker.insert(loan_data)
        borrower_data = Borrower(
            userId=borrower[0],
            nickName=borrower[1],
            realName=borrower[2],
            idNo=borrower[3],
            gender=borrower[4],
            mobile=borrower[5],
            birthDay=borrower[6],
            graduation=borrower[7],
            marriage=borrower[8],
            salary=borrower[9],
            hasHouse=borrower[10],
            hasCar=borrower[11],
            houseLoan=borrower[12],
            carLoan=borrower[13],
            officeDomain=borrower[14],
            city=borrower[15],
            workYears=borrower[16],
            auditItems=borrower[17],
            totalCount=borrower[18],
            successCount=borrower[19],
            alreadyPayCount=borrower[20],
            borrowAmount=borrower[21],
            notPayPrincipal=borrower[22],
            notPayTotalAmount=borrower[23],
            overdueAmount=borrower[24],
            overdueCount=borrower[25],
            overdueTotalAmount=borrower[26],
        )
        self.dbWorker.insert(borrower_data)
        # with open('loan.csv', 'ab+') as f:
        #     # f.write('loanId,userId,title,amount,interest,months,readyTime,interestPerShare,creditLevel,repayType,repaySource,leftMonths,status\n'.encode())
        #     f.write(','.join(loan_data).encode())
        #     f.write('\n'.encode())
        # with open('borrower.csv', 'ab+') as f:
        #     # f.write('userId,nickName,realName,idNo,gender,mobile,birthDay,graduation,marriage,salary,hasHouse,hasCar,houseLoan,carLoan,officeDomain,city,workYears,auditItems\n'.encode())
        #     f.write(','.join(borrower).encode())
        #     f.write('\n'.encode())

    def step2(self, loan_id):
        response = self.get_html('https://renrendai.com/transfer/detail/loanInvestment?loanId=' + loan_id)
        if response.status_code != 200:
            print(response.status_code)
            pass
        else:
            self.step2_save(json.loads(response.content.decode()))
            pass

    def step2_save(self, result):
        if result['status'] != 0:
            print(result['message'])
            return
        # with open('loanInvestment.csv', 'ab+') as f:
        #         #     # f.write('loanId,userId,userNickName,amount,lendTime\n'.encode())
        #         #     for each in result['data']['list']:
        #         #         f.write(','.join([str(each['loanId']), str(each['userId']), each['userNickName'], str(each['amount']), time.strftime('%Y-%m-%d %H:%M', time.localtime(int(each['lendTime'] / 1000)))]).encode())
        #         #         f.write('\n'.encode())
        investments = []
        for each in result['data']['list']:
            investments.append(Investment(
                loanId=each['loanId'],
                userId=each['userId'],
                userNickName=each['userNickName'],
                amount=each['amount'],
                lendTime=time.localtime(int(each['lendTime']/1000)),
            ))
            self.dbWorker.insert_all(investments)

    def step3(self, loan_id):
        response = self.get_html('https://renrendai.com/transfer/detail/loanTransferred?loanId=' + loan_id)
        if response.status_code != 200:
            print(response.status_code)
            pass
        else:
            self.step3_save(loan_id, json.loads(response.content.decode()))
            pass

    def step3_save(self, loan_id, result):
        if result['status'] != 0:
            print(result['message'])
            return
        loanrepayments = []
        for each in result['data']['list']:
            if each['actualRepayTime']:
                temp = time.localtime(int(each['actualRepayTime']/1000))
            else:
                temp = None
            loanrepayments.append(Loanrepayment(
                loanId=int(loan_id),
                repayTime=time.localtime(int(each['repayTime']/1000)),
                repayType=each['repayType'],
                unRepaidAmount=each['unRepaidAmount'],
                repaidFee=each['repaidFee'],
                actualRepayTime=temp,
            ))
        self.dbWorker.insert_all(loanrepayments)
        # with open('loanTransferred.csv', 'ab+') as f:
        #     # f.write('loan_id,repayTime,repayType,unRepaidAmount,repaidFee,actualRepayTime\n'.encode())
        #     for each in result['data']['list']:
        #         temp = [str(loan_id), time.strftime('%Y-%m-%d', time.localtime(int(each['repayTime'] / 1000))), each['repayType'], str(each['unRepaidAmount']), str(each['repaidFee'])]
        #         if each['actualRepayTime']:
        #             temp.append(time.strftime('%Y-%m-%d', time.localtime(int(each['actualRepaidTime'] / 1000))))
        #         else:
        #             temp.append('')
        #         f.write(','.join(temp).encode())
        #         f.write('\n'.encode())

    def run(self, ids):
        while True:
            each = r.spop('yet')
            if not each:
                print('done')
                return
            else:
                each = each.decode()
            print(each)
            self.step1('loan-' + each + '.html')
            self.step2(each)
            self.step3(each)
            r.sadd('done', int(each))
            time.sleep(1)

    def __make_sure_login(self):
        login = self.session.post('https://renrendai.com/p2p/bond/isShowBondOffDialog', headers=self.header).json()
        if login['message'] == 'not login':
            print('log in failed')
            self.__login()
            self.__make_sure_login()
        else:
            print('log in success')

    def __login(self):
        word = input('please log in manually, then type "ok":\n')
        if word == 'ok':
            return
        else:
            self.__login_with_cookie()

    def __login_with_cookie(self):
        word = input('please log in manually and parse cookie, then type "ok":\n')
        if word == 'ok':
            with open('cookie', 'rb+') as f:
                co = json.loads(f.read().decode())
            cookie = {}
            for each in co:
                cookie[each['name']] = each['value']
            print(cookie)
            cookies = http.cookiejar.LWPCookieJar()
            requests.utils.cookiejar_from_dict(cookie, cookies)
            cookies.save('cookies', ignore_discard=True, ignore_expires=True)
            self.session.cookies = cookies
            print(self.session.cookies)
            return
        else:
            self.__login_with_cookie()
