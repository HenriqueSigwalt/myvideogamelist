from flask import Flask,render_template,request,redirect,url_for #Importa os métodos necessarios do flask
from dataBase import * #Importa todas as informações do arquivo database, onde é feito a declaração do banco de dados
from sqlalchemy.orm import sessionmaker #Importa os métodos necessarios do sqlalchemy
import os #Importa a biblioteca os

Session=sessionmaker(bind=connect) #Cria uma seção de conecção com o banco de dados
session=Session() #liga essa seção a uma variavel
app=Flask(__name__) #Cria o aplicativo com flask
lm.init_app(app) #Inicializa o manuseador de login para o aplicativo
app.secret_key="Secreto" #cria uma chave secreta

@lm.user_loader 
def load_user(id): #Função do manuseador de login que carrega o usuario atual baseado no id dele
    return session.get(user,ident=id) #Pega o usuario atravez do id. Primeiro parametro é o banco de dados onde o usuario se encontra. Segundo é o id recebido pela função

@app.route("/") #Cria rota padrão de quando o aplicativo é aberto
def begin(): #Função chamada ao entrar na página
    logout_user() #Garante que nenhum usuario permanece logado de ua sessão anterior
    return redirect(url_for('landing')) #Redireciona para a pagina inicial do site

@app.route("/home",methods=["POST","GET"]) #Cria a rota para a página inicial do site
def landing(): #Função chamada ao entrar na página
    games=session.query(game).all() #Recebe uma lista dos jogos no banco de dados
    pathway=request.form #Recebe as informações passadas pelo formulario
    if "create" in pathway: #Se o formulario veio da págia de criação de conta
        use=session.query(user).filter_by(name=pathway["name"]).first() #Procura no banco de dados por um usuario com o nome passado pelo formulario
        if (pathway["password"]==pathway["confirm"]) and (not use): #Se os campos senha e confirmar senha são iguais e não existe um usuario com esse nome
            newUser=user(name=pathway["name"],access="user",password=pathway["password"],email=pathway["email"]) #Cria um novo usuario para o banco de dados com as informações passadas pelo formulario
            session.add(newUser) #Adiciona o usuario ao banco de dados
            session.commit() #Atualiza o banco de dados
            login_user(newUser) #Função do manuseador de login que marca o novo usuario como logado
            return render_template("landing.html",game=games) #Vai para a página inicial
        else: #Se as informações estavam incorretas
            return render_template("create.html") #Vai para a página de criação de conta
    elif "log" in pathway: #Se o formulario veio da página de login
        use=session.query(user).filter_by(name=pathway["name"]).first() #Procura no banco de dados por um usuario com o nome passado pelo formulario
        if (use) and (use.password==pathway["password"]): #Se existe um usuario com o nome informado é a senha é igual a marcada no banco de dados
            login_user(use) #Função do manuseador de login que marca o usuario como logado
            return render_template("landing.html",game=games) #Vai para a página inicial
        else: # Se as informações passadas forem incorretas
            return render_template("login.html") #Vai para página de login
    else:#Se nenhum formulario foi recebido ou se ele veio de outro local do site
        return render_template("landing.html",game=games) #Vai para a página inicial

@app.route("/direct",methods=["POST"]) #Cria rota para a pagina que direciona os botões da página inicial
def direct(): #Função chamada ao entrar na página
    games=session.query(game).all() #Recebe uma lista dos jogos no banco de dados
    pathway=request.form #Recebe as informações passadas pelo formulario
    if "createAccount" in pathway: #Se o botão apertado foi o de criação de conta
        return render_template("create.html") #Vai para a página de criação de conta
    if "login" in pathway: #Se o botão apertado foi o de login
        return render_template("login.html") #Vai para a página de login
    if "logout" in pathway: #Se o botão apertado foi o de logout
        logout_user() #Desliga o usuario
        return render_template("landing.html",game=games) #Vai para a página inicial
    else: #Se o botão apertado foi o de perfil
        return redirect(url_for("admin")) #Vai para a página de perfil

@app.route("/admin",methods=["POST","GET"]) #Cria uma rota para lidar com os botões que levam a página de perfil
def admin(): #Função chamada ao entrar na página
    games=session.query(game).all() #Recebe uma lista dos jogos no banco de dados
    pathway=request.form #Recebe as informações passadas pelo formulario
    if "add" in pathway: #Se o botão apertado foi o da página de adicionar novo jogo
        if games!=[]: #Se a lista de jogos não estiver vazia
            newId=games[-1].id+1 #O id do novo jogo é marcado como um a mais que o do ultimo jogo adicionado
        else: #Caso a lista de jogos estiver vazia
            newId=1 #O id do novo jogo é marcado como 1
        newGame=game(id=newId,name=pathway["name"],plataform=pathway["plataform"],producer=pathway["producer"],date=pathway["date"],genre=pathway["genre"]) #Cria um novo jogo para o banco de dados com so dados passasdos pelo formulario
        session.add(newGame) #adiciona o novo jogo ao banco de dados
    if "remove" in pathway: #Se o botão apertado foi o da página de deletar jogo
        session.query(game).filter_by(id=pathway["name"]).delete() #Deleta o jogo escolhido pelo usuario
    if "edit" in pathway: #Se o botão apertado foi o da página de editar um jogo
        session.query(game).filter_by(id=pathway["name"]).update({pathway["atribute"]:pathway["change"]}) #Altera um valor do jogo para uma nova informação. O valor a ser alterado, jogo e a nova informação são recebidas do formulario
    session.commit() #Atualiza o banco de dados
    return render_template("admin.html") #Vai para a página de perfil

@app.route("/change",methods=["POST"]) #Cria uma rota para a os botões da página de perfil
def change(): #Função chamada ao entrar na página
    pathway=request.form #Recebe as informações passadas pelo formulario
    games=session.query(game).all() #Recebe uma lista dos jogos no banco de dados
    if "new" in pathway: #Se o botão apertado foi de criar novo jogo
        return render_template("new.html") #Vai para a página de adicionar novo jogo
    elif "delete" in pathway: #Se o botão apertado foi o de deletar jogo
        return render_template("delete.html",games=games) #Vai para a página de deletar jogo
    else: #Se o botão apertado foi o de editar jogo
        return render_template("edit.html",games=games) #Vai para a página de editar jogo

@app.route("/show/<id>",methods=["POST","GET"]) #Cria rota para as páginas individuais dos jogos. Recebe o nome do jogo como parametro
def show(id): #Função chamada ao entrar na página
    games=session.query(game).filter_by(name=id).first() #Procura o jogo escolhido no banco de dados
    return render_template("show.html",game=games) #Vai para a página de mostrar jogo, passando as informações do jogo escolhido como parametro