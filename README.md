# Markcloud-Text-Annotation API 정의서


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

