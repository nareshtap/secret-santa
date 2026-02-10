from models.secret_santa_model import SecretSantaModel

def main():
    try:
        print("Welcome to the Secret Santa Assignment Application!")
        model = SecretSantaModel()
        model.run()
    except Exception as e:
        print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
