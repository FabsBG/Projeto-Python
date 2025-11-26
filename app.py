from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from database import db, Pergunta, Post   
import os

app = Flask(__name__)

# CONFIGURAÇÕES
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_URI9A8dEWubh@ep-cool-wildflower-ad8a6rj9-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INICIALIZA O BANCO
db.init_app(app)

# FORMULÁRIOS

class PerguntaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    titulo = StringField('Título da Pergunta', validators=[DataRequired()])
    pergunta = TextAreaField('Sua Pergunta', validators=[DataRequired()])
    enviar = SubmitField('Enviar Pergunta')


class PostForm(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired()])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    enviar = SubmitField('Publicar Post')


class RespostaForm(FlaskForm):
    resposta = TextAreaField('Resposta', validators=[DataRequired()])
    enviar = SubmitField('Enviar Resposta')


# ROTAS

@app.route('/')
def index():
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas():
    form = PerguntaForm()
    if form.validate_on_submit():
        nova_pergunta = Pergunta(
            nome=form.nome.data,
            email=form.email.data,
            titulo=form.titulo.data,
            pergunta=form.pergunta.data
        )
        db.session.add(nova_pergunta)
        db.session.commit()
        flash('Pergunta enviada com sucesso!', 'success')
        return redirect(url_for('perguntas'))
    return render_template('perguntas.html', form=form)


@app.route('/admin')
def admin():
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()
    posts = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('admin.html', perguntas=perguntas, posts=posts)


@app.route('/responder/<int:pergunta_id>', methods=['GET', 'POST'])
def responder_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    form = RespostaForm()

    if form.validate_on_submit():
        pergunta.resposta = form.resposta.data
        pergunta.respondida = True
        db.session.commit()
        flash('Resposta enviada com sucesso!', 'success')
        return redirect(url_for('admin'))

    return render_template('responder.html', pergunta=pergunta, form=form)


@app.route('/novo-post', methods=['GET', 'POST'])
def novo_post():
    form = PostForm()
    if form.validate_on_submit():
        novo_post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            autor=form.autor.data
        )
        db.session.add(novo_post)
        db.session.commit()
        flash('Post publicado com sucesso!', 'success')
        return redirect(url_for('admin'))

    return render_template('novo_post.html', form=form)


@app.route('/deletar-pergunta/<int:pergunta_id>')
def deletar_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    db.session.delete(pergunta)
    db.session.commit()
    flash('Pergunta deletada com sucesso!', 'success')
    return redirect(url_for('admin'))


@app.route('/deletar-post/<int:post_id>')
def deletar_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deletado com sucesso!', 'success')
    return redirect(url_for('admin'))


# EXECUÇÃO

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
