# __author: Lambert
# __date: 2017/9/6 14:49
from core import login
from core import db_handler
from core import logger

user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None

}

acc_logger = logger.log('access')

trans_logger = logger.log('transactions')



# 账户信息接口
def acc_info(user_data):
    data = user_data['account_data']
    info = '''
    \033[32;1m账户: %s,
    信贷额度: %s,
    余额: %s,
    注册时间: %s,
    过期时间: %s,
    还款日: %s,
    \033[0m''' % (
        data['id'], data['credit'], data['balance'], data['enroll_date'], data['expire_date'], data['pay_day'])
    print(info)
    back_menu(user_data)


# 还款接口
@login.login_required
def repay(user_data):
    debt = user_data['account_data']['credit'] - user_data['account_data']['balance']
    print('当前欠款:%s' % debt)
    debt_flage = False
    while not debt_flage:
        debt_money = int(input('请输入还款金额：>>>'))
        user_data['account_data']['balance'] += debt_money
        debt_status = db_handler.update_data(user_data['account_data'])
        if debt_status:
            # print('还款成功，当前余额%s' % user_data['account_data']['balance'])
            trans_logger.info('用户：%s还款%s元成功' % (user_data['account_id'], debt_money))
            debt_flage = True
            back_menu(user_data)
        else:
            acc_logger.error('用户：%s还款失败，服务器错误' % user_data['account_id'])


# 取款接口
def withdraw(user_data):
    draw_flage = False
    while not draw_flage:
        draw_money = int(input('输入取款金额>>>'))
        service_charge = draw_money * 1.05
        balance = user_data['account_data']['balance']
        if draw_money < balance + service_charge:
            user_data['account_data']['balance'] = balance - draw_money - service_charge
            db_handler.update_data(user_data['account_data'])
            trans_logger.info('用户：%s提现成功手续费%s！' % (user_data['account_id'], service_charge - draw_money))
            back_menu(user_data)
        else:
            acc_logger.info('用户：%s提现失败，余额不足' % user_data['account_id'])


# 转账接口
def transfer(user_data):
    id_flag = False
    while not id_flag:
        tran_id = input('请输入转账账户>>>')
        tran_data = db_handler.read_data(tran_id)
        if tran_data:
            balance_flag = False
            while not balance_flag:
                money = int(input('请输入转账金额>>>'))
                balance = user_data['account_data']['balance']
                if money < balance:
                    user_data['account_data']['balance'] = balance - money
                    tran_data['balance'] += money
                    db_handler.update_data(user_data['account_data'])
                    db_handler.update_data(tran_data)
                    trans_logger.info('用户：%s转账%s成功,金额%s！' % (user_data['account_id'], tran_data['id'], money))
                    back_menu(user_data)
                else:
                    acc_logger.warn('用户：%s 转账失败，余额不足' % user_data['account_id'])


# 账单接口
def pay_check(user_data):
    db_handler.read_log('transactions')
    back_menu(user_data)


# 注销
def logout(user_data):
    acc_logger.info('用户：%s注销' % user_data['account_id'])
    exit()


# 返回菜单
def back_menu(user_data):
    success_menu = '''
    1.返回主菜单
    2.退出
    '''
    succ_flag = False
    while not succ_flag:
        succ_choice = input(success_menu)
        if succ_choice == '1':
            succ_flag = True
            interactive(user_data)
        elif succ_choice == '2':
            succ_flag = True
            logout(user_data)
        else:
            succ_flag = False
            print('\033[31;1mOption does not exist!\033[0m')


# 主菜单
def interactive(user_data):
    menu = u'''
    \033[32;1m1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  账单
    6.  退出
    \033[0m'''
    menu_dic = {
        '1': acc_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout
    }
    exit_flage = False
    while not exit_flage:
        choice = input(menu)
        if choice in menu_dic:
            exit_flage = True
            menu_dic[choice](user_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


# 入口函数
def run():
    acc_data = login.login(user_data, acc_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)
