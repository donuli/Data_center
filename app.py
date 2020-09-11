from datacenter import app

if __name__ == "__main__":
    db.create_all()
    app.secret_key = "123123123"
    app.run(host="0.0.0.0", port=80)
