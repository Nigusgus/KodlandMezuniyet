from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    showers_per_day = int(request.form['showers_per_day'])
    shower_duration = int(request.form['shower_duration'])
    laundry_per_week = int(request.form['laundry_per_week'])
    hand_wash_dishes = request.form['hand_wash_dishes']
    shower_water_saving = request.form['shower_water_saving']
    meat_based_diet = request.form['meat_based_diet']
    toothbrush_water_saving = request.form['toothbrush_water_saving']
    saving_head = request.form['saving_head']
    garden_watering = request.form['garden_watering']
    leakage = request.form['leakage']

    # Ortalama litre/dk duş akışı
    litre_per_minute = 9
    if saving_head == 'yes':
        litre_per_minute *= 0.7

    total_litres = showers_per_day * shower_duration * litre_per_minute

    # Diş fırçalarken suyu kapatma tasarrufu (2 dk, 6 litre/dk)
    if toothbrush_water_saving == 'yes':
        total_litres -= 2 * 6 * 0.7

    # Bahçe sulaması litre ekle
    if garden_watering == 'yes':
        total_litres += 50

    # Sızıntı var ise litre ekle
    if leakage == 'yes':
        total_litres += 20

    # Çamaşır makinesi su tüketimi (haftalık litre ortalaması, günlük hesap)
    # Ortalama çamaşır başına 50 litre, haftalık -> günlük böl
    total_litres += (laundry_per_week * 50) / 7

    # Elde bulaşık yıkama, ortalama günlük 15 litre ekle
    if hand_wash_dishes == 'yes':
        total_litres += 15

    # Duş sırasında suyu kapatma alışkanlığı yoksa ekstra su tüketimi ekle
    if shower_water_saving == 'no':
        # Örneğin duş süresinin %10'u fazla su tüketimi olabilir
        extra = showers_per_day * shower_duration * litre_per_minute * 0.1
        total_litres += extra

    # Et ağırlıklı beslenme su ayak izi yüksek, ek su tüketimi (örnek 100 litre)
    if meat_based_diet == 'yes':
        total_litres += 100

    total_litres = round(total_litres, 2)

    return render_template('results.html', total_litres=total_litres)

if __name__ == '__main__':
    app.run(debug=True)