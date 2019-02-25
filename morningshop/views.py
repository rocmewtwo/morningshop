#! python3
# -*- coding: utf-8 -*-

import json
import sys

from morningshop.module import *
import collections

from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response

def Q1(request):
  order = loadOrderData()
  orderItem = loadItemData()

  ## Q1(a)
  shipList = list(map(lambda o: "運費" if (int(o[2]) > 0) else "免運", order))
  shipCount = collections.Counter(shipList)

  ## Q1(b)
  cohortData = calCohort(order)
  minDate = cohortData[0][0]
  cohortData = [data for _, data in cohortData]

  ## Q1(c)
  most3 = findMostPalpular(orderItem)

  return render(request, "Q1.html", {"shipCount": json.dumps(shipCount), "minDate": minDate, "cohortData": json.dumps(cohortData), "most3": json.dumps(most3)})

def Q2(request):
  return render(request, "Q2.html")

def Q3(request):
  return render(request, "Q3.html")

## Ajax Start
## Ajax End
