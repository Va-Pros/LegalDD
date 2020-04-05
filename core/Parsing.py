import io
import re
import fitz

def pdf_to_text(path):
    doc = fitz.open(path)
    text = ''
    for current_page in range(len(doc)):
        page = doc.loadPage(current_page)
        text = text + page.getText()
    return text

def parsing(path):
	text = pdf_to_text(path)
	def find_data(regular1, regular2, start = 0, end = len(text)):
		found1 = re.search(regular1, text[start : end], flags = re.DOTALL)
		found2 = re.search(regular2, text[start : end], flags = re.DOTALL)
		if found1 is None:
			return found2
		if found2 is None:
			return found1
		if(len(found1[0]) < len(found2[0])):
			return found1
		return found2

	def processing(found, offset_start, offset_end):
		rez = found[0][offset_start : len(found[0]) - offset_end]
		rez = rez.replace('\n', ' ')
		return rez

	def find_offset(text):
		i = len(text) - 2
		count = 2
		while(text[i] != '\n'):
			i -= 1
			count += 1
		return count

	def extract_data(regular1, regular2, bounds, offset_start, offset_end = -1):
		found = find_data(regular1, regular2, bounds['start'], bounds['end'])
		if(found is None):
			return 'Данные отсутствуют или не найдены'
		bounds['start'] += found.end()
		if(offset_end == -1):
			offset_end = find_offset(found[0])
		return processing(found, offset_start, offset_end)

	key_words = ['Полное наименование', 'Сокращенное наименование', 'Адрес', 'ОГРН', 'Дата регистрации', 'Сведения о прекращении',
				 'ИНН', 'Сведения об уставном капитале', 'Сведения о директоре', 'Сведения об учредителях', 'Сведения о держателе реестра акционеров',
				 'Сведения об основном виде деятельности']
	bounds = {'start' : 0, 'end' : len(text)}
	result = {}

	result[key_words[0]] = extract_data('Полное наименование.+?\n\d{,4}\n',
										'Полное наименование.+?Страница \d+ из \n', bounds, len(key_words[0]) + 1) # Полное наименование

	result[key_words[1]] = extract_data('Сокращенное наименование.+?\n\d{,4}\n',
										'Сокращенное наименование.+?Страница \d+ из \n', bounds, len(key_words[1]) + 1) # Сокращенное наименование

	found = find_data('Адрес.+?\n\d{,4}\n', 'Адрес.+?Страница \d+ из \n', bounds['start'])
	bounds['start'] += found.end()
	bounds['end'] = text.find('ГРН', bounds['start'])
	result[key_words[2]] = {}
	while(bounds['start'] < bounds['end']):
		key = extract_data('.+?\n', '.+?\n', bounds, 0, 1)
		val = extract_data('.+?\n\d{,4}\n','.+?\n\d{,4}\n', bounds, 0)
		result[key_words[2]][key] = val # Адрес
	bounds['end'] = len(text)

	result[key_words[3]] = extract_data('\nОГРН.+?\n\d{,4}\n', '\nОГРН.+?Страница \d+ из \n', bounds, len(key_words[3]) + 2) # ОГРН

	result[key_words[4]] = extract_data('Дата регистрации.+?\n\d{,4}\n',
										'Дата регистрации.+?Страница \d+ из \n', bounds, len(key_words[4]) + 1) # Дата регистрации

	if(text.find('Сведения о прекращении') != -1):
		result[key_words[5]] = {}
		bounds['end'] = text.find('Сведения об учете в налоговом органе', bounds['start'])
		result[key_words[5]]['Способ прекращения'] = extract_data('Способ прекращения.+?\n\d{,4}\n',
															   'Способ прекращения.+?Страница \d+ из \n', bounds, 19)
		result[key_words[5]]['Дата прекращения'] = extract_data('Дата прекращения.+?\n\d{,4}\n',
															 'Дата прекращения.+?Страница \d+ из \n', bounds, 17)
		bounds['end'] = len(text)

	result[key_words[6]] = extract_data('ИНН.+?\n\d{,4}\n', 'ИНН.+?Страница \d+ из \n', bounds, len(key_words[6]) + 1) # ИНН

	found = find_data('Сведения об уставном капитале.+?\n\d{,4}\n', 'Сведения об уставном капитале.+?Страница \d+ из \n', bounds['start'])
	bounds['start'] += found.end()
	bounds['end'] = text.find('Сведения о лице,', bounds['start'])
	result[key_words[7]] = {}
	result[key_words[7]]['Вид'] = extract_data('Вид.+?\n\d{,4}\n', 'Вид.+?Страница \d+ из \n', bounds, 4)
	result[key_words[7]]['Размер'] = extract_data('Размер \(в рублях\).+?\n\d{,4}\n', 'Размер \(в рублях\).+?Страница \d+ из \n', bounds, 18)
	result[key_words[7]]['Дата внесения в ЕГРЮЛ'] = extract_data('\n\d{13}\n\d{2}\.\d{2}\.\d{4}',
																 '\n\d{13}\n\d{2}\.\d{2}\.\d{4}', bounds, 15, 0) # Сведения об уставном капитале

	bounds['end'] = text.find('Сведения об учредителях', bounds['start'])
	result[key_words[8]] = {}
	result[key_words[8]]['Фамилия'] = extract_data('Фамилия.+?\n\d{,4}\n', 'Фамилия.+?Страница \d+ из \n', bounds, 8)
	result[key_words[8]]['Имя'] = extract_data('Имя.+?\n\d{,4}\n', 'Имя.+?Страница \d из \n', bounds, 4)
	result[key_words[8]]['Отчество'] = extract_data('Отчество.+?\n\d{,4}\n', 'Отчество.+?Страница \d+ из \n', bounds, 9)
	result[key_words[8]]['ИНН'] = extract_data('ИНН\n.+?\n', 'ИНН.+?Страница \d+ из \n', bounds, 4, 1)
	result[key_words[8]]['Должность'] = extract_data('Должность.+?\n\d{,4}\n', 'Должность.+?Страница \d+ из \n', bounds, 10) # Сведения о директоре
	bounds['end'] = len(text)

	bounds['end'] = text.find('Сведения о видах экономической деятельности', bounds['start'])
	index = text.find('Сведения о держателе реестра акционеров акционерного общества', bounds['start'], bounds['end'])
	if(index != -1):
		old_start  = bounds['start']
		result[key_words[10]] = {}
		result[key_words[10]]['ОГРН'] = extract_data('\nОГРН\n\d{13}','\nОГРН\n\d{13}', bounds, 6, 0)
		result[key_words[10]]['ИНН'] = extract_data('ИНН\n\d{10}', 'ИНН\n\d{10}', bounds, 4, 0)
		result[key_words[10]]['Полное наименование'] = extract_data('Полное наименование.+?\n\d{,4}\n',
																 'Полное наименование.+?Страница \d+ из \n', bounds, len(key_words[0]) + 1)
		bounds['end'] = index
		bounds['start'] = old_start
	global_end = bounds['end'] # Сведения о держателе реестра акционеров акционерного общества

	result[key_words[9]] = {}
	counter = 1
	found = find_data('\n' + str(counter) + '\n\d{,4}\nГРН и дата внесения в ЕГРЮЛ сведений о',
					  '\n' + str(counter) + '\nСтраница \d+ из \n.+?ГРН и дата внесения в ЕГРЮЛ сведений о', bounds['start'], global_end)

	if(found is not None):
		bounds['start'] += found.end()
		counter += 1
		found = find_data('\n' + str(counter) + '\n\d{,4}\nГРН и дата внесения в ЕГРЮЛ сведений о',
					  '\n' + str(counter) + '\nСтраница \d+ из \n.+?ГРН и дата внесения в ЕГРЮЛ сведений о', bounds['start'], global_end)
		bounds['end'] = bounds['start'] + found.end()
	counter = 2
	while(bounds['start'] < global_end):
		result[key_words[9]][counter - 1] = {}
		found = find_data('\nОГРН\n\d{13}', '\nОГРН\n\d{13}', bounds['start'], bounds['end'])
		if(found is None):
			result[key_words[9]][counter - 1]['Фамилия'] = extract_data('Фамилия.+?\n\d{,4}\n', 'Фамилия.+?Страница \d+ из \n', bounds, 8)
			result[key_words[9]][counter - 1]['Имя'] = extract_data('Имя.+?\n\d{,4}\n', 'Имя.+?Страница \d из \n', bounds, 4)
			result[key_words[9]][counter - 1]['Отчество'] = extract_data('Отчество.+?\n\d{,4}\n', 'Отчество.+?Страница \d+ из \n', bounds, 9)
			result[key_words[9]][counter - 1]['ИНН'] = extract_data('ИНН\n\d{10}', 'ИНН\n\d{10}', bounds, 4, 0)
		else:
			result[key_words[9]][counter - 1]['ОГРН'] = extract_data('\nОГРН\n\d{13}','\nОГРН\n\d{13}', bounds, 6, 0)
			result[key_words[9]][counter - 1]['ИНН'] = extract_data('ИНН\n\d{10}', 'ИНН\n\d{10}', bounds, 4, 0)
			result[key_words[9]][counter - 1]['Полное наименование'] = extract_data('Полное наименование.+?\n\d{,4}\n',
																			  'Полное наименование.+?Страница \d+ из \n', bounds, len(key_words[0]) + 1)
	
		
		result[key_words[9]][counter - 1]['Номинальная стоимость доли'] = extract_data('Номинальная стоимость доли \(в рублях\)\n\d+\n',
																					 'Номинальная стоимость доли \(в рублях\)\n\d+\n', bounds,
																					 38, 1)
		bounds['start'] = bounds['end']
		counter += 1
		found = find_data('\n' + str(counter) + '\n\d{,4}\nГРН и дата внесения в ЕГРЮЛ сведений о',
					  '\n' + str(counter) + '\nСтраница \d+ из \n.+?ГРН и дата внесения в ЕГРЮЛ сведений о', bounds['start'], global_end)
		if(found is None):
			bounds['end'] = global_end
		else:
			bounds['end'] = bounds['start'] + found.end() # Сведения об участниках
	bounds['end'] = len(text)

	result[key_words[11]] = extract_data('Код и наименование вида деятельности.+?\n\d{,4}\n',
										 'Код и наименование вида деятельности.+?Страница \d+ из \n', bounds, 37) # Сведения об основном виде деятельности
	return result

