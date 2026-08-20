from flask import Flask, render_template, request, redirect


app = Flask(__name__) 

#Lista global para armazenar os dicionários dos cadastros
lista_de_cadastros = []
    
@app.route('/')
def home():
    #return "<h1>Servidos Flask rodando!</h1>" "<h1>Bem vindo ao meu servidor flask</h1>"
    busca = request.args.get("busca", "").strip().lower()

    #2. filtro a lista se houver busca digitada
    if busca:
        registro_filtrados = [item for item in lista_de_cadastros if busca in item("nome").lower()]
    else:
        registro_filtrados = lista_de_cadastros

    total_registro = len(lista_de_cadastros)
    total_faturamento = sum (item("valor") for item in lista_de_cadastros)
    total_concluidos = sum(1 for item in lista_de_cadastros if item("status") == "Concluido")

#4 enviar os indicadores para a pagina index.html
    return render_template(
        "index.html",
        cadastro = registro_filtrados,
        total = total_registro,
        faturamento = total_faturamento,
        concluidos = total_concluidos,
        busca = busca
    )
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
    nome = request.form.get("campo_nome", "").strip()
    info = request.form.get("campo_info", "").strip()
    valor_str = request.form.get("Campo_Valor", "0").strip()
    try:
        valor = float(valor_str)
        if valor <=0:
            raise ValueError()
    except ValueError:
        return"<h3>Erro 400: O valor deve ser um valor maior que zero</h3><br>< a href='/ cadastro '>Voltar ao formulário</a>", 400

    if not nome or not info:
        return "<h3>Erro 400: Preencha todos os campos obrigatorio do formulario</h3><br><a href='/cadastro'>Voltar ao Formulario</a>", 400


    novo_registro = {
        "nome": nome,
        "info": info,
        "valor": valor,
        "status": "Pendente"
    }

    lista_de_cadastros.append(novo_registro)

    return redirect("/")


@app.route("/mudar-status/<int:indice>")
def mudar_status(indice):
    if 0 <= indice < len(lista_de_cadastros):
        if lista_de_cadastros[indice]["status"] == "Pendente":
            lista_de_cadastros[indice]["status"] == "Concluido"
        else:
            lista_de_cadastros[indice]["status"] == "Pendente"

    return redirect("/")

@app.route("/excluir/<int:indice>")
def excluir_cadastro(indice):
    if 0<= indice < len(lista_de_cadastros):
        lista_de_cadastros.pop(indice)
    return redirect("/")    


if __name__ == '__main__':
    app.run(debug=True)
