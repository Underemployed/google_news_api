from api.app import app
import nltk
nltk.download('punkt')

if __name__ == '__main__':
    app.run(debug=True)
