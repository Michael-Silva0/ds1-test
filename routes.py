import os

from flask import Blueprint, flash, redirect, render_template, request

from database import db
from models import Categoria, Registro

main_bp = Blueprint("main", __name__)

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}


def arquivo_permitido(filename):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
    )


@main_bp.route("/")
def home():
    busca = request.args.get("busca", "").strip().lower()
    categoria_id = request.args.get("categoria_id", "")

    query = Registro.query
    if busca:
        query = query.filter(Registro.nome.ilike(f"%{busca}%"))
    if categoria_id and categoria_id.isdigit():
        query = query.filter(Registro.categoria_id == int(categoria_id))

    registros = query.all()
    total = len(registros)
    faturamento = sum(item.valor for item in registros)
    concluidos = sum(1 for item in registros if item.status == "Concluído")
    categorias = Categoria.query.all()

    return render_template(
        "index.html",
        cadastros=registros,
        total=total,
        faturamento=faturamento,
        concluidos=concluidos,
        busca=busca,
        categorias=categorias,
        categoria_selecionada=int(categoria_id) if categoria_id.isdigit() else None,
    )


@main_bp.route("/cadastro")
def pagina_cadastro():
    categorias = Categoria.query.all()
    return render_template("cadastro.html", categorias=categorias)


@main_bp.route("/salvar", methods=["POST"])
def salvar_cadastro():
    nome = request.form.get("campo_nome", "").strip()
    info = request.form.get("campo_info", "").strip()
    valor_str = request.form.get("campo_valor", "0").strip()
    cat_id = request.form.get("campo_categoria")

    arquivo_foto = request.files.get("campo_imagem")
    if not nome or not info or not valor_str or not cat_id:
        flash("Todos os campos são obrigatórios. Por favor, preencha todos os campos.")
        return redirect(
            "/cadastro"
        )  # Redireciona de volta para a página de cadastro se algum campo estiver vazio

    try:
        valor = float(valor_str)
        if valor < 0:
            raise ValueError("Valor não pode ser negativo.")
    except ValueError:
        flash("Valor inválido. Por favor, insira um número válido.")
        return redirect(
            "/cadastro"
        )  # Redireciona de volta para a página de cadastro se o valor for inválido
    nome_imagem_salva = "padrao.png"  # Nome da imagem padrão
    if arquivo_foto and arquivo_permitido(arquivo_foto.filename):
        nome_imagem_salva = arquivo_foto.filename
        caminho_imagem = f"static/uploads/{nome_imagem_salva}"
        arquivo_foto.save(caminho_imagem)
    else:
        flash("Arquivo de imagem inválido ou não fornecido. Usando imagem padrão.")
        return redirect(
            "/cadastro"
        )  # Redireciona de volta para a página de cadastro se o arquivo de imagem for inválido
    
    novo_registro = Registro(
        nome=nome, 
        info=info, 
        valor=valor, 
        categoria_id=int(cat_id), 
        imagem=nome_imagem_salva
    )
    db.session.add(novo_registro)
    db.session.commit()

    flash("Cadastro realizado com sucesso!")
    return redirect("/")  # Redireciona para a página inicial após o cadastro bem-sucedido

@main_bp.route("/deletar/<int:registro_id>")
def excluir_cadastro(id):
    registro = Registro.query.get(id)
    if registro:  # noqa: SIM102
        if registro.imagem and registro.imagem != "padrao.png":
            caminho_imagem = f"static/uploads/{registro.imagem}"
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
        db.session.delete(registro)
        db.session.commit()
        flash("Cadastro excluído com sucesso!", "info")

    return redirect("/")  # Redireciona para a página inicial após a exclusão do cadastro