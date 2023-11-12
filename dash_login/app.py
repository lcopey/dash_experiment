from login import ProtectedDash

app = ProtectedDash()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
