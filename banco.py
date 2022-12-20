import mysql.connector
from mysql.connector import Error
import datetime

try:
    con = mysql.connector.connect(host='localhost', database='refape', user='root', password='italo175933')
    cursor = con.cursor()
    conexao=True
except:
    conexao = False

def fechaConexao():
    if (con.is_connected()):
        con.close()
        cursor.close()


#login
def login(cnpj,senha):
    comando = "select*from refape.empresa where CNPJ = \'{}\' and senha = \'{}\'".format(cnpj, senha)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = True
    except Error as e:
        saida = False
    return saida
#-------------------------


#listagen funcionarios
def buscaFun(CNPJ):
    comando = "select*from refape.funcionario where cnpj = \'{}\' ".format(CNPJ)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida = False
        else:
            saida = linhas
    except Error as e:
        saida = False
    return saida

def buscaFunNome(CNPJ,nome):
    comando = "select*from refape.funcionario where cnpj = \'{}\' and nome=\'{}\'".format(CNPJ,nome)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida=False
        else:
            saida = linhas
    except Error as e:
        saida = False
    return saida
#-------------------------


#listagen pontos
def buscaTodosPonto(cnpj):
    comando = "SELECT*FROM refape.ponto WHERE cnpj= \'{}\' ".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida=False
        else:
            saida = linhas
    except Error as e:
        saida = False
    return saida

def buscaPontoFuncionarioNome(nome,cnpj):
    comando="SELECT*FROM refape.ponto WHERE nome=\'{}\' and cnpj=\'{}\'".format(nome,cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida= False
        else:
            saida = linhas
    except Error as e:
        saida = False
    return saida
#-------------------------


#entrada de pontos
def reconhecimentoPessoa(nome,cnpj):
    pontos=list()
    comando = "SELECT*FROM refape.ponto WHERE nome=\'{}\' and cnpj=\'{}\'".format(nome, cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if linhas == False:
            return False
        for linha in linhas:
            pontos.append(linha[2])
        saidas = reconhecimentoPessoaId(max(pontos))
        if saidas != False:
            for saida in saidas:
                    cpf = saida[1]
                    comparador = saida[6]
                    if not comparador:
                        Entrada=saida[5]
                        tempoExtra = datetime.timedelta(minutes=5)
                        Entrada=Entrada+tempoExtra
                        if Entrada <= datetime.datetime.now():
                            if updatSaida(max(pontos)) == True:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        if updatEntrada(nome,cpf,cnpj) == True:
                            return True
                        else:
                            return False
        else:
            return False
    except Error as e:
        return False

def updatSaida(id):
    comando = " UPDATE refape.ponto set Saida = NOW() where  id=\'{}\'".format(id)
    try:
        cursor.execute(comando)
        con.commit()
        if calculandoPermanencia(id)==True:
            saida = True
        else:
            saida = False
    except Error as e:
        saida = False
    return saida

def updatEntrada(nome,cpf,cnpj):
    comando = """ INSERT INTO refape.ponto(nome,cpf,cnpj,Entrada)
               VALUE (\'{}\',\'{}\',\'{}\',NOW())""".format(nome, cpf, cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def reconhecimentoPessoaId(id):
    comando = "SELECT*FROM refape.ponto WHERE id=\'{}\'".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            return False
        else:
            return linhas
    except Error as e:
        return False

def calculandoPermanencia(id):
    comando = "SELECT*FROM refape.ponto WHERE id=\'{}\'".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida=True
        else:
            for linha in linhas:
                entrada=linha[5]
                saida=linha[6]
                tt = saida - entrada
                return updatPermanencia(id,tt)
    except Error as e:
        saida = False
    return saida

def updatPermanencia(id,tempo):
    comando = " UPDATE refape.ponto set permanencia = \'{}\' where id=\"{}\" ".format(tempo,id)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida
#-------------------------


#envio de empresa
def mandaEmpresa(nome,responsavel,e_mail,cnpj,senha):
    comando = " INSERT INTO refape.empresa(nome,responsavel,e_mail,cnpj,senha) VALUE (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\' )".format(nome,responsavel,e_mail,cnpj,senha)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida
#-------------------------


#envio de funcionario
def mandaFunci(nome,email,cpf,cnpj):
    comando=""" INSERT INTO refape.funcionario(nome,email,cpf,cnpj)
            VALUE (\'{}\',\'{}\',\'{}\',\'{}\')""".format(nome,email,cpf,cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida=True
    except Error as e:
        saida=False
    return saida
#-------------------------


#modifica Empresa
def updatEm(nome, responsavel, email, cnpj, senha):
        comando = " UPDATE refape.empresa set nome=\"{}\", responsavel=\"{}\" ,e_mail=\"{}\",senha=\"{}\" where cnpj=\"{}\" ".format(
            nome, responsavel, email, senha, cnpj)
        try:

            cursor.execute(comando)
            con.commit()
            saida = True

        except Error as e:
            saida = False
        return saida
#-------------------------


#modifica Funcionario
def updatFun(nome, email, cpf, cnpj):
        comando = " UPDATE refape.funcionario set nome = \"{}\", email = \"{}\"  where cpf = \"{}\" and cnpj=\'{}\'".format(
            nome, email, cpf, cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            print(comando)
            saida = True
        except Error as e:
            saida = False
        return saida
#-------------------------


#deletando Funcionario
def deletarFun(cpf, cnpj):
        comando = "DELETE FROM refape.funcionario where cpf=\'{}\' and cnpj=\'{}\'".format(cpf, cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            saida = True
        except Error as e:
            saida = False
        return saida

def buscaFunE(CNPJ, CPF):
        comando = "select*from refape.funcionario where cnpj = \'{}\' and cpf=\'{}\'".format(CNPJ, CPF)
        try:
            cursor.execute(comando)
            linhas = cursor.fetchall()
            if len(linhas) == 0:
                saida = False
            else:
                saida = linhas
        except Error as e:
            saida = False
        return saida

def deletandoTodosFuncionarios(cnpj):
        comando = "DELETE FROM refape.funcionario where cnpj=\'{}\'".format(cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            saida = True
        except Error as e:
            saida = False
        return saida
#-------------------------


#deletando Empresa
def deletarEm(cnpj):
    comando="DELETE FROM refape.empresa where cnpj=\'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
        deletaTodosPontos(cnpj)
    except Error as e:
        saida = False
    return saida

def buscaPontoFuncionarioID(id):
    comando = "SELECT*FROM refape.ponto WHERE id=\'{}\'".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = linhas
    except Error as e:
        saida = False
    return saida
#-------------------------


#deletando ponto
def deletaPonto(cpf, id):
    comando = "DELETE FROM refape.ponto where cpf= \'{}\' and id = {}".format(cpf, id)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def deletaTodosPontos(cnpj):
    comando = "DELETE FROM refape.ponto where cnpj=\'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = "funcionario deletado"
    except Error as e:
        saida = "erro ao deletar o ponto"
    return saida
#-------------------------

#dados de treinamento
def updatMudanca(cnpj):
    comando = " UPDATE refape.empresa set mudanca = NOW() where cnpj=\"{}\" ".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def updatCriacao(cnpj):
    comando = " UPDATE refape.empresa set criacao = NOW() where cnpj=\"{}\" ".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida

def comparacao(cnpj):
    criacao=buscaCriacao(cnpj)
    mudanca=buscaMudanca(cnpj)
    if criacao == False or mudanca == False:
        return False
    else:
        if criacao == mudanca:
            return True
        else:
            return False

def buscaMudanca(cnpj):
    comando = "select mudanca from refape.empresa where cnpj={}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            for linha in linhas:
                saida=linha[0]
    except Error as e:
        saida = False
    return saida

def buscaCriacao(cnpj):
    comando = "select criacao from refape.empresa where cnpj={}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            for linha in linhas:
                saida=linha[0]
    except Error as e:
        saida = False
    return saida
#-------------------------

#busca de modelos
def buscaEmpresa():
    comando = "select*from refape.empresa order by nome"
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida=linhas
    except Error as e:
        saida = False
    return saida
#-------------------------

#carregamento
def buscaNomeF(CNPJ):
    comando = "select nome from refape.funcionario where cnpj = \'{}\' order by nome".format(CNPJ)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida="não existe funcionario"
        else:
            saida = linhas
    except Error as e:
        saida = "erro na busca"
    return saida
#-------------------------


#pagina do cliente
def buscaDdadosEmpresa(cnpj):
    comando = "select*from refape.empresa where CNPJ = \'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            for linha in linhas:
                saida=linha
    except Error as e:
        saida = False
    return saida
#-------------------------


#unindo dados
def buscaInf(cnpj):
    saida=list()
    comando = "select*from refape.funcionario where cnpj= {} order by nome".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            for linha in linhas:
                saida.append(linha[3])
    except Error as e:
        saida = False
    return saida
#-------------------------


#modifica registro de face
def updatFaceF(cnpj,saida):
    comando = " UPDATE refape.funcionario set face = {} where cnpj=\"{}\" ".format(saida,cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida
#-------------------------