from app import create_app

# Initialize the app using the factory pattern
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)