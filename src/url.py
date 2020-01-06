from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlunparse


def make(url):
	return urlparse(url)


def get_scheme(data):
	return data.scheme

def get_host(data):
	return data.netloc

def get_path(data):
	return data.path

def get_query(data):
	return data.query

def set_scheme(data, scheme):
	new_url = data._replace(scheme = scheme)
	return new_url

def set_host(data, host):
	new_url = data._replace(netloc = host)
	return new_url

def set_path(data, path):
	new_url = data._replace(path = path)
	return new_url

def set_query(data, query):
	new_url = data._replace(query = query)
	return new_url


def get_query_param(data, param_name, default = None):
	query = get_query(data)
	parsed_query = parse_qs(query)
	if (param_name in parsed_query):
		return parsed_query[param_name][0]
	return default


def set_query_param(data, key, value):
	if not(get_query_param(data, key)) and value is None:
		return data
	query = get_query(data)
	parsed_query = parse_qs(query)

	if (value is None):
		parsed_query.pop(key, None)
	else:
		parsed_query[key] = value

	new_query = urlencode(parsed_query, doseq=True)

	return set_query(data, new_query)


def to_string(data):
	return urlunparse(data)


u = make('https://domain.org/community?q=low')
print(to_string(u) == 'https://domain.org/community?q=low')


u = set_host(u, 'zxc.io')
print(get_host(u) == 'zxc.io')
print(to_string(u) == 'https://zxc.io/community?q=low')


u = set_scheme(u, 'http')
print(get_scheme(u) == 'http')
print(to_string(u) == 'http://zxc.io/community?q=low')

u = set_path(u, '/404')
print(get_path(u) == '/404')
print(to_string(u) == 'http://zxc.io/404?q=low')


u = set_query_param(u, 'page', 5)
print(to_string(u) == 'http://zxc.io/404?q=low&page=5')

u = set_query_param(u, 'q', 'high')
print(to_string(u) == 'http://zxc.io/404?q=high&page=5')
print(get_query_param(u, 'q') == 'high')
print(get_query_param(u, 'user', 'guest') == 'guest')
print(get_query_param(u, 'b') is None)

u = set_query_param(u, 'q', None)
print(to_string(u) == 'http://zxc.io/404?page=5')

u = set_query_param(u, 'missed', None)
print(to_string(u) == 'http://zxc.io/404?page=5')
