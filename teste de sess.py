from flask import Flask, render_template, redirect, request, session,Response,flash
from flask_session import Session
import reconhecimento as rec
import banco as bd
import cv2
import os
from fpdf import FPDF
import csv
import io
import xlwt
import disparandoEmail as disp


global listas,pessoas
listasDeModelos=list()
listasDePessoas=list()

global switch
switch = 1

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
UPLOAD_FOLDER=os.path.join(os.getcwd(),"fotos")
Session(app)

cameras = cv2.VideoCapture(0)
model_path = '12345.h5'
model = rec.load_model(model_path)

modelos=list()


def pegandoModelo():
    dados=bd.buscaEmpresa()
    for dado in dados:
        try:
            nome=str(dado[4]) + ".h5"
            caminho = os.path.join(os.getcwd(), "inteligen")
            caminhoFinal = os.path.join(caminho,nome)
            modelos.append(rec.load_model(caminhoFinal))
        except:
            pass
    return


def aplicandoReconhecimento(frame,cnpj,classe):
    tensor,x1, y1, w, h = rec.compara(frame)
    print("retorno efetuado")
    classe = model.predict_classes(tensor)[0]
    prob = model.predict_proba(tensor)
    prob = prob[0][classe] * 100
    if prob >= 98:
        y2 = y1 + h
        x2 = x1 + w
        if classe == 0:
            color = (224, 43, 100)
        else:
            color = (192, 255, 119)  # bgr
            user = str(pessoas[classe]).upper()
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        fonte_scale = 0.5

        if user != "desconhecido":
            bd.reconhecimentoPessoa(user,cnpj)
        frame=cv2.putText(frame, user, (x1, y1 - 10), font, fonte_scale, color, thickness=1)

    return frame



def generate_frames():
    while True:

        ## read the camera frame
        success, frame = cameras.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame=aplicandoReconhecimento(frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames_cadastro(cpf):
    saida = 100
    contadorr = 0
    while saida>0:
        contador=contadorr
        ## read the camera frame
        success, frame = cameras.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            nome = str(cpf) + str(contador) + ".jpeg"
            savePath = os.path.join(UPLOAD_FOLDER, nome)
            frame.save(savePath)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        saida=saida-1
        contadorr=contadorr+1
        rec.fotos(request.form.get("cpf"), len(100))
    return Criente()


@app.route('/camera')
def camera():
    return render_template('cadastroFotos.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/videoCadastro')
def videoCadastro():
    return Response(generate_frames_cadastro(), mimetype='multipart/x-mixed-replace; boundary=frame')

def compara(frame,pessoas,model):
    faces = rec.detector.detect_faces(frame)
    for face in faces:

        confidence = face['confidence'] * 100
        if confidence >= 98:
            x1, y1, w, h = face['box']
            y2 = y1 + h
            x2 = x1 + w
            face = rec.extrair_face(frame)
            face = face.astype("float32") / 255
            emb = rec.get_embedding(face)
            tensor = rec.np.expand_dims(emb, axis=0)
            norm = rec.Normalizer(norm="l2")
            tensor = norm.transform(tensor)
            return tensor

            classe = model.predict_classes(tensor)[0]
            prob = model.predict_proba(tensor)
            prob = prob[0][classe] * 100

            if prob >= 98:
                if classe == 0:
                    color = (224, 43, 100)
                else:
                    color = (192, 255, 119)  # bgr
                    user = str(pessoas[classe]).upper()
    return x1,y1,x2,y2,color,user

def carregamento(cnpj):
    nome = ["desconhecido"]
    pessoas = bd.buscaNomeF(cnpj)
    nome.extend(pessoas)
    print(nome)
    for pessoa in pessoas:
        print(pessoa)
    return pessoas

def carrega():
    lista = bd.cnpjFF()
    print(lista)
    for item in lista:
        cnpj = str(item) + ".h5"
        caminhoFinal = os.path.join(os.getcwd(), "inteligen")
        caminhoFinal=caminhoFinal+"\\"+cnpj
        try:
            model = rec.load_model(caminhoFinal)
            listas.append(model)
            bd.insertLocal(item,len(listas)-1)
        except:
            print("modelo não encontrado")
    return




@app.route("/")
def index():
        return render_template("index.html")

@app.route("/envioEmail",methods=["POST","GET"])
def envioEmail():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        assunto = request.form.get("assunto")
        mensagem = request.form.get("message")
        if nome != "None" and email != "None" and mensagem != 'None':
            saida = disp.envioEmail(nome, email, assunto, mensagem)
            if saida == True:
                flash("mensagem enviada")
            else:
                flash("erro ao enviar a mensagem ")
        else:
            flash("erro ao enviar a mensagem ")
        return redirect('/')

@app.route("/Criente", methods=["POST", "GET"])
def Criente():
    if not session.get("name"):
        return redirect("/login")
    else:
        cnpj=session.get("name")
        saida = bd.buscaDdadosEmpresa(cnpj)
        nome=saida[0]
        responsavel=saida[1]
        return render_template('tela_inicial.html',nome=nome,responsavel=responsavel)

@app.route("/login", methods=["POST", "GET"])
def login():
        if request.method == "POST":
            verificador = bd.login(request.form.get("name"),request.form.get("senha"))
            if(verificador==True):
                session["name"] = request.form.get("name")
                return redirect("/Criente")
            else:
                flash("o cnpj ou a senha esta errada ")
                return redirect('/login')
                
        return render_template("loginEmpresa.html")

@app.route("/criaConta", methods=["POST", "GET"])
def Criacao():
    if request.method == "POST":
        cnpj = request.form.get("cnpj")
        verificador = bd.buscaCnpj(cnpj)
        if verificador == False:
            senha = request.form.get("senha")
            senhaConfir=request.form.get("senhaConfir")
            nome = request.form.get("nome")
            responsavel = request.form.get("responsavel")
            email = request.form.get("email")
            if senha == senhaConfir:
                bd.mandaEmpresa(nome,responsavel,email,cnpj,senha)
                return redirect("/login")
            else:
                flash('confirmação de senha errada')
                return redirect('/criaConta')
        else:
            flash('empresa ja cadastrada')
            return redirect('/criaConta')
    return render_template("cadastroEmpresa.html")

@app.route("/EditaEmpresa",methods=["POST", "GET"])
def EditaEmpresa():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            conf = request.form.get("confirmacao")
            if conf == "on":
                senha = request.form.get("senha")
                confSenha = request.form.get("confSenha")
                if senha == confSenha:
                    cnpj = session.get("name")
                    nome = request.form.get("nome")
                    email = request.form.get("email")
                    responsavel = request.form.get("responsavel")
                    if bd.updatEm(nome, responsavel, email, cnpj, senha)==True:
                        flash("mudança realizada ")
                        return redirect("/Criente")
                    else:
                        flash("erro na mudança")
                        return redirect("/Criente")
                else:
                    flash("senhas diferentes")
                    return redirect("/Criente")
            else:
                flash("confirmação não marcada")
                return redirect("/Criente")
        else:
            cnpj=session.get("name")
            dados=bd.buscaDdadosEmpresa(cnpj)
            return render_template("ModificaEmpresa.html",dados=dados)

@app.route("/funci", methods=["POST", "GET"])
def funcionario():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method=="POST":
            cnpj = session.get("name")
            NOME = request.form.get("name")
            EMAIL = request.form.get("email")
            CPF = request.form.get("cpf")
            bd.mandaFunci(NOME,EMAIL,CPF,cnpj)
            bd.updatMudanca(cnpj)
            fires = request.files.getlist("fotos")
            if len(fires)>0:
                contadorr=len(fires)
                for fire in fires:
                    contador=contadorr
                    nome = request.form.get("cpf")+str(contador)+".jpeg"
                    savePath=os.path.join(UPLOAD_FOLDER,nome)
                    fire.save(savePath)
                    print("envio feito")
                    contadorr=contadorr-1
                rec.fotos(request.form.get("cpf"),len(fires))
                return redirect("/Criente")
            else:
                return fotosCadastroFuncionario(CPF)
        else:
            return render_template("cadastroFuncionario.html")

@app.route("/fotos",methods=["POST" , "GET"])
def fotos():
    return render_template("cadastroFotos.html")

@app.route("/fotosCadastroFuncionario/<cpf>",methods=["POST" , "GET"])
def fotosCadastroFuncionario(cpf):
    return render_template("cadastroFuncionarioFotos.html",cpf=cpf)

@app.route("/listagemF",methods=["POST" , "GET"])
def listagemF():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            cnpj = session.get("name")
            busca=request.form.get("busca")
            if busca=='':
                dados=bd.buscaFun(cnpj)
            else:
                dados=bd.buscaFunNome(cnpj,busca)
            if dados == 'erro':
                dados=False
            return render_template("listagemF.html", funcionarios=dados)
        else:
            cnpj=session.get("name")
            funcionarios=bd.buscaFun(cnpj)
            return render_template("listagemF.html" , funcionarios=funcionarios)

@app.route("/informaPonto",methods=["POST" , "GET"])
def informaP():
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "POST":
            cnpj = session.get("name")
            busca=request.form.get("busca")
            if busca=='':
                dados=bd.buscaTodosPonto(cnpj)
            else:
                dados=bd.buscaPontoFuncionarioNome(busca,cnpj)
            if dados == 'erro':
                dados=False
            return render_template("informaP.html", pontos=dados)
        else:
            cnpj=session.get("name")
            pontos=bd.buscaTodosPonto(cnpj)
            return render_template("informaP.html", pontos=pontos)

@app.route("/modificaF/<cpf>",methods=["POST" , "GET"])
def modificaF(cpf):
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "GET":
            cnpj = session.get("name")
            dados=bd.buscaFunE(cnpj,cpf)
            return render_template("modificaFuncionario.html", dados=dados)
        else:
            cnpj = session.get("name")
            nome=request.form.get("nome")
            email=request.form.get("email")
            cpf=request.form.get("cpf")
            conf=request.form.get("confirmacao")
            print(conf)
            if conf=='on':
                if bd.updatFun(nome,email,cpf,cnpj)==True:
                    flash("mudança efetuada")
                else:
                    flash("erro na mudança")
            else:
                flash("confirmação não marcada")
        return redirect('/listagemF')

@app.route("/deletaP/<id>", methods=["POST","GET"])
def deletaP(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method=="GET":
            dados=bd.buscaPontoFuncionarioID(id)
            print(dados)
            return render_template("ApagaPonto.html",dados=dados)
        else:
            id=request.form.get("id")
            cpf = request.form.get("cpf")
            conf = request.form.get("confirmacao")
            if conf == 'on':
                if bd.deletaPonto(cpf,id)==True:
                    flash("ponto deletado ")
                    return redirect('/informaPonto')
                else:
                    flash(" erro ao deletar o ponto ")
                    return redirect('/informaPonto')
            else:
                flash(" confirmação não marcado")
                return redirect('/informaPonto')

@app.route("/apagarFunc/<cpf>",methods=["POST" , "GET"])
def apagaF(cpf):
    if not session.get("name"):
        return redirect("/login")
    else:
        if request.method == "GET":
            cnpj = session.get("name")
            dados = bd.buscaFunE(cnpj,cpf)
            print(dados)
            return render_template("DeletaFuncionario.html",dados=dados)
        else:
            conf = request.form.get("confirmacao")
            print(conf)
            if conf == 'on':
                cnpj = session.get("name")
                cpf = request.form.get("cpf")
                print(cnpj)
                print(cpf)
                if bd.deletarFun(cpf, cnpj)==True:
                    flash('funcionario deletado')
                    return redirect('/listagemF')
                else:
                    flash('erro ao deletar funcionario')
                    return redirect('/listagemF')
            else:
                flash('erro ao deletar funcionario')
                return redirect('/listagemF')

@app.route("/caregamento")
def caregamento():
    return render_template("caregamento.html")

@app.route("/treinamento",methods=["POST" , "GET"])
def treinamento():
    if not session.get("name"):
        return redirect("/login")
    else:
        cnpj = session.get("name")
        if request.method == "Post":
            rec.uniDados(cnpj)
        if bd.comparacao(cnpj) == True:
            return render_template("treinamento.html",recente = bd.buscaCriacao(cnpj),pendentes = bd.buscaMudanca(cnpj),mostra = True)
        else:
            return render_template("treinamento.html",recente = bd.buscaCriacao(cnpj),pendentes = bd.buscaMudanca(cnpj),mostra = False)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")





@app.route('/download/report/pdf')
def download_report():
    cnpj = session.get("name")
    result = bd.buscaFun(cnpj)
    pdf = FPDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0, 'Listagem de Funcionarios', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)

    col_width = page_width / 4

    pdf.ln(1)

    th = pdf.font_size

    pdf.cell(col_width, th, "nome", border=1)
    pdf.cell(col_width, th, "email", border=1)
    pdf.cell(col_width, th, "cpf", border=1)
    pdf.cell(col_width, th, "cnpj", border=1)
    pdf.ln(th)

    for row in result:
        pdf.cell(col_width, th, row[0], border=1)
        pdf.cell(col_width, th, row[2], border=1)
        pdf.cell(col_width, th, row[3], border=1)
        pdf.cell(col_width, th, row[1], border=1)
        pdf.ln(th)

    pdf.ln(10)

    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- fim da listagem -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})

@app.route('/download/report/csv')
def download_report_csv():
        cnpj = session.get("name")
        result = bd.buscaFun(cnpj)
        output = io.StringIO()
        writer = csv.writer(output)

        line = ['nome,email,cpf,cnpj']
        writer.writerow(line)

        for row in result:
            line = [row[0] + ',' + row[2] + ',' + row[3] + ',' + row[1]]
            writer.writerow(line)

        output.seek(0)

        return Response(output, mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=employee_report.csv"})

@app.route('/download/report/excel')
def download_report_excel():
    cnpj = session.get("name")
    result = bd.buscaFun(cnpj)

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('Employee Report')

    sh.write(0, 0, 'nome')
    sh.write(0, 1, 'email')
    sh.write(0, 2, 'cpf')
    sh.write(0, 3, 'cnpj')

    idx = 0
    for row in result:
        sh.write(idx + 1, 0, row[0])
        sh.write(idx + 1, 1, row[2])
        sh.write(idx + 1, 2, row[3])
        sh.write(idx + 1, 3, row[1])
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=employee_report.xls"})

@app.route('/download/report/ponto/pdf')
def download_report_ponto():
    cnpj = session.get("name")
    result = bd.buscaTodosPonto(cnpj)
    pdf = FPDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0, 'Listagem de Pontos', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)

    col_width = page_width / 11

    pdf.ln(1)

    th = pdf.font_size

    pdf.cell(col_width, th, "nome", border=0)
    pdf.cell(col_width, th, "cpf", border=0)
    pdf.cell(col_width, th, "id", border=0)
    pdf.cell(col_width, th, "entrada", border=0)
    pdf.cell(col_width, th, "", border=0)
    pdf.cell(col_width, th, "", border=0)
    pdf.cell(col_width, th, "saida", border=0)
    pdf.cell(col_width, th, "", border=0)
    pdf.cell(col_width, th, "", border=0)
    pdf.cell(col_width, th, "permanencia", border=0)
    pdf.cell(col_width, th, "", border=0)
    pdf.ln(th)

    for row in result:
        pdf.cell(col_width, th, row[0], border=0)
        pdf.cell(col_width, th, row[1], border=0)
        pdf.cell(col_width, th, str(row[2]), border=0)
        pdf.cell(col_width, th, str(row[5]), border=0)
        pdf.cell(col_width, th, "", border=0)
        pdf.cell(col_width, th, "", border=0)
        pdf.cell(col_width, th, str(row[6]), border=0)
        pdf.cell(col_width, th, "", border=0)
        pdf.cell(col_width, th, "", border=0)
        pdf.cell(col_width, th, str(row[3]), border=0)
        pdf.cell(col_width, th, "", border=0)
        pdf.ln(th)

    pdf.ln(10)

    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- fim da listagem -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})

@app.route('/download/report/ponto/csv')
def download_report_ponto_csv():
        cnpj = session.get("name")
        result = bd.buscaTodosPonto(cnpj)
        output = io.StringIO()
        writer = csv.writer(output)

        line = ['nome,cpf,id,entrada,saida,permanencia']
        writer.writerow(line)

        for row in result:
            line = [row[0] + ',' + row[1] + ',' + str(row[2]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[3])]
            writer.writerow(line)

        output.seek(0)

        return Response(output, mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=employee_report.csv"})

@app.route('/download/report/ponto/excel')
def download_report_ponto_excel():
    cnpj = session.get("name")
    result = bd.buscaTodosPonto(cnpj)

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('Employee Report')

    sh.write(0, 0, 'nome')
    sh.write(0, 1, 'cpf')
    sh.write(0, 2, 'id')
    sh.write(0, 3, 'entrada')
    sh.write(0, 4, 'saida')
    sh.write(0, 5, 'permanencia')
    sh.write(0, 6, 'cnpj')

    idx = 0
    for row in result:
        sh.write(idx + 1, 0, row[0])
        sh.write(idx + 1, 1, row[1])
        sh.write(idx + 1, 2, str(row[2]))
        sh.write(idx + 1, 3, str(row[5]))
        sh.write(idx + 1, 4, str(row[6]))
        sh.write(idx + 1, 5, str(row[3]))
        sh.write(idx + 1, 6, row[4])
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=employee_report.xls"})

if __name__ == "__main__":
    app.run(debug=True)
    camera.release()
    cv2.destroyAllWindows()