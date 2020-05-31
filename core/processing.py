import fitz
import pymorphy2
import string
import pathlib
import win32com.client


# путь и массив ключевых фраз
def find_key_phrases(path_str, key_phrases):
    # ненайденные фразы
    not_found = []
    morph = pymorphy2.MorphAnalyzer()
    # нужен для создания обработанного файла в той же директории
    path = pathlib.Path(path_str).resolve()
    if(path.suffix != ".pdf"):
        if(path.suffix == ".doc" or path.suffix == ".docx"):
            # конвертация в пдф
            # 17 значит pdf
            wdFormatPDF = 17
            word = win32com.client.Dispatch('Word.Application')
            word_doc = word.Documents.Open(str(path))
            path = pathlib.Path(str(path.parent/path.stem) + ".pdf")
            word_doc.SaveAs(str(path), wdFormatPDF)
            word_doc.Close()
            word.Quit()
    document = fitz.open(path)
    # пунктуация, которую будем удалять
    punctuation = str.maketrans(dict.fromkeys(string.punctuation))
    # массив, каждый элемент которого равен массиву слов страницы
    array_words_pages = []
    # массив, каждый элемент которого равен массиву слов (в начальной форме) страницы
    array_normalized_words_pages = []
    # проход по всем страницам
    for current_page in range(len(document)):
        page = document.loadPage(current_page)
        temp_words = page.getText("words")
        array_words_pages.append([])
        # записываем массив слов текущей страницы в общий массив
        for i in range(len(temp_words)):
            array_words_pages[current_page].append(temp_words[i][4])

    # идем по всем страницам
    for current_page in range(len(array_words_pages)):
        array_normalized_words_pages.append([])
        # идем по всем словам на странице
        for elem in range(len(array_words_pages[current_page])):
            # записываем слово (в начальной форме), убирая перед этим пунктуацию
           array_normalized_words_pages[current_page].append(morph.parse(array_words_pages[current_page][elem].translate(punctuation))[0].normal_form)

    # идем по всем ключевым фразам
    for i in range(len(key_phrases)):
        # массив слов фразы
        words_phrase = key_phrases[i].split()
        # массив слов (в начальной форме) фразы без пунктуации
        normalized_words_phrase = []
        for j in range(len(words_phrase)):
            # переводим слова в начальную форму без пунктуации
            normalized_words_phrase.append(morph.parse(words_phrase[j].translate(punctuation))[0].normal_form)
        # флаг, показывает нашли фразу в тексте
        flag = False
        # содержит оригинальную фразу, которая соответствует найденной (в начальной форме)
        original_phrase = " "
        # индекс первого слова найденной фразы
        index = -1
        # производим поиск фразы (в начальной форме) в тексте (начальной формы)
        for current_page in range(len(document)):
            # проходим по словам текущей страницы
            for n in range(len(array_normalized_words_pages[current_page]) - len(normalized_words_phrase)):
                # проходим по словам фразы
                for m in range(len(normalized_words_phrase)):
                    # если соответствующие слова не равны
                    if(array_normalized_words_pages[current_page][n + m] != normalized_words_phrase[m]):
                        flag = False
                        index = -1
                        break
                    else:
                        flag = True
                        index = n
                # если нашли совпадение
                if(flag):
                    break
            # если фраза найдена на этой странице
            if(flag):
                # построим оригинал фразы
                original_phrase = original_phrase.join(array_words_pages[current_page][index:index + len(normalized_words_phrase)])
                # загружаем страницу, в которой нашли
                page = document.loadPage(current_page)
                # ищем на странице
                quads = page.searchFor(original_phrase, hit_max = 5, quads = True)
                # выделяем
                anotation = page.addHighlightAnnot(quads)
                # ставим зеленый цвет
                anotation.setColors({"stroke":(0, 1, 0)})
                anotation.update()
                break
        # если фраза не была найдена
        if not flag:
            # добавляем в ненайденные
            not_found.append(key_phrases[i])
    document.saveIncr()
    document.close()
    return not_found
