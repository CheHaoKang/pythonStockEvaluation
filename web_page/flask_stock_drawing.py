import sys, os
from flask import Flask, render_template
from flask import request
import glob


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def user():
    png_files = []
    for png_file in glob.glob('static/stockDrawing_*.png'):
        png_files.append(png_file.replace('\\', '/').replace('static/', ''))

    print(png_files)
    return render_template('stock_drawing.html', png_files=png_files)

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')