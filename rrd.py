#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import http.cookiejar
import json
import time

import requests
import re

from rd import r
from db import Borrower, Investment, Loan, Loanrepayment, DBWorker, Transfer
from users import user
from captcha import header_captcha


class Spider:
    url = 'https://renrendai.com/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    session = requests.session()
    dbWorker = DBWorker()

    def __init__(self):
        self.__make_sure_login()

    @staticmethod
    def parse_ids(ids) -> [str]:
        return [str(each) for each in ids]

    def get_html(self, base_url: str = url, header=None) -> requests.Response:
        if header is None:
            header = self.header
        return self.session.get(base_url, headers=header, timeout=30)

    def post_html(self, url, data=None, header=None):
        if header is None:
            header = self.header
        return self.session.post(url, headers=header, data=data)

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
        try:
            ready_time = time.localtime(int(loan['readyTime'] / 1000))
        except:
            ready_time = None
        loan_data = Loan(
            loanId=loan['loanId'],
            userId=user['userId'],
            title=loan['title'],
            amount=loan['amount'],
            interest=loan['interest'],
            months=loan['months'],
            readyTime=ready_time,
            interestPerShare=loan['interestPerShare'],
            creditLevel=user['creditLevel'],
            repayType=loan['repayType'],
            repaySource=result['repaySource'],
            leftMonths=loan['leftMonths'],
            status=loan['status'],
        )
        try:
            if self.dbWorker.search(Loan.loanId == loan['loanId']):
                return -1
        except:
            return -1
        self.dbWorker.insert(loan_data)
        borrower = []
        try:
            borrower.append(str(user['userId']))
            if self.dbWorker.search(Borrower.userId == user['userId']):
                return
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
        while True:
            response = self.get_html('https://renrendai.com/transfer/detail/loanInvestment?loanId=' + loan_id)
            if response.status_code != 200:
                # {"status":1001,"message":"用户未登录, 或者登录状态已过期"}
                print(response.status_code)
                return
            res = json.loads(response.content.decode())
            if res['status'] != 0:
                if res['status'] == 1001:
                    self.__make_sure_login()
                    continue
                else:
                    print(res)
                    exit(2)
            self.step2_save(res)
            return

    def step2_save(self, result):
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
        while True:
            response = self.get_html('https://renrendai.com/transfer/detail/loanTransferred?loanId=' + loan_id)
            if response.status_code != 200:
                print(response.status_code)
                return
            res = json.loads(response.content.decode())
            if res['status'] != 0:
                if res['status'] == 1001:
                    self.__make_sure_login()
                    continue
                else:
                    print(res)
                    exit(3)
            self.step3_save(loan_id, res)
            return

    def step3_save(self, loan_id, result):
        if result['status'] != 0:
            print(result['message'])
            exit(3)
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

    def step4(self, loan_id):
        while True:
            html = self.get_html('https://renrendai.com/transfer/detail/loanRepayment?loanId=%s' % loan_id)
            if html.status_code != 200:
                print(html.status_code)
                return
            res = json.loads(html.content.decode())
            if res['status'] != 0:
                if res['status'] == 1001:
                    self.__make_sure_login()
                    continue
                else:
                    print(res)
                    exit(4)
            self.step4_save(loan_id, res)
            return

    def step4_save(self, loan_id, result):
        transfers = []
        for each in result['data']['list']:
            transfers.append(Transfer(
                transfer_id=int(each['transferId']),
                loanId=loan_id,
                toUserId=each['toUserId'],
                fromUserId=each['fromUserId'],
                price=float(each['price']),
                createTime=time.localtime(int(each['createTime']/1000)),
            ))
        self.dbWorker.insert_all(transfers)

    def run(self):
        while True:
            each = r.spop('yet')
            # each = r.rpop('old')
            if not each:
                print('done')
                return
                # print('sleep for 2h')
                # time.sleep(2*60*60)
                # continue
            else:
                each = each.decode()
            print(each)
            if self.step1('loan-' + each + '.html') == -1:
                continue
            self.step2(each)
            self.step3(each)
            r.sadd('done', int(each))
            # r.zadd('old-done', {each: int(each)})
            time.sleep(1)

    def __make_sure_login(self):
        login = self.post_html(url='https://renrendai.com/p2p/bond/isShowBondOffDialog').json()
        if login['message'] == 'not login':
            print('log in failed')
            self.__login()
            self.__make_sure_login()
        else:
            print('log in success')

    def __login(self):
        html = self.get_html('https://renrendai.com/passport/index/captcha')
        base64_data = base64.b64encode(html.content)
        captcha = 'data:image/jpeg;base64,' + base64_data.decode()
        data_captcha = {
            'v_pic': captcha,
            'v_type': 'n4',
        }
        res = requests.post('http://apigateway.jianjiaoshuju.com/api/v_1/yzm.html', headers=header_captcha, data=data_captcha)
        if res.json()['errCode'] != 0:
            print(res.json())
            exit(1)
        data = {
            'j_username': user['username'],
            'j_password': user['password'],
            'j_code': res.json()['v_code'],
            'rememberme': 'on',
            'targetUrl': '',
            'returnUrl': '/user/account/p2p/index',
        }
        h = self.post_html(url='https://renrendai.com/passport/index/doLogin', data=data)
        res = h.json()
        if res['status'] == 0:
            return
        else:
            print(res['message'])


if __name__ == '__main__':
    spider = Spider()
    while True:
        loanid = r.spop('old-transfer')
        if not loanid:
            print('done')
            break
        spider.step4(loanid.decode())
        r.sadd('old-transfer-done', int(loanid))
        print(loanid)
        time.sleep(1)
