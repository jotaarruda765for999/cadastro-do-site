from flask import Flask, render_template, request, redirect, url_for
import json
import os
import re
import bcrypt

app= Flask (__name__)
arquivo = 'usuarios.json'


#carregar dados
def carregar_dados():
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return []    
def salvar_dados(usuarios):
    with open(arquivo, 'w') as f:
        json.dump(usuarios,f,indent=4)

def email_valido(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None


@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    usuarios = carregar_dados()
    
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if not nome or not email or not senha:
        return render_template('todos os campos são obrigatorio. Tente novamente.')
        return

    if not email_valido(email):
        return render_template('Email inválido. Tente novamente.')
        return

    for user in usuarios:
        if user['email'] == email:
            return render_template('Esse email ja esta cadastrado. Tente novamente com outro email.')
            
            return
        
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())


    usuario = {
        'nome': nome,
        'email': email,
        'senha': senha_hash.decode('utf-8')
    }
    usuarios.append(usuario)
    salvar_dados(usuarios)
    return render_template('usuario_cadastrado.html')


@app.route('/login', methods=['POST'])
def login():
    usuarios= carregar_dados()
    
    email = request.form['email']
    senha = request.form['senha']

    for user in usuarios:
        if user['email'] == email :
            if bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
                return render_template('login_sucesso.html')
                return user
        if user['email'] == email:
            return render_template('login_sucesso.html')
        if not email or not senha:
           return render_template('Preencha todos os campos. Tente novamente.')
    
    return render_template('email ou senha incorretos. Tente novamente ')
    return None

@app.route('/deletar', methods=['POST'])
def deletar():
    usuarios = carregar_dados()

    email = request.form['email']
    senha = request.form['senha']

    for user in usuarios:

        if user['email'] == email and bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
            usuarios.remove(user)
            salvar_dados(usuarios)
            return render_template('usuario deletado com sucesso!')
            return


@app.route('/editar', methods=['POST'])
def editar():
    usuarios = carregar_dados()

    email = request.form['email']

    for user in usuarios:
        if user ['email'] == email:
            return render_template('usuario encontrado!')
        
        novo_nome = request.form['novo_nome']
        nova_senha = request.form['nova_senha']

        if novo_nome:
            user['nome'] = novo_nome
        if nova_senha:
            senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            user ['senha'] = senha_hash.decode('utf-8')
                 
        
        salvar_dados(usuarios)
        return render_template('usuario editado com sucesso!')
        return
    return render_template('usuario não encontrado.')

@app.route('/listar')
def listar():
    usuarios = carregar_dados()
    if not usuarios:
        return render_template('nenhum usuário cadastrado. ')
    for i, user in enumerate(usuarios, start=1):
        return render_template(f'{i}. Nome: {user["nome"]} - email: {user["email"]}')



def menu():
    while True:
        print('n/ sistema de usuarios:')
        print('1 cadastrar usuário')
        print('2 login')
        print('3 deletar usuário')
        print('4 editar usuário')
        print('5 listar usuários')
        print('6 sair')

        opcao = input('escolha uma opção: ')

        if opcao == '1':
            cadastrar()
        elif opcao == '2':
            login()
        elif opcao == '3':
            deletar()
        elif opcao == '4':
            editar()
        elif opcao == '5':
            listar()
        elif opcao == '6':
            print('saindo do sistema...')
            break
        else:
            render_template('opção inválida tente novamente.')


if __name__ == '__main__':
    app.run(debug=True)
    
        
        



