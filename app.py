from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def cek_pajak_sleman(nomer, kode_belakang):
    url = "https://samsatsleman.jogjaprov.go.id/cek/pages/getpajak"
    data = {
        "nomer": nomer,
        "kode_belakang": kode_belakang
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://samsatsleman.jogjaprov.go.id/cek/pajak"
    }

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table-bordered")

        if not table:
            return None

        hasil = {}
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                hasil[key] = value
        return hasil
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        nomer = request.form.get('nomer')
        kode_belakang = request.form.get('kode_belakang')
        data = cek_pajak_sleman(nomer, kode_belakang)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
