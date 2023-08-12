from flask import Flask, request, render_template, session, send_file, url_for, redirect
import techriotrsa # self created module

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = "place_secret_key_here"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            keysize = int(request.form['keysize'])
            techriotrsa.keygen(keysize)
            session["keys_generated"] = True
            with open('keypair/private.pem', "r") as file:
                prv_key = file.read()
            with open('keypair/public.pem', "r") as file:
                pub_key = file.read()
            return render_template("index.html", private_key="private.pem", prv_key=prv_key, pub_key=pub_key)
        except:
            return render_template("index.html", error="ERROR: No key size selected!")
    return render_template("index.html")

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == "POST":
        plaintext = request.form.get('plaintext')
        pubkey = request.form.get('pubkey')
        scrambled = techriotrsa.encrypt(pubkey, plaintext)
        return render_template("encrypt.html", scrambled=scrambled)
    
    return render_template("encrypt.html")

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == "POST":
        ciphertext = request.form.get('scrambledtext')
        prvkey = request.form.get('prvkey')
        plaintext = techriotrsa.decrypt(prvkey, ciphertext)
        return render_template("decrypt.html", plaintext=plaintext)
    return render_template("decrypt.html")

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get("keys_generated"):
        return redirect(url_for("/"))
    return send_file(path_or_file="keypair/"+filename, as_attachment=True)

if __name__ == "__main__":
    app.run(port=4500)
