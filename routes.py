# importamos la instancia de Flask (app)
from apptrivia import app, admin_permission
import os, random, datetime

# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, Usuario
from flask import render_template, session, request, redirect, url_for, jsonify, abort, flash, g, current_app
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms.login import LoginForm
from forms.register import RegisterForm
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException
from flask_principal import AnonymousIdentity, RoleNeed, UserNeed, Identity, identity_loaded, identity_changed

# para poder usar Flask-Login
login_manager = LoginManager(app)
login_manager.init_app(app)

#le ponemos a fuerza el identity del usuario que está logueado. Se llama antes de c/request
@app.before_request
def before_request():
	#Si está logueado
    if hasattr(current_user, 'id'):
        g.identity = Identity(current_user.id)
        app_actual = current_app._get_current_object()			#la app actual es Flask
        identity_changed.send(app_actual, identity=Identity(current_user.id))
    else:
        g.identity = AnonymousIdentity


@app.route('/trivia')
def index():
    session.modified = True
    session['completas'] = {}
    session['tiempo'] = datetime.datetime.now()
    return render_template('home.html')
    #return "<h1>BIENVENIDO TERRÍCOLA</h1></br><div><h3><a href='/trivia/categorias'>¡Comienza a jugar!</a></h3></div>"


@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    categorias = Categoria.query.all()
    respond = session['completas']
    ids = []
    ind = 0;
    if (respond != None):
        for r in respond:
            catId = r[r.index("_")+1: len(r)]
            #ids[ind]
            #ind += 1
    return render_template('categorias.html', categorias=categorias, respondidas=ids)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarrespuesta(id_pregunta, id_respuesta):
    pregunta = Pregunta.query.get(id_pregunta)
    respuesta = Respuesta.query.get(id_respuesta)
    categCompletas = session['completas']
    if respuesta.correcta:
       # categCompletas = session['completas']
        if categCompletas is None:
            categCompletas = {"categ_" + str(pregunta.categoria_id), "OK"}
            session['completas'] = categCompletas
        else:
            categCompletas["categ_" + str(pregunta.categoria_id)] = "OK"
            session['completas'] = categCompletas

            cantCateg = Categoria.query.all()
            if len(cantCateg) == len(categCompletas):
                #ganaste
                return redirect(url_for('ganaste'))

    return render_template('respuestas.html', pregunta=pregunta, respuesta=respuesta)


@app.route('/trivia/ganaste', methods=['GET'])
def ganaste():
    tiempo = datetime.datetime.now() - session['tiempo']
    session['completas'] = None
    return render_template('ganaste.html', tiempo=tiempo)


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))


@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@app.route('/trivia/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(name=username, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


""" manejo de errores """

@app.errorhandler(404)
def page_not_found(e):
    #return jsonify(error=str(e)), 404
    return render_template('404.html')


@app.errorhandler(401)
def unathorized(e):
    return render_template('401.html')
    #return jsonify(error=str(e)), 404


@app.errorhandler(403)
def unathorized(e):
    return render_template('403.html')


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), e.code


""" Flask-Principal"""

# Flask-Principal: Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user

    # Agregamos una UserNeed a la identidad, con el id del usuario actual.
    if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))



@app.route('/test')
@login_required
@admin_permission.require(http_exception=403)
def test_principal():
    return render_template('test.html')