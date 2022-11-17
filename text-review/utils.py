import re
from collections import Counter
from datetime import datetime, timedelta


def get_date_range(inputdate):
    dt_list = []

    if not inputdate:
        inputdate = datetime.today().strftime("%Y%m%d")
        dt_list.append(inputdate)

    else:
        dr = inputdate.split("-")
        if len(dr) == 1:
            inputdate = dr[0]
            dt_list.append(inputdate)

        else:
            start = datetime.strptime(dr[0], "%Y%m%d")
            end = datetime.strptime(dr[1], "%Y%m%d")
            dt_list = [
                (start + timedelta(days=i)).strftime("%Y%m%d")
                for i in range((end - start).days + 1)
            ]

    return dt_list


# 공백 기준 split -> regular expression -> lower() -> 중복제거
def data_preprocess(updated_data):
    print("> data_preprocess...")
    tmp = []

    for ud in updated_data:
        words = ud["productNameEng"].lower().split(" ")
        for word in words:
            word2 = re.sub("[^a-zA-Z]", "", word)
            if word2:
                tmp.append(word2)

    processed_data = list(dict.fromkeys(tmp))

    return processed_data


def get_difference(processed_data, source_eng):
    print("> get_difference...")
    res = Counter(processed_data) - Counter(source_eng)
    diff_result = list(res.keys())

    return diff_result
