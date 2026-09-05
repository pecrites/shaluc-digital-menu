from flask import Flask, render_template, abort
import json, qrcode, socket

app=Flask(__name__)
LANGUAGES={"fr":"🇫🇷 Français","en":"🇬🇧 English","zh":"🇨🇳 中文","hi":"🇮🇳 हिन्दी"}

def load_menu():
    with open("data/menu.json",encoding="utf-8") as f: return json.load(f)

def lan_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(("8.8.8.8",80))
        ip=s.getsockname()[0]; s.close(); return ip
    except: return "127.0.0.1"

@app.route("/")
def index(): return render_template("index.html",languages=LANGUAGES)

@app.route("/menu/<language>")
def show_menu(language):
    if language not in LANGUAGES: abort(404)
    return render_template("menu.html",menu=load_menu(),language=language,language_name=LANGUAGES[language])

@app.route("/qr")
def qr(): return render_template("qr.html",qr_url=f"http://{lan_ip()}:5000/")

if __name__=="__main__":
    url=f"http://{lan_ip()}:5000/"
    qrcode.make(url).save("static/shalue_qr.png")
    print("PC     :", "http://127.0.0.1:5000")
    print("TELEPHONE (même Wi-Fi):", url)
    print("QR     : static/shalue_qr.png")
    app.run(host="0.0.0.0",port=5000,debug=True)
