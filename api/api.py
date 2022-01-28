import re
import os
import json
from types import SimpleNamespace
from functools import lru_cache
from datetime import datetime
from fastapi import Depends, FastAPI
from pydantic import BaseModel, validator, Extra
from .calculate_delivery_fee import calculate_delivery_fee

class Order(BaseModel, extra=Extra.forbid):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: str

	@validator('number_of_items')
	def	at_least_one_item(cls, v):
		if v < 1:
			raise ValueError('no items in order')
		return v

	# validation is strict by choice and accepts only full ISO format strings
	# with timezone included and optionally microseconds
	# eg. YYYY-MM-DDTHH:MM:SS(.sss[sss])Z or YYYY-MM-DDTHH:MM:SS(.sss[sss])±ZZ:ZZ
	# additional check is for incorrect dates such as Feb 30
	@validator('time')
	def validate_datetime(cls, v):
		regex = r'^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](2[0-3]|[01][0-9]):[0-5][0-9])$'
		match_iso8601 = re.compile(regex).match
		if match_iso8601(v) is None:
			raise ValueError('time not in ISO format, use: YYYY-MM-DDTHH:MM:SS(.sss[sss])Z or YYYY-MM-DDTHH:MM:SS(.sss[sss])±ZZ:ZZ')
		try:
			datetime.fromisoformat(v.replace('Z', '+00:00'))
		except:
			raise ValueError('incorrect date')
		return v

app = FastAPI()

@lru_cache(maxsize=1)
def get_rules():
	with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
 		return json.load(f, object_hook=lambda d: SimpleNamespace(**d))

@app.put("/delivery_fee")
def get_delivery_fee(order: Order, rules = Depends(get_rules)):
	fee = calculate_delivery_fee(order, rules)
	return {"delivery_fee": fee}