import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from analysis import aws_cost, AWS_cost_calculate
from datetime import date, timedelta
import datetime
from dateutil import relativedelta
# Create your views here.

def home(request):
    return render(request, 'home.html')

'''
main
'''
@csrf_exempt
def cost_report(request):
    file_no = request.POST['file_no']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    #받아온 시작일과 종료일이 month까지만 있는지 day까지 있는 지 확인
    if (len(start_date.split("-")) == 3 and len(end_date.split("-")) == 3):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        contain_day = True
    else:
        start_date, end_date = get_start_end_date(start_date, end_date)
        contain_day = False
        print(start_date, end_date)
    if (start_date == 0):
        return redirect("home")
    #ID를 parsing
    file_no_list = parse_file_no(file_no)
    result, month_list, sum_result = AWS_cost_calculate.AWS_Calculate().aws_cost_calculate(file_no_list, start_date, end_date, contain_day)
    for idx in range(len(month_list)):
        for i in range(0, len(result[idx].columns)):
            result[idx].iloc[:, i] = result[idx].iloc[:, i].apply(lambda x: "{:,}".format(x))
    result_html = [i.to_html(border=1, classes="tables") for i in result]

    return render(request, 'report.html', {'results': zip(result_html, month_list, sum_result)})

'''
이번 달 오늘까지의 값을 불러서 덮어쓰기
'''
def look_up(request):
    file_no_list = [100,101,102,103,104,105,106,107,108,109,200,201,202,203,204,205,206,207,208,209,300,301,302,303,304,305,306,307,400,401,402,403,404,405,406]

    # start_date, end_date = datetime.datetime.strptime("2021-08-01", "%Y-%m-%d").date(), datetime.datetime.strptime("2021-09-01", "%Y-%m-%d").date()
    start_date, end_date = date.today().replace(day=1), date.today() + relativedelta.relativedelta(days=1)
    result, month_list, sum_result = aws_cost.AWS_Cost().get_AWS_cost_report(file_no_list, start_date, end_date)
    for idx in range(len(month_list)):
        for i in range(0, len(result[idx].columns)):
            result[idx].iloc[:, i] = result[idx].iloc[:, i].apply(lambda x: "{:,}".format(x))
    result_html = [i.to_html(border=1, classes="tables") for i in result]
    return render(request, 'report.html', {'results':zip(result_html, month_list, sum_result)})

'''
주어진 file_no를 parsing
'''
def parse_file_no(file_no):
    result = []

    if (file_no == '*'):
        return [100,101,102,103,104,105,106,107,108,109,200,201,202,203,204,205,206,207,208,209,300,301,302,303,304,305,306,307,400,401,402,403,404,405,406]
    file_no_list = file_no.split(',')
    for file_no in file_no_list:
        if "-" not in file_no:
            result.append(int(file_no))
        else:
            split = file_no.split("-")
            result.extend(range(int(split[0]), int(split[1]) + 1)) # -를 기준으로 range
    return result

'''
이번달의 마지막 날을 datetype return
'''
def month_last_day(day):
    day = day + relativedelta.relativedelta(months=1)
    last_day_month_ago = day.replace(day=1) - relativedelta.relativedelta(days=1)
    return last_day_month_ago

'''
시작 일자와 종료일자를 return
'''
def get_start_end_date(start_YM, end_YM):
    today = date.today()
    if end_YM == '*' and start_YM != '*':
        end_YM = start_YM
    start_date = datetime.datetime.strptime(start_YM, "%Y-%m").date()
    end_date = datetime.datetime.strptime(end_YM, "%Y-%m").date()

    if (start_date == end_date):
        if start_date.month != today.month:
            return start_date.replace(day=1), month_last_day(end_date)
        else:
            return start_date.replace(day=1), today
    elif (start_date < end_date and end_date.month == today.month):
        return start_date.replace(day=1), today
    elif (start_date < end_date):
        return start_date.replace(day=1), month_last_day(end_date)
    else:
        return 0,0