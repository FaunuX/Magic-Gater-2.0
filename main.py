from flask import Flask, render_template, make_response, redirect, request, jsonify
import model

app = Flask(__name__)

color_preferences_default = '{"W":10,"U":10,"B":10,"R":10,"G":10}'
type_preferences_default = '{}'

cardpicker = model.recommendationEngine(color_preferences_default, type_preferences_default)


@app.route('/stream/')
def image_page():
  if type(request.cookies.get('color_preferences')) is str and type(request.cookies.get('type_preferences')) is str:
    cardpicker.color_preferences = request.cookies.get('color_preferences')
    cardpicker.type_preferences = request.cookies.get('type_preferences')
  else:
    cardpicker.color_preferences = color_preferences_default
    cardpicker.type_preferences = type_preferences_default
  cards = cardpicker.commander_page(10)
  return render_template('stream.html', card_data=cards, tab_classes=['', 'active_tab', ''])


@app.route('/set/<pon>/<commander_data>', methods=['POST', 'GET'])
def set_color_preferences(pon, commander_data):
  print('popopopopopopooop')
  if request.method == 'POST':
    cardpicker.model.add_data(cardpicker.generate_commander_input(cardpicker.cooked_data(commander_data)), pon)
    for i in range(10):
      cardpicker.model.evolve()
    resp = make_response()
    if request.cookies.get("saved"):
      saved = request.cookies.get("saved")
    else:
      saved = []
    if pon == 1:
      saved.append(commander_data)
    print(saved)
    print("spam")
    resp.set_cookie("saved", saved)
    return resp

@app.route('/')
def home():
  return render_template('home.html', tab_classes=['active_tab', '', ''])

@app.route('/api/new_cmdrs/')
def new_commanders():
  return jsonify(cardpicker.commander_page(8))

@app.errorhandler(404)
def fourohfour(e):
  return render_template('404.html', tab_classes=['', '', ''])

@app.route('/saved/')
def saved():
  print(request.cookies.get('saved'))
  return render_template('saved.html', commander_data=request.cookies.get('saved'), tab_classes=['', '', ''])
  
    
app.run(host='0.0.0.0', port=8080)
