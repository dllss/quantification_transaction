import tushare as ts
import pandas as pd
import os
import time

"""
获取历史数据
"""
"""
Tushare是一个大数据开放社区, 免费提供各类金融数据和区块链数据, 助力智能投资与创新型投资。
1.首先进入Tushare官网: Tushare官网。
2.在Tushare官网注册并登录。
3.登陆后进入个人主页, 在个人主页的接口TOKEN栏里就是你的token。
"""
tushareToken = '9f35cf890004d38d14677fc73bacc74deb0b96f24c62cb15a2b76d90'
ts.set_token(tushareToken)
ts.set_token(tushareToken)
save_path = '.'
pro = ts.pro_api()


def getNormalData():
    # 获取基础信息数据, 包括股票代码、名称、上市日期、退市日期等
    pool = pro.stock_basic(
        exchange='',
        list_status='L',
        adj='qfq',
        fields='ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs',
    )
    # print(pool.head())

    # 因为穷没开通创业板和科创板权限, 这里只考虑主板和中心板
    pool = pool[pool['market'].isin(['主板', '中小板'])].reset_index()
    pool.to_csv(
        os.path.join(save_path, 'company_info.csv'), index=False, encoding='ANSI'
    )

    print('获得上市股票总数：', len(pool) - 1)
    for j, i in enumerate(pool.ts_code, start=1):
        print('正在获取第%d家, 股票代码%s.' % (j, i))
        path = os.path.join(save_path, 'OldData', i + '_NormalData.csv')
        # 跳过已经生成的文件
        if os.path.exists(path):
            continue
        # 接口限制访问200次/分钟, 加一点微小的延时防止被ban
        time.sleep(0.301)
        df = pro.daily(
            ts_code=i,
            start_date=startDate,
            end_date=endDate,
            fields='ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount',
        )
        df = df.sort_values('trade_date', ascending=True)
        df.to_csv(path, index=False)


def getIndexData():
    # 上交所指数信息
    df = pro.index_basic(market='SSE')
    df.to_csv(os.path.join(save_path, 'SSE.csv'), index=False, encoding='ANSI')

    # 深交所指数信息
    df = pro.index_basic(market='SZSE')
    df.to_csv(os.path.join(save_path, 'SZSE.csv'), index=False, encoding='ANSI')

    # 获取指数历史信息
    # 这里获取几个重要的指数 【上证综指, 上证50, 上证A指, 深证成指, 深证300, 中小300, 创业300, 中小板综, 创业板综】
    index = [
        '000001.SH',
        '000016.SH',
        '000002.SH',
        '399001.SZ',
        '399007.SZ',
        '399008.SZ',
        '399012.SZ',
        '399101.SZ',
        '399102.SZ',
    ]
    for i in index:
        path = os.path.join(save_path, 'OldData', i + '_NormalData.csv')
        df = pro.index_daily(
            ts_code=i,
            start_date=startDate,
            end_date=endDate,
            fields='ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, '
            'vol, amount',
        )
        df = df.sort_values('trade_date', ascending=True)
        df.to_csv(path, index=False)


if __name__ == '__main__':
    # 设置起始日期
    startDate = '20120101'
    endDate = '20191226'
    # 主程序
    getNormalData()
    getIndexData()
