# AWS Cost Report Web

### 📌실행방법

1. AWS_COST_API_WEB을 다운로드받아  `C:\AWS_COST_API_WEB` 경로에 압축을 해제합니다. 

2. 필요한 모듈이 설치되어있는 가상 환경을 실행시키기 위해, 가상 환경 아래의 Scripts폴더로 이동합니다. cmd 창에 다음 명령+경로를 입력합니다. 

   ```
   cd C:\AWS_COST_API_WEB\venv\Scripts
   ```

3. 해당 위치에서 가상환경을 실행시킵니다. cmd 창에 activate명령을 입력합니다. 

   ```
   C:\AWS_COST_API_WEB\venv\Scripts>activate
   (venv) C:\AWS_COST_API_WEB\venv\Scripts>
   ```
`
4. `AWS_COST_API_WEB`로 이동해 runserver 명령을 실행합니다. 

   ```
   (venv) C:\AWS_COST_API_WEB\venv\Scripts>cd ..
   `
   (venv) C:\AWS_COST_API_WEB\venv>cd ..
   
   (venv) C:\AWS_COST_API_WEB>python manage.py runserver 80
   Watching for file changes with StatReloader
   Performing system checks...
   (...)
   ```

5. 웹브라우저에서 http://127.0.0.1:80/ 또는 http://localhost:80/ 으로 접속합니다. 
6. [api 호출] 버튼을 클릭합니다.
7. 파일 번호, 시작일, 종료일을 입력한 후 [조회하기]버튼을 누릅니다. 
8. `C:\AWS_COST_API_WEB\report`에서 조회 결과를 csv파일로 확인할 수 있습니다. 
9. 웹 브라우저에서 조회 결과를 이미지파일로 확인할 수 있습니다. 



### 📌프로젝트 개요

- `get_cost_and_usage()` 를 사용해 루트계정별 사용량 및  지불해야할 비용(단위: USD)을 확인할 수 있습니다. 
- 루트계정별로 비용 관리 용도의 사용자(`CostManager`)를 생성한 후, CostManager의 액세스 키를 사용해 API요청을 전송합니다. 
- 요청을 통해 받은 데이터(json)을 파싱하여 원하는 데이터만 추출해 dataframe화 하고, csv 파일로 저장합니다. 
- `aws_account_*.csv` : 루트계정별 로그인 정보, 액세스 키 정보. 요청 파라미터에 들어갈 데이터 관리 용도
  - Root Account: 루트계정 로그인 ID
  - Name: 루트계정 이름
  - Password : 루트계정 로그인 비밀번호
  - CostManager_ID: 비용 관리 사용자 로그인 ID
  - CostManager_PW: 비용 관리 사용자 로그인 PW
  - Access_ID: 액세스 키 아이디
  - Secret_Access_Key: 시크릿 액세스 키
  - Region: 지역
  - Account_ID: 루트계정 ID, IAM사용자로 로그인 시 사용
- `aws_cost.py` : `get_cost_and_usage()`를 호출하는 파이썬 프로그램 
- `AWS_cost_calculate.py` : 요청 결과 생성되는 csv파일을 읽어, 데이터를 시각화하는 파이썬 프로그램 
- `report/aws_cost_report_[현재시각정보].csv` : `aws_cost.py` 실행 결과 생성되는 데이터 파일 



