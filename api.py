from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, validator
from get_delivery_fee import get_delivery_fee

class Order(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: str

	@validator('number_of_items')
	def	at_least_one_item(cls, v):
		if v < 1:
			raise ValueError('no items in order')
		return v

	@validator('time')
	def time_valid(cls, v):
		print(v)
		format_string = '%Y-%m-%dT%H:%M:%SZ'
		try:
			datetime.strptime(v, format_string)
		except:
			raise ValueError(f'time not in ISO format, should be {format_string}')
		return v

app = FastAPI()

@app.post("/delivery_fee")
async def calculate_delivery_fee(order: Order):
	print(order.cart_value)
	fee = get_delivery_fee(order)
	
	return { "delivery_fee": fee }