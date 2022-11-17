import csv
import time
import random
import requests
import warnings

warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup

url = "https://imarksearch.com/marksearch/sangpyoSearchList.do"


def marksearch(target_kor):
    files = []
    payload = {"BrandName": f"{target_kor}"}
    sleep_time = round(random.uniform(0.43, 1), 3)  # moderate

    headers = {
        "Cookie": "Grids=searchGrid0#+XLNDeLVrCPqqnqAbPager]bEdSangpyoName]]+A]bSangpumryu]-b-b-bIqSbIbIbAdDuL9JcpPanel+DdistinctCount]DgroupCode]GImageUrl]BcDChulwonNo]GSangpyoName]HeESangpyoEng]FSangpumryu]WeGYusagunCode]QcGChulwonin]kFChulwonNoFormat]9ERegisterNo]FRegisterDate]kEGonggoNo]GLastAppName]Ib7DaeriinvStatusGcETrialInfo]GExpireDate]9++; marksearch_user_id_cookie=haeyul; marksearch_user_password_cookie=13611!; JSESSIONID=F3C92D1C652C68D96BEB2F3FD2802053; locale=ko; OptanonConsent=isIABGlobal=false&datestamp=Thu+Aug+25+2022+13%3A44%3A36+GMT%2B0900+(%ED%95%9C%EA%B5%AD+%ED%91%9C%EC%A4%80%EC%8B%9C)&version=6.31.0&hosts=&consentId=7e961f1a-79e4-4bd9-9733-6322a7839dad&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1&AwaitingReconsent=false&geolocation=KR%3B41; OptanonAlertBoxClosed=2022-08-25T04:44:36.726Z; JSESSIONID=BF39C6D4F146EC8CD2F22793E8A98643",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Authorization": "Basic aGFleXVsOjEzNjExIQ==",
    }
    try:
        response = requests.post(
            url, headers=headers, data=payload, files=files, timeout=60
        )

        kor, eng = [], []
        soup = BeautifulSoup(response.text, "html.parser")

        for i in soup.find_all("i"):
            if not (i["sangpyoname"] == "" or i["sangpyoname"] == " "):
                kor.append(i["sangpyoname"])

            if not (i["sangpyoeng"] == "" or i["sangpyoeng"] == " "):
                eng.append(i["sangpyoeng"].lower())

        time.sleep(sleep_time)

    except Exception as e:
        print(e)
        with open("../result_txt/marksearch_error.txt", "a", encoding="utf-8-sig") as f:
            tw = csv.writer(f, delimiter="\t")
            tw.writerow([target_kor, e])
        pass
        time.sleep(sleep_time)

    return kor + eng


if __name__ == "__main__":

    target_kor = "딕셔너리"

    li_kor = marksearch(target_kor)
    li_kor = list(set(li_kor))

    print(li_kor)
    print("\n>> finish")
