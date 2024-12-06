from flask import Flask, request, render_template
import hashlib
import time

app = Flask(__name__)

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def dictionary_attack(target_hash, dictionary_file):
    attempts = 0
    start_time = time.time()

    with open(dictionary_file, 'r') as file:
        for line in file:
            attempts += 1
            word = line.strip()
            hashed_word = hash_password(word)
            if hashed_word == target_hash:
                end_time = time.time()
                return word, attempts, end_time - start_time

    return None, attempts, None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        target_hash = request.form['hash']
        dictionary_file = 'dict.txt'
        cracked_password, attempts, duration = dictionary_attack(target_hash, dictionary_file)
        if cracked_password:
            result = {
                'password': cracked_password,
                'attempts': attempts,
                'duration': duration
            }
        else:
            result = {
                'password': None,
                'attempts': attempts
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
