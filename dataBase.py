from sqlalchemy import create_engine,text,Column,String,Integer #Importa os métodos necessarios do sqlalchemy
from sqlalchemy.ext.declarative import declarative_base #Importa os métodos necessarios do sqlalchemy
from flask_login import LoginManager,login_user,current_user,logout_user #Importa os métodos necessarios do flask login

engine=create_engine("sqlite:///games.sqlite") #Cria engine que conecta ao banco de dados
connect=engine.connect() #Cria conexão como o banco de dados
base=declarative_base() #Cria uma base declarativa
lm=LoginManager() #Cria um manuseador de login

class game(base): #Cria uma classe para conectar com tabela de jogos
    __tablename__="Games" #Marca o nome dtabela que deve ser utuilizada 
    id=Column(Integer,primary_key=True) #Liga a informação de id com sua coluna de mesmo nome. Marca como chave primaria
    name=Column(String) #Liga a informação de nome com sua coluna de mesmo nome.
    plataform=Column(String) #Liga a informação de plataforma com sua coluna de mesmo nome.
    producer=Column(String) #Liga a informação de produtora com sua coluna de mesmo nome.
    date=Column(String) #Liga a informação de data de lançamento com sua coluna de mesmo nome.
    genre=Column(String) #Liga a informação de genero com sua coluna de mesmo nome.

class user(base): #Cria uma classe para conectar com tabela de usuarios
    __tablename__="users" #Marca o nome dtabela que deve ser utuilizada 
    name=Column(String,primary_key=True) #Liga a informação de nome com sua coluna de mesmo nome.
    access=Column(String) #Liga a informação de acesso com sua coluna de mesmo nome.
    email=Column(String) #Liga a informação de email com sua coluna de mesmo nome.
    password=Column(String) #Liga a informação de senha com sua coluna de mesmo nome.
    @property 
    def is_authenticated(self): #Função do manuseador de login que é chamada quando o usuario está logado
        return True 
    @property 
    def is_active(self): #Função do manuseador de login que é chamada quando o usuario está ativo
        return True 
    @property 
    def is_anonymous(self): #Função do manuseador de login que é chamada quando o usuario não está logado
        return False 
    def get_id(self): #Função do manuseador de login que retorna o id do usuario
        return self.name #Define o id do usuario como o seu nome
    def __repr__(self): #Função executada quando o objeto é lido do banco de dados
        return self.name #Retorna o nome do usuario