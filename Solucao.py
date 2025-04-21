import oracledb, pandas as pd, os, json
from time import sleep

# try:
    # oracledb.init_oracle_client(lib_dir=r'C:\Users\Davi\Documents\instantclient-basic-windows.x64-23.7.0.25.01\instantclient_23_7')
    # conn = oracledb.connect(user="rm562274", password="090402", dsn='oracle.fiap.com.br:1521/ORCL')
# except:
#     print("Algo deu errado\nVerifique a conexão.")
# else:
#     print("Conexão estabelecida com sucesso")

oracledb.init_oracle_client(lib_dir=r'C:\Users\Davi\Documents\instantclient-basic-windows.x64-23.7.0.25.01\instantclient_23_7')
conn = oracledb.connect(user="sys", password="090402", dsn='localhost:1521/XEPDB1', mode=oracledb.SYSDBA)
cursor = conn.cursor()
# aaaaa

def cadastro(dataframe, condition):
    cursor.executemany(f'''INSERT INTO INSUMOS_AGRICOLAS (
                            ID,
                            INSUMO, 
                            CATEGORIA, 
                            FABRICANTE, 
                            VALIDADE, 
                            QTDE_EM_ESTOQUE, 
                            UNIDADE_DE_MEDIDA, 
                            AQUISICAO, 
                            VALOR_UNITARIO)
                        VALUES(SEQ_CLIENTE.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8)
                ''', list(dataframe.itertuples(index=False, name=None)))

    conn.commit()

def delete():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM INSUMOS_AGRICOLAS")
    conn.commit()

def update_insumo(row):
    cursor.execute('''
        UPDATE INSUMOS_AGRICOLAS 
        SET INSUMO = :2, 
            CATEGORIA = :3, 
            FABRICANTE = :4, 
            VALIDADE = :5, 
            QTDE_EM_ESTOQUE = :6, 
            UNIDADE_DE_MEDIDA = :7, 
            AQUISICAO = :8, 
            VALOR_UNITARIO = :9 
        WHERE ID = :1
    ''', (
        int(row.ID),
        str(row.INSUMO),
        str(row.CATEGORIA),
        str(row.FABRICANTE),
        str(row.VALIDADE),
        float(row.QTDE_EM_ESTOQUE),
        str(row.UNIDADE_DE_MEDIDA),
        str(row.AQUISICAO),
        float(row.VALOR_UNITARIO)
    ))
    conn.commit()

def registros():
    df_list = []
    registro = {
        'INSUMO': input("Digite o insumo que deseja inserir: "),
        'CATEGORIA':input("Digite a categoria do insumo inserido: "),
        'FABRICANTE':input("Digite quem é o fabricante deste insumo: "),
        'VALIDADE':input("Digite a validade do insumo: "),
        'QTDE_EM_ESTOQUE':float(input("Digite a quantidade em estoque deste insumo: ")),
        'UNIDADE_DE_MEDIDA':input("Digite qual a unidade de medida adequada para este insumo: "),
        'AQUISICAO':input("Digite a data de aquisição do insumo: "),
        'VALOR_UNITARIO':float(input("Digite o valor unitário do insumo: "))
    }
    return df_list.append(registro)
 
while True:
    os.system('cls')
    df_list = []
    menu_option = int(input(f'''{'-'*15}
Seleciona a ação que deseja realizar

[1] Cadastrar novo insumo
[2] Consultar insumos
[3] Atualizar insumo
[4] Excluir insumo
[5] Sair
{'-'*15}
'''))
    
    if menu_option > 5 or menu_option < 1:
        os.system('cls')
        print("Ops, algo deu errado\nDigite uma opção valida")
        sleep(3)
        os.system('cls')
        continue

    match menu_option:
        case 1:
            condition = int(input("Você possui um arquivo formatado com os dados que deseja inserir?:\n [1] SIM\n [2] NAO\nDigite: "))
            if condition == 1:
                try:
                    print('O Arquivo deve conter as colunas estrutradas na seguinte ordem:\nINSUMO, CATEGORIA, FABRICANTE, VALIDADE, QUANTIDADE EM ESTOQUE, UNIDADE DE MEDIDA, DATA DE AQUISICAO, VALOR UNITARIO\n')
                    path = input('Digite aqui o diretório do arquivo: ')
                    with open(rf'{path}', 'r') as archive:
                        df = json.load(archive)
                    df = pd.DataFrame(df)
                    df.columns = ['INSUMO', 'CATEGORIA', 'FABRICANTE', 'VALIDADE', 'QTDE_EM_ESTOQUE', 'UNIDADE_DE_MEDIDA', 'AQUISICAO', 'VALOR_UNITARIO']

                except:
                    print('Algo não saiu como esperado, tente novamente.')

            elif condition == 2:
                while True:
                    resp = float(input('Gostaria de inserir mais dados ?:\n[1] SIM\n[2] NAO\nDigite: '))
                    if resp == 2:
                        break
                df = pd.DataFrame(registros)
            cadastro(df, condition)
 
            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')
            
        case 2:
            os.system('cls')
            option = int(input('Qual o tipo de consulta que gostaria de realizar?\n[1] Consulta de registros por lote\n[2] Consulta de registro unico\nDigite aqui: '))
            match option:
                case 1:
                    sql = 'SELECT * FROM INSUMOS_AGRICOLAS WHERE '
                    # print(sql[-6:-1])
                    while True:
                        os.system('cls')
                        ask = int(input('''Quais filtros gostaria de fazer ?\n[1] Filtro de data de valiade\n[2] Filtro de insumos\n[3] Filtro de fabricante\n[4] Filtro de categoria\n\nLEMBRETE: Caso queira refazer algum filtro ja feito, os dados serão sobrepostos\nDigite aqui: '''))
                        match ask:
                            case 1:
                                data_1 = input('Digite a data de validade inicial: ')
                                data_2 = input('Digite a data de validade final: ')
                                sql = sql + f"VALIDADE BETWEEN '{data_1}' and '{data_2}'" if sql[-6:-1] == 'WHERE' else sql + f" and VALIDADE BETWEEN '{data_1}' and '{data_2}'"
                            case 2:
                                insumos = input('Digite separando cada elemento por "," sem espaço, quais insumos deseja analisar: ')
                                sql = sql + ("INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')") if sql[-6:-1] == 'WHERE' else sql + (" and INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')")
                            case 3:
                                fabricante = input('Digite separando cada elemento por "," sem espaço, quais fabricantes deseja consultar: ')
                                sql = sql + ("FABRICANTE in (" + "'" + "', '".join([i for i in fabricante.split(',')]) + "')")  if sql[-6:-1] == 'WHERE' else sql + (" and FABRICANTE in (" + "'" + "', '".join([i for i in fabricante.split(',')]) + "')")
                                print(fabricante)
                            case 4:
                                categoria = input('Digite separando cada elemento por "," sem espaço, quais fabricantes deseja consultar: ')
                                sql = sql + ("CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')") if sql[-6:-1] == 'WHERE' else sql + (" and CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')")
                        if int(input('Gostaria de adicionar mais dados\n[1] SIM\n[2] NAO\nDigite: ')) == 2:
                            os.system('cls')
                            print(F"INSUMOS: {insumos}\nDATA: {data_1} - {data_2}\nFABRICANTE: {fabricante}\nCATEGORIA: {categoria}")
                            sleep(2)
                            break
                case 2:
                    
                        id_consulta = int(input("Insira o ID do registro que deseja vizualizar: "))
                        sql = f'SELECT * FROM INSUMOS_AGRICOLAS WHERE ID = {id_consulta}'
                    
            # print(sql)
            try:
                df_consulta = pd.read_sql(sql, conn)
            except Exception as e:
                os.system('cls')
                print('Algo deu errado.\nTente novamente.')

            print(df_consulta)

            resp = int(input('Deseja extrair os dados?\n[1] SIM\n[2] NAO\nDigite: '))
            try:
                if resp == 1:
                    df_consulta.to_csv(rf'{input("Digite o caminho onde deseja armazenar o arquivo: ")}\{input("Digite um nome para salvar o arquivo: ")}', index=False, sep=';')
                    break
                elif resp > 2 or resp <1:
                    raise(ValueError)
            except ValueError as e:
                print(f'{e} Valor digitado invalido!')
            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')
        
        case 3:
            os.system('cls')
            try:
                id = int(input('Digite o ID do registro que você deseja alterar: '))
                df_att = pd.read_sql(f"SELECT * FROM INSUMOS_AGRICOLAS WHERE ID = {id}", conn)
                if len(df_att) == 0:
                    raise(ValueError)
                print(df_att)
                while True:
                        os.system('cls')
                        alteracao = int(input('Digite o dado que deseja fazer alteração\n[0] Insumo\n[1] Categoria\n[2] Fabricante\n[3] Validade\n[4]Quantidade em estoque\n[5] Unidade de medida\n[6] Aquisicao\n[7] Valor unitario\nDigite aqui: '))
                        option_list = ['INSUMO', 'CATEGORIA', 'FABRICANTE', 'VALIDADE', 'QTDE_EM_ESTOQUE', 'UNIDADE_DE_MEDIDA', 'AQUISICAO', 'VALOR_UNITARIO']
                        df_att[option_list[alteracao]] = input('Digite o valor que deseja atribuir ao campo: ')
                        print(df_att)
                        
                        resp = int(input('Deseja atualizar mais algum registro?\n[1] SIM\n[2] NAO\nDigite: '))
                        if resp == 2:
                            break
                        if resp > 2 or resp < 1:
                            raise(TypeError)
            except Exception as e:
                os.system('cls')
                sleep(2)
                print(e,'Algo deu errado')
                continue
            # update_insumo(df_att.iloc[0])
            
            INSUMO = df_att['INSUMO'].iloc[0]
            CATEGORIA = df_att['CATEGORIA'].iloc[0]
            FABRICANTE = df_att['FABRICANTE'].iloc[0]
            VALIDADE = df_att['VALIDADE'].iloc[0]
            QTDE_EM_ESTOQUE = df_att['QTDE_EM_ESTOQUE'].iloc[0]
            UNIDADE_DE_MEDIDA = df_att['UNIDADE_DE_MEDIDA'].iloc[0]
            AQUISICAO = df_att['AQUISICAO'].iloc[0]
            VALOR_UNITARIO = df_att['VALOR_UNITARIO'].iloc[0]

            cursor.execute(f'''
                UPDATE INSUMOS_AGRICOLAS 
                SET INSUMO = '{str(INSUMO)}', 
                    CATEGORIA = '{str(CATEGORIA)}', 
                    FABRICANTE = '{str(FABRICANTE)}', 
                    VALIDADE = '{str(VALIDADE)}', 
                    QTDE_EM_ESTOQUE = {float(QTDE_EM_ESTOQUE)}, 
                    UNIDADE_DE_MEDIDA = '{str(UNIDADE_DE_MEDIDA)}', 
                    AQUISICAO = '{str(AQUISICAO)}', 
                    VALOR_UNITARIO = {float(VALOR_UNITARIO)}
                WHERE ID = {int(id)}
            ''')
            conn.commit()
            
        case 4:
            os.system('cls')
            id = int(input("Digite o ID do insumo que deseja eliminar do banco de dados: "))
            cursor = conn.cursor()

            try:
                cursor.execute(F"DELETE FROM INSUMOS_AGRICOLAS WHERE ID = {id}")
            except Exception as e:
                print(f'{e} O ID indicado não existe.')

            conn.commit()
            os.system('cls')

        case 5:
            conn.close()
            exit()
