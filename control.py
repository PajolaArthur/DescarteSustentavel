from main import app, os
from model import *
from flask import Flask, render_template, request, url_for, flash, redirect, send_file
from werkzeug.exceptions import abort
from geopy.geocoders import Nominatim
from fpdf import FPDF
import folium

usuariologado=0
atualdataehora = datetime.now()
horadata = atualdataehora.strftime('%d/%m/%Y %H:%M:%S')


@app.route('/')
def index():
    global usuariologado
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "}        

    coletas = Coletas.query.all()
    mapObj = folium.Map(zoom_start=14, location=[-20.719641,-47.887951], width=800, height=400, position="center")

    for coleta in coletas:

        dados=(coleta.id,coleta.descricao,coleta.endereco,coleta.telefone,coleta.diacoleta)

        inEnde= dados[2]
        cep="14620-000"
        cidade="Orlândia"
    
        Endereco = inEnde+"  "+cidade+" "+cep
        geolocalizador = Nominatim(user_agent="geopy")
        Localizacao = geolocalizador.geocode(Endereco)
        if not Localizacao == None:
            geolocal = Localizacao.latitude, Localizacao.longitude
            marcador=coleta.id
            marcador=folium.Marker(location=geolocal,
            tooltip=dados[1],
            popup=folium.Popup("\n Descrição: "+dados[1]+"\n Endereço: "+dados[2]+"\n Telefone: "+dados[3]+"\n Dia: "+dados[4],max_width=1000)).add_to(mapObj)
        
       
    mapObj.save('templates/mapa.html')
    return render_template('index.html', coletas=coletas, dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/mapacoleta')
def mapacoleta():
    return render_template('mapacoleta.html')


def get_coleta(coleta_id):
    coleta = Coletas.query.filter_by(id=coleta_id).first()
    if coleta is None:
        abort(404)
    return coleta

@app.route('/<int:coleta_id>')
def coleta(coleta_id):
    global usuariologado
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 

    if usuariologado==0:
        flash("Usuário não identificado, realize Login para Gerenciar!")
        return redirect(url_for('index'))
    else:
        coleta = get_coleta(coleta_id)
        whatsapp=coleta.telefone
        telddd = whatsapp[1:3]
        telinicio = whatsapp[5:10]
        telfinal = whatsapp[11:15]

        whatsapp=telddd+telinicio+telfinal
        dadoswhats = {"whats":whatsapp}
   
        geolocalizador = Nominatim(user_agent="geopy")
        local= coleta.endereco
        localendereco = (local+" Orlândia 14620-000")
        geolocal = geolocalizador.geocode(localendereco)
        if  geolocal == None:
            geocord = localendereco
            dadoslocal = {"geoendereco":localendereco, "geocord":geocord}
            mapcoleta = folium.Map(zoom_start=20, location=[-20.719641,-47.887951], width=800, height=400, position="center")
            mapcoleta.save('templates/mapacoleta.html')

            return render_template('coleta.html', coleta=coleta, dadoslocal=dadoslocal, dadoswhats=dadoswhats, dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)

        else:
            geocord = geolocal.latitude, geolocal.longitude
            dadoslocal = {"geoendereco":localendereco, "geocord":geocord}
            mapcoleta = folium.Map(zoom_start=14, location=[-20.719641,-47.887951], width=800, height=400, position="center")
            dados=(coleta.id,coleta.descricao,coleta.endereco,coleta.telefone,coleta.diacoleta)
    
            inEnde= dados[2]
            cep="14620-000"
            cidade="Orlândia"
    
            Endereco = inEnde+"  "+cidade+" "+cep
            geolocalizador = Nominatim(user_agent="geopy")
            Localizacao = geolocalizador.geocode(Endereco)

            geolocal = Localizacao.latitude, Localizacao.longitude

            folium.Marker(location=geocord,
            tooltip=dados[1],
            popup=folium.Popup("\n Descrição: "+dados[1]+"\n Endereço: "+dados[2]+"\n Telefone: "+dados[3]+"\n Dia: "+dados[4],max_width=1000)).add_to(mapcoleta)
            mapcoleta.save('templates/mapacoleta.html')
            return render_template('coleta.html', coleta=coleta, dadoslocal=dadoslocal, dadoswhats=dadoswhats, dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)
   
@app.route('/<int:id>/baixar', methods=('GET', 'POST'))
def baixar(id):
    coleta = get_coleta(id)
    idcoleta = str(coleta.id)

    caminhodoarquivo='static/PDFs/'
    nomearquivo=idcoleta+"_"+coleta.descricao+"_"+coleta.endereco

    # Instantiation of inherited class
    pdf = FPDF()
    pdf.add_page()
    # HEADER
    # Logo
    pdf.image('static/img/reciclando.png', 65, 10, 80)
    # Arial bold 15
    pdf.set_font('Arial', 'B', 30)
    # Move to the right
    pdf.cell(80)
    # Title
    pdf.ln(80)
    pdf.cell(190, 20, 'Descarte Sustentável', 1, 0, 'C')
    # Line break
    pdf.ln(40)
    pdf.alias_nb_pages()
    pdf.set_font('Times', '', 15)
    pdf.cell(0, 4, 'ID: '+idcoleta, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Descrição: '+coleta.descricao, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Quantidade: '+coleta.quantidade, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Endereco: '+coleta.endereco, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Telefone: '+coleta.telefone, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Dia de coleta: '+coleta.diacoleta, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Hora de coleta: '+coleta.horacoleta, 0, 1)
    pdf.ln(5)
    pdf.cell(0, 4, 'Situação: '+coleta.situacao, 0, 1)
    pdf.ln(74)
    pdf.cell(105)
    pdf.cell(0, 4, 'Relatório gerado em: '+horadata, 0, 1)

    pdf.output(caminhodoarquivo+nomearquivo+'.pdf', 'F')

    caminho = caminhodoarquivo+nomearquivo+'.pdf'
    return send_file(caminho, as_attachment=True)

@app.route('/gerenciar')
def gerenciar():
    global usuariologado
    coletas = Coletas.query.all()
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 

    if usuariologado==0:
        flash("Usuário não identificado, realize Login para Gerenciar!")
        return redirect(url_for('index'))
    else:
            coletas = Coletas.query.all()
            mapObj = folium.Map(zoom_start=14, location=[-20.719641,-47.887951], width=800, height=400, position="center")

            for coleta in coletas:

                dados=(coleta.id,coleta.descricao,coleta.endereco,coleta.telefone,coleta.diacoleta,coleta.situacao)

                inEnde= dados[2]
                cep="14620-000"
                cidade="Orlândia"
    
                Endereco = inEnde+"  "+cidade+" "+cep
                geolocalizador = Nominatim(user_agent="geopy")
                Localizacao = geolocalizador.geocode(Endereco)
                if not Localizacao == None:
                    geolocal = Localizacao.latitude, Localizacao.longitude
                    marcador=coleta.id
                    marcador=folium.Marker(location=geolocal,
                    tooltip=dados[1],
                    popup=folium.Popup("|Situação: "+dados[5]+" |Descrição: "+dados[1]+" |Endereço: "+dados[2]+" |Telefone: "+dados[3]+" |Dia: "+dados[4],max_width=1000)).add_to(mapObj)
        
       
            mapObj.save('templates/mapa.html')
            return render_template('gerenciar.html', coletas=coletas, dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)


@app.route('/login', methods=('GET', 'POST'))
def login():
    global usuariologado
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 

    if usuariologado==0:
        usuarios = Usuarios.query.all()

        if request.method == 'POST':
            nome = request.form['nome']
            senha = request.form['senha']
            print("Entrada: ",nome, senha)
            print("Tempo: ", horadata)
            if not nome and senha:
                flash('Campos obrigatórios! Preencha os campos Nome e Senha!')
            elif not nome:
                flash('Campos obrigatórios! Preencha o campo Nome!')
            elif not senha:
                flash('Campos obrigatórios! Preencha o campo Senha!')
            else:
                for usuario in usuarios: 
                    if usuario.nome == nome and usuario.senha == senha:
                        usuariologado+=1
                        return redirect(url_for('gerenciar'))
                    else: 
                        return redirect(url_for('login'))
        return render_template('login.html', dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)
    else:
        return redirect(url_for('gerenciar'))



@app.route('/create', methods=('GET', 'POST'))
def create():
    global usuariologado
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 

    if request.method == 'POST':
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        diacoleta = request.form['diacoleta']
        horacoleta = request.form['horacoleta']
        situacao = "Em andamento"

        if not descricao:
            flash('Campos obrigatórios! Preencha o campo Descrição')
        elif not quantidade:
             flash('Campos obrigatórios! Preencha o campo Quantidade')
        elif not endereco:
             flash('Campos obrigatórios! Preencha o campo Endereço.')
        elif not telefone:
             flash('Campos obrigatórios! Preencha o campo Telefone')
        else:
            coleta = Coletas(descricao=descricao, quantidade=quantidade, endereco=endereco, telefone=telefone, diacoleta=diacoleta, horacoleta=horacoleta, situacao=situacao)
            db.session.add(coleta)
            db.session.commit()
            return redirect(url_for('index'))
        
    return render_template('create.html', dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    global usuariologado
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 

    if usuariologado ==0:
        return redirect(url_for('login'))

    coleta = get_coleta(id)

    if request.method == 'POST':
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        diacoleta = request.form['diacoleta']
        horacoleta = request.form['horacoleta']
        situacao = request.form['situacao']

        if not descricao:
            flash('Campos obrigatórios!')
        else:
            coleta.descricao = descricao
            coleta.quantidade = quantidade
            coleta.endereco = endereco
            coleta.telefone = telefone
            coleta.diacoleta = diacoleta
            coleta.horacoleta = horacoleta
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', coleta=coleta, dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    coleta = get_coleta(id)
    db.session.delete(coleta)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(coleta.descricao))
    return redirect(url_for('gerenciar'))

@app.route('/<int:id>/concluido', methods=('POST',))
def concluido(id):
    coleta = get_coleta(id)
    coleta.situacao = "Concluído"
    db.session.commit()
    flash('"{}" foi concluído com sucesso!'.format(coleta.descricao))
    return redirect(url_for('gerenciar'))

@app.route('/<int:id>/cancela', methods=('POST',))
def cancela(id):
    coleta = get_coleta(id)
    coleta.situacao = "Cancelado"
    db.session.commit()
    flash('"{}" foi Cancelado com sucesso!'.format(coleta.descricao))
    return redirect(url_for('gerenciar'))


@app.route('/sobrenos')
def sobrenos():
    if usuariologado != 0:
        dadoslogin = {"login":" "}
        dadosgerenciar = {"gerenciar":"Gerenciar"}
    else:
        dadoslogin = {"login":"Login"}
        dadosgerenciar = {"login":" "} 
    return render_template('sobrenos.html', dadoslogin=dadoslogin, dadosgerenciar=dadosgerenciar)
