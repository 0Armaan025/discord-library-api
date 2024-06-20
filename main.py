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
    
    books = []
    for title in book_titles:
        book_name = title.get_text(separator=" ", strip=True)
        
        parent_td = title.find_parent('td')
        
        
        author_td = parent_td.find_next('td')
        author = author_td.get_text(separator=" ", strip=True) if author_td else "N/A"
        
        second_td = author_td.find_next('td')
        year = second_td.get_text(separator=" ", strip=True) if second_td else "N/A"
        
        
        fourth_td = parent_td.find_next('td')
        for _ in range(3):
            if fourth_td:
                fourth_td = fourth_td.find_next('td')
        
        language = fourth_td.get_text(separator=" ", strip=True) if fourth_td else "N/A"
        
        
        seventh_td = parent_td.find_next('td')
        for _ in range(6):  
            if seventh_td:
                seventh_td = seventh_td.find_next('td')
        
        
        
        file_link = seventh_td.find('a')['href'] if seventh_td and seventh_td.find('a') else "N/A"
        
        
        books.append({
            "title": book_name,
            "author": author,
            "year": year,
            "language": language,
            "file_link": file_link
        })
    
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
