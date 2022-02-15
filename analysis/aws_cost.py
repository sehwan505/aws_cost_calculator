from config.settings import DATA_DIRS
from config.settings import REPORT_DIRS
from analysis import AWS_cost_calculate

import os
import sys
import pandas as pd
import numpy as np
import datetime
import boto3

class AWS_Cost:
    '''
    cost explorer api를 이용해서 account의 cost를 시작일 부터 종료일까지 불러와서 저장
    '''
    def get_AWS_cost_report(self, file_no_list, start_date, end_date):

        print(start_date, end_date)
        # 파일 읽어들이기
        try:
            os.chdir(sys._MEIPASS)
            print(sys._MEIPASS)
        except:
            os.chdir(os.getcwd())
        f = pd.DataFrame()
        for i in range(1,5):
            temp = pd.read_csv(DATA_DIRS[0]+"\\aws_account_" + str(i) +".csv", sep=",", dtype={'Account_ID': 'str'})
            f = pd.concat([f,temp], ignore_index=True)
        print(f)
        print("파일을 조회합니다.")
        print(file_no_list)
        condition = f["Root Account"].apply(lambda x: int(x[2:5]) in file_no_list)
        access_data = f.loc[condition, ["Root Account","Access_ID", "Secret_Access_Key", "Region", "Account_ID"]]
        print(access_data)
        # 요청에 사용할 데이터 리스트화
        access_id = access_data['Access_ID'].values.tolist()
        secret_access_key = access_data['Secret_Access_Key'].values.tolist()
        region = access_data['Region'].values.tolist()
        account_id = access_data['Account_ID'].values.tolist()
        account_id = list(map(str, account_id))
        root_account = f['Root Account'].values.tolist()

        # API 요청 전송
        print("요청을 전송합니다. 잠시만 기다려 주세요..")
        total_list = []

        for i in range(0, len(account_id)):
            print(i, account_id[i])
            client = boto3.client('ce',
                                  aws_access_key_id=access_id[i],
                                  aws_secret_access_key=secret_access_key[i],
                                  region_name=region[i])
            response = client.get_cost_and_usage(
                TimePeriod={
                    "Start": start_date.strftime("%Y-%m-%d"),
                    "End": end_date.strftime("%Y-%m-%d")
                },
                Granularity="DAILY",
                Filter={
                    "Dimensions": {
                        "Key": "LINKED_ACCOUNT",
                        "Values": [account_id[i]]
                    }
                },
                GroupBy=[
                    {
                        "Type": "DIMENSION",
                        "Key": "REGION"
                    }
                ],
                Metrics=["BlendedCost"])

            # print(response)
            resultdata = response['ResultsByTime']
            date = []
            total = []

            # 응답받은 데이터 파싱
            for i in range(0, len(resultdata)):
                timedata = resultdata[i]['TimePeriod']
                date.append(timedata['Start'])
                Groups = resultdata[i]['Groups']
                cost_of_aday_list = []
                for j in range(0, len(Groups)):
                    Keys = Groups[j]['Keys']
                    Cost = Groups[j]['Metrics']['BlendedCost']['Amount']
                    cost_of_aday_list.append(float(Cost))
                cost_per_day = np.array(cost_of_aday_list)
                cost_per_day_sum = sum(cost_per_day)
                total.append(cost_per_day_sum)
            total_list.append(total)

        # 리스트를 데이터프레임으로 변환
        df = pd.DataFrame.from_records(total_list, columns=date, index=access_data["Root Account"])
        # 데이터프레임을 csv 파일로 저장
        basename = REPORT_DIRS[0]+"\\aws_cost_report"
        suffix = str(start_date.month) +".csv"
        filename = "_".join([basename, suffix])
        df.to_csv(filename, sep=',', na_rep='NaN')
        print("요청 결과를 " + filename + " 파일로 저장했습니다.")
        file_name = "aws_cost_report_"+ suffix
        print(file_name)
        # 파일 이름 넣어서 calculate 함수 호출
        result, month_list, sum_result = AWS_cost_calculate.AWS_Calculate().aws_cost_calculate(file_no_list, start_date, end_date)
        return result, month_list, sum_result

if __name__ == '__main__':
    result = AWS_Cost().get_AWS_cost_report('300', '2021-06-01', '2021-07-01');
    print(result);