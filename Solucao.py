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

 
while True:
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
                    df_list.append(registro)
                    resp = float(input('Gostaria de inserir mais dados ?:\n[1] SIM\n[2] NAO\nDigite: '))
                    if resp == 2:
                        break
                df = pd.DataFrame(df_list)
            cadastro(df, condition)
 
            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')
            
        case 2:
            os.system('cls')
            option = int(input('Qual o tipo de consulta que gostaria de realizar?\n[1] Consulta de registros por lote\n[2] Consulta de registro unico\nDigite aqui: '))
            match option:
                case 1:
                    data_1 = ''
                    data_2 = ''
                    insumos = ''
                    fabricante = ''
                    categoria = ''
                    sql = 'SELECT * FROM INSUMOS_AGRICOLAS WHERE'

                    while True:
                        os.system('cls')
                        ask = int(input('''Quais filtros gostaria de fazer ?\n[1] Filtro de data de valiade\n[2] Filtro de insumos\n[3] Filtro de fabricante\n[4] Filtro de categoria\n\nLEMBRETE: Caso queira refazer algum filtro ja feito, os dados serão sobrepostos\nDigite aqui: '''))
                        match ask:
                            case 1:
                                data_1 = input('Digite a data de validade inicial: ')
                                data_2 = input('Digite a data de validade final: ')
                                sql = sql + f" VALIDADE >= {data_1} and VALIDADE <= {data_2}" if 'and' not in sql else sql + f" and VALIDADE >= {data_1} and VALIDADE <= {data_2}"
                            case 2:
                                insumos = input('Digite separando cada elemento por "," quais insumos deseja analisar: ').strip()
                                sql = sql + (" INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')") if 'and' not in sql else sql + (" and INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')")
                            case 3:
                                fabricante = pd.read_sql('SELECT DISTINCT FABRICANTE FROM INSUMOS_AGRICOLAS', conn)
                                # input(f'''Digite separando cada elemento por "," quais fabricantes deseja consultar.\nLista de fabricantes\n{pd.read_sql('SELECT DISTINCT FABRICANTE FROM INSUMOS_AGRICOLAS', conn)}\nDigite aqui:''').strip()
                                fabricante_list = []
                                while True:
                                    fabricante_list.append(fabricante.loc[int(input(f'''Digite o numero referente a qual fabricantes deseja consultar.\nLista de fabricantes\n{fabricante}\nDigite aqui:'''))])
                                    print(fabricante_list)
                                    if int(input("Deseja inserir mais algum fabricane na consulta?\n[1] SIM\n[2] NAO\nDigite: ")) == 2:
                                        break
                                sql = sql + (" FABRICANTE in (" + "'" + "', '".join([i for i in fabricante_list]) + "')") if 'and' not in sql else sql + (" and FABRICANTE in (" + "'" + "', '".join([i for i in fabricante_list]) + "')")
                                print(sql)
                            case 4:
                                categoria = input('Digite separando cada elemento por "," quais fabricantes deseja consultar: ').strip()
                                sql = sql + (" CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')") if 'and' not in sql else sql + (" and CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')")
                        if int(input('Gostaria de adicionar mais dados\n[1] SIM\n[2] NAO\nDigite: ')) == 2:
                            # os.system('cls')
                            print(F"INSUMOS: {insumos}\nDATA: {data_1} - {data_2}\nFABRICANTE: {fabricante_list}\nCATEGORIA: {categoria}")
                            break
                case 2:
                    id_consulta = int(input("Insira o ID do registro que deseja vizualizar: "))

            df_cosulta = pd.read_sql(sql, conn)
            print(df_cosulta)

            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')

        
        case 4:
            os.system('cls')
            id = int(input("Digite o ID do insumo que deseja eliminar do banco de dados: "))
            cursor = conn.cursor()
            cursor.execute(F"DELETE FROM INSUMOS_AGRICOLAS WHERE ID = {id}")
            conn.commit()
            os.system('cls')

        case 5:
            conn.close()
            exit()
