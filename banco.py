import mysql.connector
from mysql.connector import Error

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


#comandos de pesquisa
def buscaFun(CNPJ):
    comando = "select*from refape.funcionario where cnpj = \'{}\' ".format(CNPJ)
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

def buscaFunE(CNPJ,CPF):
    comando = "select*from refape.funcionario where cnpj = \'{}\' and cpf=\'{}\'".format(CNPJ,CPF)
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

def buscaFunNome(CNPJ,nome):
    comando = "select*from refape.funcionario where cnpj = \'{}\' and nome=\'{}\'".format(CNPJ,nome)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida="erro"
        else:
            saida = linhas
    except Error as e:
        saida = "erro"
    return saida



def cnpjFF():
    comando = "select * from refape.empresa order by nome"
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "ERRO"
        else:
            saida=list()
            for linha in linhas:
                saida.append(linha[4])
    except Error as e:
        saida = "ERRO"
    return saida

def buscaEm(cnpj):
    comando = "select*from refape.empresa where CNPJ = \'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida = "ERRO"
        else:
            for linha in linhas:
                if linha[6] == linha[7]:
                    saida = True
                else:
                    saida = False
    except Error as e:
        saida = False
    return saida

def buscaDdadosEmpresa(cnpj):
    comando = "select*from refape.empresa where CNPJ = \'{}\'".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "ERRO"
        else:
            for linha in linhas:
                saida=linha
    except Error as e:
        saida = False
    return saida

def buscaMudanca(cnpj):
    comando = "select mudanca from refape.empresa where cnpj={}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "erro"
        else:
            for linha in linhas:
                saida=linha[0]
    except Error as e:
        saida = "erro"
    return saida

def buscaCriacao(cnpj):
    comando = "select criacao from refape.empresa where cnpj={}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "erro"
        else:
            for linha in linhas:
                saida = linha[0]
    except Error as e:
        saida = "erro"
    return saida

def buscaInf(cnpj):
    saida=list()
    comando = "select*from refape.funcionario where cnpj= {} order by nome".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "erro"
        else:
            for linha in linhas:
                saida.append(linha[3])
    except Error as e:
        saida = "erro na busca"
    return saida

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



def buscaLocal(cnpj):
    comando = "select locall from refape.empresa where cnpj= {} order by nome".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = "ERRO"
        else:
            saida = linhas
    except Error as e:
        saida = "ERRO"
    return saida

def buscaCnpj(cnpj):
    comando = "select*from refape.empresa where cnpj = {}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            saida = True
    except Error as e:
        saida = "ERRO"
    return saida

def verificador(id):
    comando="select*from refape.ponto where id = \'{}\'".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        for linha in linhas:
            if linha[5] == "None":
                saida=True
            else:
                saida=False
    except Error as e:
        saida = "erro na busca"
    return saida



def login(cnpj,senha):
    comando = "select*from refape.empresa where CNPJ = \'{}\' and senha = \'{}\'".format(cnpj, senha)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = False
        else:
            for linha in linhas:
                saida = True
    except Error as e:
        saida = False
    return saida
def comparacao(cnpj):
    criacao=buscaCriacao(cnpj)
    mudanca=buscaMudanca(cnpj)
    if criacao=="erro" or mudanca=="erro":
        return False
    else:
        if criacao == mudanca:
            return True
        else:
            return False



def mandaEmpresa(nome,responsavel,e_mail,cnpj,senha):
    comando = " INSERT INTO refape.empresa(nome,responsavel,e_mail,cnpj,senha) VALUE (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\' )".format(nome,responsavel,e_mail,cnpj,senha)
    try:
        cursor.execute(comando)
        con.commit()
        saida="deu bom no envio"
    except Error as e:
        saida="erro no envio"
    return saida

def mandaFunci(nome,email,cpf,cnpj):
    comando=""" INSERT INTO refape.funcionario(nome,email,cpf,cnpj)
            VALUE (\'{}\',\'{}\',\'{}\',\'{}\')""".format(nome,email,cpf,cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida="deu bom no cadstro de funcionario"
    except Error as e:
        saida="erro no cadastro de funcionario"
    return saida



def buscaTodosPonto(cnpj):
    comando = "SELECT*FROM refape.ponto WHERE cnpj= \'{}\' ".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        saida = linhas
    except Error as e:
        saida = "erro na busca"
    return saida

def buscaPontos(cnpj):
    saida=list()
    nomes=list()
    comando = "SELECT*FROM refape.ponto where cnpj={}".format(cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        for linha in linhas:
            if linha[6]==None:
                saida.append(linha)
    except Error as e:
        saida = "erro na busca"
    return saida

def buscaPontoFuncionario(cpf,cnpj):
    comando="SELECT*FROM refape.ponto WHERE cpf=\'{}\' and cnpj=\'{}\'".format(cpf,cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        return linhas
    except Error as e:
        return "erro"

def buscaPontoFuncionarioNome(nome,cnpj):
    comando="SELECT*FROM refape.ponto WHERE nome=\'{}\' and cnpj=\'{}\'".format(nome,cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas)==0:
            saida='erro'
        else:
            saida = linhas
    except Error as e:
        saida = "erro"
    return saida

def buscaPontoFuncionarioID(id):
    comando="SELECT*FROM refape.ponto WHERE id=\'{}\'".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        saida = linhas
    except Error as e:
        saida = "erro na busca"
    return saida

def reconhecimentoPessoa(nome,cnpj):
    pontos=list()
    comando = "SELECT*FROM refape.ponto WHERE nome=\'{}\' and cnpj=\'{}\'".format(nome, cnpj)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        for linha in linhas:
            pontos.append(linha[2])
        saidas = reconhecimentoPessoaId(max(pontos))
        for saida in saidas:
            if saida != False:
                cpf = saida[3]
                comparador=saida[6]
                if comparador == "None":
                    if updatSaida(max(pontos)) == True:
                        return True
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
        saida = True
    except Error as e:
        saida = False
    return saida

def updatEntrada(nome,cpf,cnpj):
    comando = """ INSERT INTO refape.ponto(nome,cpf,cnpj Entrada)
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




def deletarEm(cnpj,confirmacao):
    if confirmacao==True:
        comando="DELETE FROM refape.empresa where cnpj=\'{}\'".format(cnpj)
        comando2="DELETE FROM refape.funcionario where cnpj=\'{}\'".format(cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            cursor.execute(comando2)
            con.commit()
            saida = "empresa deletada"
        except Error as e:
            saida = "erro ao deletar a empresa"

    else:
        saida = "falha ao deletar uma empresa"
    return saida

def deletarFun(cpf,cnpj):
        comando = "DELETE FROM refape.funcionario where cpf=\'{}\' and cnpj=\'{}\'".format(cpf,cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            saida = True
        except Error as e:
            saida = False
        return saida

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



def updatEm(nome,responsavel,email,cnpj,senha):
        comando = " UPDATE refape.empresa set nome=\"{}\", responsavel=\"{}\" ,e_mail=\"{}\",senha=\"{}\" where cnpj=\"{}\" ".format(nome,responsavel,email,senha,cnpj)
        try:

            cursor.execute(comando)
            con.commit()
            saida = True

        except Error as e:
            saida = False
        return saida

def updatFaceF(cnpj):
    comando = " UPDATE refape.empresa set mudanca = CURRENT_TIMESTAMP() where cnpj=\"{}\" ".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = "mudança feita"
    except Error as e:
        saida = "erro ao fazer a mudança"
    return saida

def updatFun(nome,email,cpf,cnpj):
        comando = " UPDATE refape.funcionario set nome = \"{}\", email = \"{}\"  where cpf = \"{}\" and cnpj=\'{}\'".format(nome,email,cpf,cnpj)
        try:
            cursor.execute(comando)
            con.commit()
            print(comando)
            saida = True
        except Error as e:
            saida = False
        return  saida

def updatMudanca(cnpj):
    comando = " UPDATE refape.empresa set mudanca = NOW() where cnpj=\"{}\" ".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = "mudança feita"
    except Error as e:
        saida = "erro ao fazer a mudança"
    return saida

def updatCriacao(cnpj):
    comando = " UPDATE refape.empresa set criacao = NOW() where cnpj=\"{}\" ".format(cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = "mudança feita"
    except Error as e:
        saida = "erro ao fazer a mudança"
    return saida

def insertLocal(cnpj,local):
    comando = " UPDATE refape.empresa set locall=\"{}\" where cnpj=\"{}\" ".format(local,cnpj)
    try:
        cursor.execute(comando)
        con.commit()
        saida = "mudança feita"
    except Error as e:
        saida = "erro ao fazer a mudança"
    return saida
