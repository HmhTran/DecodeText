from factory import DecodeTextAppFactory

def printDoubleSpaced(msg):
    print(f"\n{msg}\n")

def main():
    app = DecodeTextAppFactory().build()
    app.run()

if __name__ == "__main__":
    main()
