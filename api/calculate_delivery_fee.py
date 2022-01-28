from __future__ import annotations
import datetime

from types import SimpleNamespace
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .api import Order


def calculate_delivery_fee(order: Order, rules: SimpleNamespace) -> int:

	#free delivery
	if order.cart_value >= rules.free_delivery_cutoff:
		return 0

	#small order surcharge
	if order.cart_value < rules.small_order_surcharge_cutoff:
		small_order_surcharge = rules.small_order_surcharge_cutoff - order.cart_value
	else:
		small_order_surcharge = 0

	#delivery distance fee
	delivery_distance_fee = rules.delivery_distance.first_distance.value
	dist = rules.delivery_distance.first_distance.meters
	while dist < order.delivery_distance:
		delivery_distance_fee += rules.delivery_distance.additional_distance.value
		dist += rules.delivery_distance.additional_distance.meters

	#item surcharge
	if order.number_of_items > rules.item_surcharge.cutoff:
		item_surcharge = rules.item_surcharge.value * (order.number_of_items - rules.item_surcharge.cutoff)
	else:
		item_surcharge = 0

	#subtotal
	fee = small_order_surcharge + delivery_distance_fee + item_surcharge

	#friday rush
	date, time = order.time.split('T')
	if datetime.date.fromisoformat(date).weekday() == 4:
		time = datetime.time.fromisoformat(time.replace('Z', '+00:00'))
		start = datetime.time.fromisoformat(rules.friday_rush.starting_time.replace('Z', '+00:00'))
		end = datetime.time.fromisoformat(rules.friday_rush.ending_time.replace('Z', '+00:00'))
		if time >= start and time < end:
			fee = int(fee * rules.friday_rush.multiplier)

	#maximum delivery fee
	if fee > rules.maximum_delivery_fee:
		fee = rules.maximum_delivery_fee

	print(
f'small_order_surcharge_fee: {small_order_surcharge}\n\
delivery_distance_fee: {delivery_distance_fee}\n\
item_surcharge: {item_surcharge}\n\
friday_rush: {fee - small_order_surcharge - delivery_distance_fee - item_surcharge}\n\
fee: {fee}')
	return fee