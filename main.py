from flask import Flask, render_template, blueprints
from blueprints.videototexturl.url_blueprint import url_blueprint
from blueprints.videototextmp4.mp4_blueprint import mp4_blueprint
from blueprints.keywordsdescr.keydesc_blueprint import keydesc_blueprint
from blueprints.keywordsshort.keyshort_blueprint import keyshort_blueprint
from blueprints.keywordstfidf.keytfidf_blueprint import keytfidf_blueprint
from blueprints.genreskeywords.ge_ke_blueprint import ge_ke_blueprint
from blueprints.genretext.genretext_blueprint import genretext_blueprint

# from blueprints

app = Flask(__name__)

# Register Blueprints for each disease model
app.register_blueprint(url_blueprint, url_prefix='/videototexturl')
app.register_blueprint(mp4_blueprint, url_prefix='/videototextmp4')
app.register_blueprint(ge_ke_blueprint, url_prefix="/genreskeywords")
app.register_blueprint(keydesc_blueprint, url_prefix='/keywordsdecsr')
app.register_blueprint(keyshort_blueprint, url_prefix='/keywordsshort')
app.register_blueprint(keytfidf_blueprint, url_prefix='/keywordstfidf')
app.register_blueprint(genretext_blueprint, url_prefix="/genretext")





# Register other Blueprints as needed
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)