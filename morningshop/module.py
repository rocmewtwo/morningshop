#! python3
# -*- coding: utf-8 -*-
import csv
import os.path
from collections import defaultdict, Counter
from operator import itemgetter
from itertools import groupby, chain
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))

def loadOrderData():
  with open(os.path.join(BASE, 'order.csv'), newline='', encoding='utf8') as csvfile:
    next(csvfile) ## skip header
    reader = csv.reader(csvfile)
    order = list(reader)

  return order

def loadItemData():
  with open(os.path.join(BASE, 'order_item.csv'), newline='', encoding='utf8') as csvfile:
    next(csvfile) ## skip header
    reader = csv.reader(csvfile)
    orderItem = list(reader)

  return orderItem

def calCohort(order):
  cohortData = []
  userList = defaultdict(set)
  lastDate = None

  for date, group in groupby(sorted(order, key=lambda o: o[3]), key=lambda o: o[3].split()[0]):
    dt = datetime.strptime(date, "%Y/%m/%d")
    ## 補齊空白天數
    if (lastDate != None and dt-lastDate > timedelta(days=1)):
      for i in range(1, (dt - lastDate).days):
        addDate = dt + timedelta(days=i)
        addLastCohort(cohortData, userList, addDate, set())

    ## 統計當天的user
    userList[date] = addUser = set(data[1] for data in group)
    ## 增加資料到cohortData
    addLastCohort(cohortData, userList, date, addUser)
    lastDate = datetime.strptime(date, "%Y/%m/%d")

  return cohortData

## 增加user下訂到每一層級的最後一欄
def addLastCohort(cohortData, userList, date, addUser):
  if (len(cohortData) == 0):
    cohortData.append((date, [len(addUser)]))
  else:
    for index, data in enumerate(cohortData):
      user = userList.get(data[0], set())
      cohortData[index][1].append(len(user.intersection(addUser)))

    cohortData.append((date, [len(addUser)]))

def findMostPalpular(orderItem):
  itemList = list(chain(*[[item[1]] * int(item[2]) for item in orderItem]))
  counter = Counter(itemList)
  most3 = counter.most_common(3)

  return most3

if __name__ == "__main__":
  order = loadOrderData()
  orderItem = loadItemData()

  cohortData = calCohort(order)
