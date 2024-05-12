from flask import Flask, send_file, request
import os

app = Flask(__name__)
file_path = "media\youtube\Kamisama ni Natta Hi ED.mp3"

@app.route('/download')
def download_file():
    # Dapatkan ukuran total file
    total_size = os.path.getsize(file_path)

    # Dapatkan rentang yang diminta oleh klien
    range_header = request.headers.get('Range', None)
    start, end = 0, total_size - 1

    if range_header:
        try:
            # Ambil nilai rentang dari header
            _, range_values = range_header.split('=')
            start, end = map(int, range_values.split('-'))
        except ValueError:
            pass

    # Hitung panjang konten yang akan dikirim
    content_length = end - start + 1

    # Konfigurasikan header tanggapan
    headers = {
        'Content-Range': f'bytes {start}-{end}/{total_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': content_length
    }

    # Buka file dan kirimkan bagian yang diminta
    with open(file_path, 'rb') as f:
        f.seek(start)
        data = f.read(content_length)

    return send_file(
        data,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name=f'file_part_{start}_{end}.txt',
        headers=headers
    )

if __name__ == "__main__":
    app.run(debug=True)
