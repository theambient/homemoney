
import os.path
import flask
import mimetypes

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
VIEW_DIR = os.path.join(ROOT, 'view')

app = flask.Flask(__name__)

@app.route("/<path:path>")
def default_view(path):

    fullpath = os.path.join(VIEW_DIR, path)
    try:
        fd = open(fullpath)
        mime = mimetypes.guess_type(fullpath)[0]
        return fd.read(), 200, {'Content-Type': mime}
    except Exception:
        return 404

