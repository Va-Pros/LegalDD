import io
import multiprocessing
import numpy

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def preprocess_text(text):
	tokens = mystem.lemmatize(text.lower())
	tokens = [token for token in tokens if token not in russian_stopwords\
	and token != " " \
	and token.strip() not in punctuation]
	text = " ".join(tokens)
	return text

def extract_text_from_pdf(pdf_path):
	resource_manager = PDFResourceManager()
	fake_file_handle = io.StringIO()
	converter = TextConverter(resource_manager, fake_file_handle)
	page_interpreter = PDFPageInterpreter(resource_manager, converter)

	with open(pdf_path, 'rb') as fh:
		for page in PDFPage.get_pages(fh, caching = True,check_extractable = True):
			page_interpreter.process_page(page)

	text = fake_file_handle.getvalue()

	converter.close()
	fake_file_handle.close()

	if text:
		return text

text = preprocess_text(extract_text_from_pdf('w.pdf'))
cores = multiprocessing.cpu_count()
arrWords = text.split()
w2v_model = Word2Vec([arrWords], min_count = 1, size = 300, workers = cores - 1)
print(w2v_model.wv[arrWords].mean(axis = 0))
