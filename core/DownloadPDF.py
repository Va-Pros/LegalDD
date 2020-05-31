import requests
import json
import time

def downloadPDF(OGRN, out_file):
    sess = requests.session()
    url = 'https://egrul.nalog.ru/'
    data = {
        'query': OGRN,
        'vyp3CaptchaToken': ''
    }
    try:
        sess.get(url)
        response = sess.post(url, data=data)
        data = json.loads(response.text)
        while True:
            response = sess.get(url + 'search-result/' + data['t'])
            data = json.loads(response.text)
            if data.get('status') is None:
                token = data['rows'][0]['t']
                break
        response = sess.get(url + 'vyp-request/' + token)
        while True:
            response = sess.get(url + 'vyp-status/' + token)
            if json.loads(response.text)['status'] == 'ready':
                break
            time.sleep(0.05)
        response = sess.get(url + 'vyp-download/' + token)
        with open(out_file, 'wb') as fout:
            fout.write(response.content)
    except:
        return False
    sess.close()
    return True
