from flask import Flask, render_template_string, send_file
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

app = Flask(__name__)

# Öğrenci bilgileri
student_info = {
    "isim": "Nursena",
    "soyisim": "Altın",
    "ogrenci_no": "211213058"
}

# Rastgele noktalar ve grid görselleştirme fonksiyonu
def create_random_dots():
    num_points = 1000
    min_value = 0
    max_value = 1000
    grid_size = 200
    colors = np.random.rand(max_value // grid_size, max_value // grid_size, 3)
    x_coords = np.random.randint(min_value, max_value + 1, num_points)
    y_coords = np.random.randint(min_value, max_value + 1, num_points)

    df = pd.DataFrame({
        'X': x_coords,
        'Y': y_coords
    })

    buf = io.BytesIO()
    fig, ax = plt.subplots()

    for i in range(min_value, max_value, grid_size):
        for j in range(min_value, max_value, grid_size):
            mask = (x_coords >= i) & (x_coords < i + grid_size) & (y_coords >= j) & (y_coords < j + grid_size)
            points_in_grid = df[mask]
            if not points_in_grid.empty:
                ax.scatter(points_in_grid['X'], points_in_grid['Y'], c=[colors[i // grid_size][j // grid_size]], label=f'Grid {i // grid_size}, {j // grid_size}')

    ax.set_xlabel('X Koordinatları')
    ax.set_ylabel('Y Koordinatları')
    ax.set_title(f'Rastgele Noktaların Görselleştirilmesi (Grid Size: {grid_size}x{grid_size})')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@app.route('/')
def home():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ödev 7 - Renkli Noktalar</title>
        <style>
            body {{
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            .header {{
                margin-top: 20px;
            }}
            .content {{
                margin-top: 40px;
            }}
            .footer {{
                margin-top: 40px;
            }}
        </style>
        <script>
            function refreshImage() {{
                var img = document.getElementById('random-dots-image');
                img.src = '/generate_image?' + new Date().getTime();
            }}
        </script>
    </head>
    <body>
        <div class="header">
            <h1>Öğrenci Bilgileri</h1>
            <p>İsim: {student_info['isim']}</p>
            <p>Soyisim: {student_info['soyisim']}</p>
            <p>Öğrenci Numarası: {student_info['ogrenci_no']}</p>
        </div>
        <div class="content">
            <h2>Rastgele Noktalar</h2>
            <img id="random-dots-image" src="{{{{ url_for('generate_image') }}}}" alt="Rastgele Noktalar">
        </div>
        <div class="footer">
            <button onclick="refreshImage()">Yeni Görsel Oluştur</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/generate_image')
def generate_image():
    buf = create_random_dots()
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
