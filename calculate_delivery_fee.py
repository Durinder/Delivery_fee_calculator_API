import json
import datetime

def calculate_delivery_fee(order):
	with open("config.json", "r") as f:
		rules = json.load(f)

	""" with open('data.json', 'w') as outfile:
		json.dump(rules, outfile, ensure_ascii=False, indent=4) """
	
	#free delivery
	if order.cart_value >= rules['free_delivery_cutoff']:
		return 0

	#small order surcharge
	small_order_surcharge = rules['small_order_surcharge_cutoff'] - order.cart_value if order.cart_value < rules['small_order_surcharge_cutoff'] else 0

	#delivery distance fee
	delivery_distance_fee = rules['delivery_distance']['first_distance']['value']
	dist = rules['delivery_distance']['first_distance']['meters']
	while dist < order.delivery_distance:
		delivery_distance_fee += rules['delivery_distance']['additional_distance']['value']
		dist += rules['delivery_distance']['additional_distance']['meters']

	#item surcharge
	item_surcharge = rules['item_surcharge']['value'] * (order.number_of_items - rules['item_surcharge']['cutoff']) if order.number_of_items > rules['item_surcharge']['cutoff'] else 0

	#subtotal
	fee = small_order_surcharge + delivery_distance_fee + item_surcharge

	#friday rush
	date, time = order.time.split('T')
	if datetime.date.fromisoformat(date).weekday() == 4:
		print('FRIDAY!')
		time = datetime.time.fromisoformat(time.replace('Z', '+00:00'))
		print(time)
		start = datetime.time.fromisoformat(rules['friday_rush']['starting_time'].replace('Z', '+00:00'))
		end = datetime.time.fromisoformat(rules['friday_rush']['ending_time'].replace('Z', '+00:00'))
		if time >= start and time < end:
			fee = int(fee * rules['friday_rush']['multiplier'])

	#maximum delivery fee
	if fee > rules['maximum_delivery_fee']:
		fee = rules['maximum_delivery_fee']
	
	return fee