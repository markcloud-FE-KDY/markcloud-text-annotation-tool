# Markcloud-Text-Review 정의서

1. 날짜 입력

    - ex. `python3 main.py –date 20221001-20221003` 이면, `[20221001,20221002,20221003]` 에 해당하는 날짜 들고 오기 

    - ex. `python3 main.py –date 20221001-20221001` 이면,`[20221001]` 에 해당하는 날짜 들고 오기 
 
    - ex. `python3 main.py –date 20221002` 이면,`[20221002]` 에 해당하는 날짜 들고 오기 

    - ex. `python3 main.py` 이면, `[오늘날짜]` 들고 오기 
       
<br>

2. 들고 온 날짜에 업데이트 된 `productNameEng` 데이터 들고오기 

    ```python
    def get_updated_data(coll, start_date, end_date):
        print(f"> get_updated_data... {start_date}-{end_date}")

        updated_data = list(
            coll.find(
                {
                    "_dataUpdateDate": {"$gte": start_date, "$lte": end_date},
                    "productNameEng": {"$ne": None},
                },
                {"_id": 0, "productNameEng": 1},
            )
        )

        return updated_data
    ```
       
<br>

3. 가져 온 `productNameEng` 를 전처리

    1. `.lower()` 적용
    2. 공백 기준으로 split
    3. regular expression 적용 `[^a-zA-Z]`
    4. 중복 제거
    5. 전처리 된 `productNameEng` 를 저장하고 반환 ex.`['kipris', 'update']`

    ```python
    def data_preprocess(updated_data):
        print("> data_preprocess...")
        tmp = []

        for ud in updated_data:
            words = ud.lower().split(" ")
            for word in words:
                word2 = re.sub("[^a-zA-Z]", "", word)
                if word2:
                    tmp.append(word2)

        processed_data = list(dict.fromkeys(tmp))

        return processed_data
    ```

<br>

4. 기존 `mark_dict` 데이터에 있는 `productNameEng` 항목들은 제거

    ```python
    def get_difference(processed_data, source_eng):
        print("> get_difference...")
        res = Counter(processed_data) - Counter(source_eng)
        diff_result = list(res.keys())

        return diff_result
    ```

<br>

5. 남은 `productNameEng`를 `model.py`를 이용해서 `modelResult`로 변환 

    - ex : `wwwyedinacomcn	예디나`, `lonseal	론씰`

<br>

6. `modelResult`를 마크서치에 검색 (`marksearch.py`)

    1. 일치하는 항목이 있으면 `mark_dict` 컬렉션에 바로 저장 
       1.  ex. `extremes	익스트림스` 에서 `익스트림스` 를 마크서치에 검색
       2. `['NORTHERN EXTREMES', 'NORTHERN EXTREMES', 'EXTREME SCREEN', 'extremesports']` 검색 결과  리스트 내에서  `productNameEng` 컬럼의 `extremes` 가 들어있는 문자열이 있거나 `extremes` or `EXTREMES` 등 완전일치하는 항목이 있으면,
       3. `mark_dict` 컬렉션에`['productNameEng', 'modelResult', 'similarWords', 'humanCheck']` 데이터를 저장 및 `humanCheck` 컬럼은 `true` 로 표시
       <br>
    2. 일치하는 항목이 없으면 `productNameEng` 를 마크서치에 검색 (`marksearch.py`)
       1. ex. `econapaen	에코나페엔` 에서 `econapaen` 을 마크서치에 검색
       2. `['에코나팬', 'ECONAPAEN']` 검색 결과 리스트 내에서 `modelResult` 컬럼의 `에코나페엔` 이 들어있는 문자열이 **있으면** 6-1-3 번 실행
          1. **없으면**  `['에코나팬', 'ECONAPAEN']` 의 한글 원소들을 `kodex` 로 변환 후 유사도 측정 후 **75%** 정확도 이상이면 `mark_dict` 컬렉션에`['productNameEng', 'modelResult', 'similarWords', 'humanCheck']` 데이터를 저장
             - `similarWords` 컬럼은 유사도 순으로 정렬
             - `humanCheck` 컬럼은 `false` 로 표시


---

# API 동작 과정

1. 현재 db에 있는 `humanCheck=false`인 `mark_dict` 중에서 `_id`가 가장 작은 데이터를 불러온다.

   ```python
   def retrieve_markdict(oid: Optional[str] = None) -> dict:
       if not oid:
           markdict = list(
               mark_dict_collection.find({"humanCheck": False}).sort("_id", 1).limit(1)
           )[0]
       else:
           markdict = mark_dict_collection.find_one({"_id": ObjectId(oid)})
       if markdict:
           return markdict_helper(markdict)
   ```

2. 검수자는 `productNameEng`를 보고 다음 중 하나로 `modelResult`를 업데이트 할 수 있다.

   1. 기존의 `modelResult`
   2. `similarWord`의 유사 단어들
   3. 검수자가 직접 입력


3. `완료` 버튼을 누르면 

   1. 기존의 `modelResult`는 `previousResult` 컬럼에 저장된다.

      ```python
      def add_previousResult(oid: str, previousResult: str):
          oid = ObjectId(oid)
          mark_dict_collection.update_one(
              {"_id": oid},
              {"$set": {"previousResult": previousResult}},
          )
      ```

   2. `modelResult`는 1-2에서 선택한 것으로 업데이트된다.

      ```python
      def update_modelResult(oid: str, data: dict):
          if len(data) < 1:
              return False
          oid = ObjectId(oid)
          mark_dict_collection.update_one(
              {"_id": oid},
              {"$set": data},
          )
      ```

   3. `humanCheck`가 true로 업데이트된다.

      ```python
      def update_humanCheck(oid: str):
          oid = ObjectId(oid)
          mark_dict_collection.update_one({"_id": oid}, {"$set": {"humanCheck": True}})
      ```

4. `retrieve_previous`  현재 `ObjectId`보다 작은 `ObjectId` 중에서 가장 큰 값을 가져온다.

   ```python
   def retrieve_previous(oid: Optional[str] = None) -> dict:
       if not oid:
           return None
       previous = list(
           mark_dict_collection.find({"_id": {"$lt": ObjectId(oid)}, "humanCheck": False})
           .sort("_id", -1)
           .limit(1)
       )
       if previous:
           return markdict_helper(previous[0])
   ```

5. `retrieve_next`  현재 `ObjectId`보다 큰 `ObjectId` 중에서 가장 작은 값을 가져온다.

   ```python
   def retrieve_next(oid: Optional[str] = None) -> dict:
       if not oid:
           next = list(
               mark_dict_collection.find({"humanCheck": False})
               .sort("_id", 1)
               .skip(1)
               .limit(1)
           )[0]
       else:
           next = mark_dict_collection.find_one(
               {"_id": {"$gt": ObjectId(oid)}, "humanCheck": False}
           )
       if next:
           return markdict_helper(next)
   ```

