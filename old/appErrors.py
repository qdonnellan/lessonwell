
def google_user_not_found():
	return "You need to be signed into Google and link your Google Account before you can create an account"

def DNE(thing_that_does_not_exist):
	return "That %s does not exist" % thing_that_does_not_exist

def inactive(thing_that_is_inactive):
	return "That %s is currently inactive" % thing_that_is_inactive

def id_not_digits():
	return "The content ID must be an ingteger"

def terms_not_accepted():
	return "You must accept the terms of service before creating an account"

def customer_not_found():
	return "We could not locate your customer information"

def plan_not_found():
	return "We could not locate your customer subscription information"
