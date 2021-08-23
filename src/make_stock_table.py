import dart_fss
from dart_fss import corp

api_key = 'd1e5b05bbc86fef9c3d6a72ae1a1c764fd65b5fe'
dart_fss.set_api_key(api_key=api_key)

corp_list = corp.get_corp_list()

corp = corp_list.find_by_corp_name('삼성전자', True)[0]

corp.load()

for corp in corp_list[:10]:
	print(corp.corp_name, corp.corp_code)