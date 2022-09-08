 # for i in importantIndexArr:
    #     path = os.path.join(save_path, oldDataFolderName, i + '_NormalData.csv')
    #     df = proApi.index_daily(
    #         ts_code=i,
    #         start_date=startDate,
    #         end_date=endDate,
    #         fields='ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount',
    #     )
    #     df = df.sort_values('trade_date', ascending=True)
    #     df.to_csv(path, index=F