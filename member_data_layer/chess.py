import json

class DataLayerException(Exception):
 def __init__(self,message="",exceptions=None):
  self.message=message
  self.exceptions=exceptions
 def toJSON(self):
  json_string=json.dumps(self,indent=4,default=lambda obj:obj.__dict__)
  return json_string
 def fromJSON(json_string):
  dictionary=json.loads(json_string)
  message=dictionary["message"]
  exceptions=dictionary["exceptions"]
  return DataLayerException(message,exceptions)
 def fromDict(dictionary):
  return DataLayerException(**dictionary)

class Member:
 def __init__(self,username,password):
  self.username=username
  self.password=password
 def toJSON(self):
  return json.dumps(self.__dict__)
 def fromJSON(json_string):
  new_dict=json.loads(json_string)  
  return Member(**new_dict)

