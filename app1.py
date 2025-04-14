from flask import Flask, request, make_response
import os

app = Flask(__name__)
FLAG = os.getenv("FLAG", "CTF{FAKE_FLAG_123}")

def xor_encrypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

@app.route("/")
def home():
    username = request.args.get("user", "ctfkey42")
    key = username.encode()
    encrypted_flag = xor_encrypt(FLAG.encode(), key)
    cookie_value = encrypted_flag.hex()
    
    # HTML response with inline CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTF Challenge</title>
        <style>
            body {{
                background-color: #1a1a1a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }}
            .container {{
                background-color: #333;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                max-width: 600px;
            }}
            h1 {{
                font-size: 36px;
                margin-bottom: 20px;
                color: #00cc00;
            }}
            p {{
                font-size: 20px;
                line-height: 1.6;
            }}
            a {{
                color: #00ff99;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                color: #99ff99;
                text-decoration: underline;
            }}
            .highlight {{
                color: #ffcc00;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the CTF Challenge!</h1>
            <p>Hello, {username}! Your mission is to unlock the <span class="highlight">secret</span> hidden in your cookies.</p>
            <p><a href="/hint">Need a hint?</a></p>
        </div>
    </body>
    </html>
    """
    
    resp = make_response(html_content)
    resp.set_cookie("secret", cookie_value)
    return resp

@app.route("/hint")
def hint():
    # Hint page with same styling
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTF Hint</title>
        <style>
            body {
                background-color: #1a1a1a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            .container {
                background-color: #333;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                max-width: 600px;
            }
            h1 {
                font-size: 36px;
                margin-bottom: 20px;
                color: #00cc00;
            }
            p {
                font-size: 20px;
                line-height: 1.6;
            }
            a {
                color: #00ff99;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                color: #99ff99;
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hint</h1>
            <p>The secret is hex-encoded. Decode it to bytes, use the username as a key (repeat to 18 bytes), and convert to text.</p>
            <p><a href="/">Back to challenge</a></p>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)