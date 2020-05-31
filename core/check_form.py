#принимает два словаря: первый из опросника, второй из распарсенного егрюла
def check_form(form_data, egrul_data):
	# данные, которые не лежат напрямую в конце, в данном случае это "Размер уставного капитала"
	checked_data = ["ОГРН", "ИНН", "Полное наименование", "Сокращенное наименование", "Размер уставного капитала"]
	# кол-во данных, которые не лежат напрямую
	special_check = 1;
	# идем только по общим данным
	for i in range(len(checked_data) - special_check):
		if(form_data[checked_data[i]].lower() != egrul_data[checked_data[i]].lower()):
			return False
	# отдельная проверка
	if(form_data["Размер уставного капитала"] != egrul_data["Сведения об уставном капитале"]["Размер"]):
		return False

	return True
	