import pandas as pd
from config.settings import REPORT_DIRS
import math
import datetime


class AWS_Calculate:
    '''
    month를 기준으로 월별로 분류, 환율 적용
    '''
    def aws_cost_separate_by_month(this, start_month, end_month, aws_cost):
        aws_cost.columns = aws_cost.columns.str[5:] #2021-07-01에서 2021버리기
        if (start_month == end_month):
            month_list = [start_month]
            aws_cost.insert(0, "total", aws_cost.iloc[:, :].sum(axis=1))
            for i in range(0, len(aws_cost)):
                aws_cost.iloc[i, :] = aws_cost.iloc[i, :] * 1150
            for i in range(0, len(aws_cost.columns)):
                aws_cost.iloc[:, i] = aws_cost.iloc[:, i].apply(lambda x: math.ceil(x))
            result = [aws_cost]
        else:
            month_list = range(int(start_month), int(end_month) + 1)
            result = []
            for idx, month in enumerate(month_list):
                result.append(aws_cost.loc[:,  aws_cost.columns.str[:2] == f"{month:>02}"])
                result[idx].insert(0, "total", result[idx].iloc[:, :].sum(axis=1))
                for i in range(0, len(aws_cost)):
                    result[idx].iloc[i, :] = result[idx].iloc[i, :] * 1150
                for i in range(0, len(result[idx].columns)):
                    result[idx].iloc[:, i] = result[idx].iloc[:, i].apply(lambda x: int(str(x).split(".")[0]))
                result[idx].style.set_table_styles([
                    {'selector': 'table', 'props': 'overflow: scroll; border: 0px;'},
                    {'selector': 'td', 'props': 'text-align:center;'},
                ])
        sum_result = [i.iloc[:, 1:].values.sum() for i in result]
        return result, month_list, sum_result

    '''
    day를 기준으로 월별로 분류, 환율 적용
    '''
    def aws_cost_separate_by_day(this, start_date, end_date, aws_cost):
        if (start_date == end_date):
            month_list = [start_date.month]
            aws_cost = aws_cost.loc[:, aws_cost.columns.str == start_date.strftime("%Y-%m-%d")]
            aws_cost.columns = aws_cost.columns.str[5:] #2021-07-01에서 2021버리기
            aws_cost.insert(0, "total", aws_cost.iloc[:, :].sum(axis=1))
            for i in range(0, len(aws_cost)):
                aws_cost.iloc[i, :] = aws_cost.iloc[i, :] * 1150
            for i in range(0, len(aws_cost.columns)):
                aws_cost.iloc[:, i] = aws_cost.iloc[:, i].apply(lambda x: math.ceil(x))
            result = [aws_cost]
        else:
            month_list = range(int(start_date.month), int(end_date.month) + 1)
            date_list = pd.date_range(start=start_date.strftime("%Y-%m-%d"),end=end_date.strftime("%Y-%m-%d")).strftime("%Y-%m-%d").tolist()
            aws_cost = aws_cost.loc[:, aws_cost.columns.isin(date_list)]
            aws_cost.columns = aws_cost.columns.str[5:] #2021-07-01에서 2021버리기
            result = []
            for idx, month in enumerate(month_list):
                result.append(aws_cost.loc[:,  aws_cost.columns.str[:2] == f"{month:>02}"])
                result[idx].insert(0, "total", result[idx].iloc[:, :].sum(axis=1))
                for i in range(0, len(aws_cost)):
                    result[idx].iloc[i, :] = result[idx].iloc[i, :] * 1150
                for i in range(0, len(result[idx].columns)):
                    result[idx].iloc[:, i] = result[idx].iloc[:, i].apply(lambda x: int(str(x).split(".")[0]))
                result[idx].style.set_table_styles([
                    {'selector': 'table', 'props': 'overflow: scroll; border: 0px;'},
                    {'selector': 'td', 'props': 'text-align:center;'},
                ])
        sum_result = [i.iloc[:, 1:].values.sum() for i in result]
        return result, month_list, sum_result

    '''
    원하는 ID_no와 시작일 종료일을 받아서 ID별로 합계을 구하는 함수
    '''
    def aws_cost_calculate(self, file_no_list, start_date, end_date, contain_day=False):
        start_month = start_date.month
        end_month = end_date.month
        # csv 파일 불러오기
        aws_cost = pd.DataFrame()
        if (start_month == end_month):
            aws_cost = pd.read_csv(REPORT_DIRS[0] + '\\' + "aws_cost_report_" +str(start_month) + ".csv")
        else:
            for month in range(start_month, end_month + 1):
                temp = pd.read_csv(REPORT_DIRS[0] + '\\' + "aws_cost_report_" +str(month) + ".csv")
                if (month != start_month):
                    temp = temp.drop(["Root Account"], axis=1)
                aws_cost = pd.concat([aws_cost, temp], axis=1)

        #받아온 file_no_list에 속해있는 row만 사용
        aws_cost["Root Account"] = aws_cost["Root Account"].apply(lambda x: str(x).split("@")[0])
        condition = aws_cost["Root Account"].apply(lambda x: int(x[2:]) in file_no_list)
        aws_cost = aws_cost.loc[condition, :]
        aws_cost.set_index("Root Account", inplace=True)
        # 받은 데이터를 월에 따라 분할하고 가독성있도록 변환
        if (contain_day):
            return (self.aws_cost_separate_by_day(start_date, end_date, aws_cost))
        else:
            return (self.aws_cost_separate_by_month(start_month, end_month, aws_cost))

if __name__ == '__main__':
    result = AWS_Calculate().aws_cost_calculate('aws_cost_report_210727_093838.csv')