from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-book/<name>')
def get_book(name):
    
    encoded_name = name.replace(' ', '+')
    
    
    url = f"https://libgen.rs/search.php?req={encoded_name}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"
    
    
    response = requests.get(url)
    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    
    book_titles = soup.select('td a[href^="book/index.php?md5="]')
    
    
    book_names = [title.get_text(separator=" ", strip=True) for title in book_titles]
    
    return jsonify(book_names)

if __name__ == '__main__':
    app.run(debug=True)
