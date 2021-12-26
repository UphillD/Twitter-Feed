# Miscellaneous functions required by the twitter API
import requests

from config import *

# Generates list of search rules from file
def generate_rules():
	# Initialize empty rule list
	query_rules = rules
	return query_rules

# Authenticates bearer token (API v2)
def bearer_oauth(r):
	r.headers["Authorization"] = "Bearer {}".format(bearer_token)
	r.headers["User-Agent"] = "v2FilteredStreamPython"
	return r

# Gets current query rules
def get_rules():
	response = requests.get(url_rules, auth=bearer_oauth)
	if response.status_code != 200:
		raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
	return response.json()

# Deletes current query rules
def delete_rules(rules):
	if rules is None or "data" not in rules:
		return None

	ids = list(map(lambda rule: rule["id"], rules["data"]))
	payload = {"delete": {"ids": ids}}
	response = requests.post(url_rules, auth=bearer_oauth, json=payload)
	if response.status_code != 200:
		raise Exception("Cannot delete rules (HTTP {}): {}".format(response.status_code, response.text))
	return response.json()

# Sets new query rules
def set_rules(rules):
	payload = {"add": rules}
	response = requests.post(url_rules, auth=bearer_oauth, json=payload)
	if response.status_code != 201:
		raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))
	return response.json()

