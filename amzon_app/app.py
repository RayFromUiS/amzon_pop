"""
test case on how to render plot from matplotlib
"""
from flask import Flask, send_file, make_response
from plots.test import do_test_plot

app = Flask(__name__)

@app.route('/', methods=['GET'])
def correlation_matrix():
    bytes_obj = do_test_plot()

    return send_file(bytes_obj,
                     # attachment_filename='plot.png',
                     mimetype='image/png')

if __name__ == "__main__":
    import webbrowser
    # webbrowser.open("localhost:5001")
    app.run(debug=True)