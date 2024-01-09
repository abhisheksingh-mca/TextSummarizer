import tkinter as tk
from tkinter import scrolledtext
import bs4 as bs
import urllib.request as url
import re
import nltk 
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import heapq
from string import punctuation

class WikipediaArticleSummaryApp:
    def __init__(self, root):
        self.root = root
       
        self.root.title("Text Sumaraizer")

        self.root.configure(bg='#CBE1EF')  # Background color
        title_font = ("Helvetica", 18, "bold")
        label_font = ("Helvetica", 12)
        label_font1 = ("Helvetica", 12, "bold")
        button_font = ("Helvetica", 12, "bold")

        self.title_label = tk.Label(root, text="Text Summuraizer", font=title_font, bg='#9ACDE0', fg='#0A568A', padx=10, pady=10)  # Background and foreground color, padding
        self.title_label.pack(fill=tk.X)

        self.url_label = tk.Label(root, text="Paste the URL link below 👇🏻:",font=label_font1, bg='#CBE1EF')
        self.url_label.pack(pady=(10,0))

        self.url_entry = tk.Entry(root, width=50, font=label_font)
        self.url_entry.insert(0, "https://www.geeksforgeeks.org/natural-language-processing-overview/")
        self.url_entry.pack(padx=5,pady=5)

        self.fetch_button = tk.Button(root, text="Fetch Article", command=self.fetch_article, font=button_font, bg='#5EA9BE', fg='white', pady=5)
        self.fetch_button.pack(pady=(10,0))

        self.summary_text = scrolledtext.ScrolledText(root, width=80,font=label_font, height=20,bg='#E6E6E6', fg='black', padx=10,pady=10)
        self.summary_text.pack(expand=True, fill=tk.BOTH, padx=10,pady=5)

    def fetch_article(self):
        url1 = self.url_entry.get()
        scraped_data = url.urlopen(url1)
        article = scraped_data.read()
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        paragraphs = parsed_article.find_all('p')
        article_text = ""
        for p in paragraphs:
            article_text += p.text

        # Add your text preprocessing and summary extraction code here
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords_list = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords_list and word not in punctuation:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
       
        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)

        # Display the summary in the GUI
        self.summary_text.delete(1.0, tk.END)  # Clear previous content
        self.summary_text.insert(tk.END, summary)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = WikipediaArticleSummaryApp(root)
    root.mainloop()
