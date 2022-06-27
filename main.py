from factory import DecodeTextAppFactory

def main():
    app = DecodeTextAppFactory().build()
    app.run()

if __name__ == "__main__":
    main()
