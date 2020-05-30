import fitz

# путь и массив ключевых слов
def find_key_words(path, key_words):
    not_found = []
    document = fitz.open(path)
    if not document.isPDF:
        pdfbytes = document.convertToPDF()
        document = fitz.open("pdf", pdfbytes)
    for i in range(len(key_words)):
        flag = False
        for current_page in range(len(document)):
            page = document.loadPage(current_page)
            quads = page.searchFor(key_words[i], hit_max = 10, quads = True)
            anotation = page.addHighlightAnnot(quads)
            if anotation is not None:
                anotation.setColors({"stroke":(0, 1, 0)})
                anotation.update()
                flag = True
        if not flag:
            not_found.append(key_words[i])
    document.save("Processed_" + path)
    document.close()
    return not_found