# Dash - 한국 화훼 공판장 경매 정보 대쉬보드

## Project Description
이 프로젝트는 [Dash](https://plotly.com/dash/) 를 이용해 한국의 화훼 공판장 경매 정보를 
interactive한 대쉬보드로 시각화하고 그 결과를 [Heroku](https://www.heroku.com) 를 사용해 
웹페이지로 구현합니다.

## Data
시각화에 사용한 데이터는 [화훼유통정보시스템](https://flower.at.or.kr/) 에서 제공하는 공공데이터로
2017년 1월부터 2021년까지 12월까지 수집된 'at양재'에서 거래된 품목/품종별 경매 정보 입니다.

- Data 수집: [Flower_DataCollect.ipynb](https://github.com/JayAhn0104/Dash_Plolty/blob/master/Flower_DataCollect.ipynb)

## Dashboard Overview
대쉬보드 웹사이트는 총 3페이지로 분리되어 있습니다. 
1. 전체 시장
   - 시장 전체의 거래량 및 평균 거래금액 요약
2. Top Sales
   - 년도별/월별 거래량 및 평균 거래금액 기준 상위 일부 품목들에 대한 정보
3. 개별 품목
   - 개별 품목에 대한 거래량 및 평균 거래금액

| 전체시장                                                                                                                                | Top_Sale                                                                                                                                | 개별품목                                                                                                                                |
|-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| <center><img alt="screen_shot" src='https://drive.google.com/uc?export=view&id=1WOW25FndVx3gjzvkAiAMeGypi7EliaCN' width = 300></center> | <center><img alt="screen_shot" src='https://drive.google.com/uc?export=view&id=1WSev0pK5Z3XrbDY8WNUBCa9WhahFDKTr' width = 300></center> | <center><img alt="screen_shot" src='https://drive.google.com/uc?export=view&id=1jcoUMFBnl9j560XckLfrBANnaFwexTPD' width = 300></center> |

<br>

## Dashboard Website
[korea-flower](https://korea-flower.herokuapp.com)

위의 링크를 통해 완성된 대쉬보드를 제공하는 웹사이트로 접속할 수 있습니다. 





