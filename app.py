from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import tempfile
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'edicoes_audio.json'
UPLOAD_FOLDER = tempfile.mkdtemp()

def carregar():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar(dados):
    with open(DB_FILE, 'w') as f:
        json.dump(dados, f, indent=2)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "api": "Clipador - Edição de Áudio Profissional",
        "versao": "2.1.0",
        "status": "online",
        "recursos": [
            "cortar", "velocidade", "tom", "fade_in_out",
            "converter", "extrair_audio", "normalizar",
            "reverb", "eco", "remover_voz", "silenciar",
            "inverter", "loop"
        ]
    })

@app.route('/api/audio/cortar', methods=['POST'])
def cortar():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    inicio = request.form.get('inicio', '0')
    duracao = request.form.get('duracao', '30')
    formato = request.form.get('formato', 'mp3')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, f'cortado.{formato}')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-ss', inicio, '-t', duracao,
           '-c', 'copy', temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'cortado.{formato}')

@app.route('/api/audio/velocidade', methods=['POST'])
def velocidade():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    fator = request.form.get('fator', '1.5')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, f'speed_{fator}x.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-filter:a', f'atempo={fator}',
           '-vn', temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'speed_{fator}x.mp3')

@app.route('/api/audio/tom', methods=['POST'])
def tom():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    semitons = request.form.get('semitons', '2')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, f'pitch_{semitons}.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af', f'rubberband=pitch={semitons}',
           '-q:a', '2', temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'pitch_{semitons}.mp3')

@app.route('/api/audio/fade', methods=['POST'])
def fade():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    fade_in = request.form.get('fade_in', '2')
    fade_out = request.form.get('fade_out', '2')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'fade.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af',
           f'afade=t=in:ss=0:d={fade_in},afade=t=out:st=999999:d={fade_out}',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='fade.mp3')

@app.route('/api/audio/converter', methods=['POST'])
def converter():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    formato = request.form.get('formato', 'mp3')
    qualidade = request.form.get('qualidade', '320k')
    
    codecs = {'mp3': 'libmp3lame', 'aac': 'aac', 'ogg': 'libvorbis', 'flac': 'flac', 'wav': 'pcm_s16le'}
    codec = codecs.get(formato, 'libmp3lame')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}')
    temp_output = os.path.join(UPLOAD_FOLDER, f'convertido.{formato}')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-c:a', codec, '-b:a', qualidade, temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'convertido.{formato}')

@app.route('/api/audio/extrair', methods=['POST'])
def extrair():
    if 'video' not in request.files:
        return jsonify({"erro": "Vídeo não enviado"}), 400
    
    file = request.files['video']
    formato = request.form.get('formato', 'mp3')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp4')
    temp_output = os.path.join(UPLOAD_FOLDER, f'audio.{formato}')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-vn', '-ar', '44100', '-ac', '2',
           '-b:a', '320k', temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'audio.{formato}')

@app.route('/api/audio/normalizar', methods=['POST'])
def normalizar():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'normalizado.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af', 'loudnorm=I=-16:LRA=11:TP=-1.5',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='normalizado.mp3')

@app.route('/api/audio/reverb', methods=['POST'])
def reverb():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'reverb.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af',
           'aecho=0.8:0.7:40:0.5,aecho=0.8:0.7:80:0.3',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='reverb.mp3')

@app.route('/api/audio/eco', methods=['POST'])
def eco():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    delay = request.form.get('delay', '300')
    decay = request.form.get('decay', '0.5')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'eco.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af',
           f'aecho=0.8:{decay}:{delay}:{decay}',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='eco.mp3')

@app.route('/api/audio/remover-voz', methods=['POST'])
def remover_voz():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'karaoke.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af', 'pan=stereo|c0=c0-c1|c1=c0-c1',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='karaoke.mp3')

@app.route('/api/audio/silenciar', methods=['POST'])
def silenciar():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    inicio = request.form.get('inicio', '1')
    duracao = request.form.get('duracao', '2')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'silenciado.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af',
           f'volume=0:enable=\'between(t,{inicio},{float(inicio)+float(duracao)})\':volume=1',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='silenciado.mp3')

@app.route('/api/audio/inverter', methods=['POST'])
def inverter():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, 'invertido.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-af', 'areverse', temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name='invertido.mp3')

@app.route('/api/audio/loop', methods=['POST'])
def loop():
    if 'audio' not in request.files:
        return jsonify({"erro": "Áudio não enviado"}), 400
    
    file = request.files['audio']
    repeticoes = request.form.get('repeticoes', '3')
    
    temp_input = os.path.join(UPLOAD_FOLDER, f'input_{datetime.now().timestamp()}.mp3')
    temp_output = os.path.join(UPLOAD_FOLDER, f'loop_{repeticoes}x.mp3')
    file.save(temp_input)
    
    cmd = ['ffmpeg', '-i', temp_input, '-filter_complex',
           f'aloop=loop={repeticoes}:size=2e9',
           temp_output, '-y']
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    return send_file(temp_output, as_attachment=True, download_name=f'loop_{repeticoes}x.mp3')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5016))
    app.run(host='0.0.0.0', port=port, debug=False)
