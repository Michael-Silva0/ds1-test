from flask import Flask, render_template, request


app = Flask(__name__) 


    
@app.route('/')
def home():
    #return "<h1>Servidos Flask rodando!</h1>" "<h1>Bem vindo ao meu servidor flask</h1>"
    return render_template("index.html")
    

@app.route('/sobre')
def sobre():
    return "<h1>Sobre a função</h1>" "<p>Esta é uma simples aplicação flask</p>"


@app.route('/status')
def status():
    return "<h1>Estatus da aplicação</h1>" "<p>O servidor esta rodando flask corretamente</p>"


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/salvar", methods=["POST"])
def salvar():
    nome_digitado = request.form.get("campo_nome")
    info_digitada = request.form.get("campo_info")

    return render_template("resultado.html", nome=nome_digitado, info=info_digitada)




if __name__ == '__main__':
    app.run(debug=True)
