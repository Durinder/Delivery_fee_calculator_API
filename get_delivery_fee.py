import json
from types import SimpleNamespace

def get_delivery_fee(order):
	with open("config.json", "r") as jsonfile:
		rules = json.load(jsonfile, object_hook=lambda d: SimpleNamespace(**d))

	#small_order_surcharge
	small_order_surcharge = rules.small_order_surcharge_cutoff - order.cart_value if order.cart_value < rules.small_order_surcharge_cutoff else 0

	#delivery_distance_fee
	delivery_distance_fee = rules.delivery_distance.first_distance.value
	dist = rules.delivery_distance.first_distance.meters
	while dist < order.delivery_distance:
		delivery_distance_fee += rules.delivery_distance.additional_distance.value
		dist += rules.delivery_distance.additional_distance.meters

	#item_surcharge
	item_surcharge = rules.item_surcharge.value * (order.number_of_items - rules.item_surcharge.cutoff) if order.number_of_items > rules.item_surcharge.cutoff else 0

	#free_delivery
	if order.cart_value >= rules.free_delivery_cutoff:
		return 0

	fee = small_order_surcharge + delivery_distance_fee + item_surcharge
	print(
f'small_order_surcharge_fee: {small_order_surcharge}\n\
delivery_distance_fee: {delivery_distance_fee}\n\
item_surcharge: {item_surcharge}')
	return fee

if __name__=='__main__':
	print("hello world")