from flask import Flask, render_template, make_response, redirect, request 
import model
import view

app = Flask(__name__)

color_preferences_default = '{"W": 10, "U": 10, "B": 10, "R": 10, "G": 10}'
type_preferences_default = {'Phyrexian': 50, 'Dragon': 50}


@app.route('/')
def image_page():
  if type(request.cookies.get('color_preferences')) is str and type(request.cookies.get('type_preferences')) is str:
    print('damn')
    return render_template('stream.html', images=view.image_page(model.commander_page(request.cookies.get('color_preferences'), request.cookies.get('type_preferences'))))
  else:
    return render_template('stream.html', images=view.image_page(model.commander_page(color_preferences_default, type_preferences_default)))


@app.route('/set/<cookie>/<preferences>', methods=['POST', 'GET'])
def set_color_preferences(cookie, preferences):
  if request.method == 'POST':
    if cookie == 'color':
      if request.cookies.get('color_preferences'):
        color_preferences = request.cookies.get('color_preferences')
      else:
        color_preferences = ''
      resp = make_response(redirect('/'))
      resp.set_cookie('color_preferences', bytes(preferences, 'utf-8'))
      print(request.cookies.get('color_preferences'))
      return resp
    elif cookie == 'type':
      if request.cookies.get('type_preferences'):
        type_preferences = request.cookies.get('type_preferences')
      else:
        type_preferences = {'W': 1000, 'U': 10, 'B': 10, 'R': 10, 'G': 10}
      resp = make_response(redirect('/'))
      resp.set_cookie('type_preferences', bytes(preferences, 'utf-8'))
      print(request.cookies.get('type_preferences'))
      return resp

    
app.run(host='0.0.0.0', port=8080)
