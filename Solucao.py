import oracledb, pandas as pd, os
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
# aaaaa
df = {'INSUMOS':[], 'CATEGORIA':[], 'FABRICANTE':[], 'VALIDADE':[], 'QTDE_EM_ESTOQUE':[], 'UNIDADE_DE_MEDIDA':[], 'AQUISICAO':[], 'VALOR_UNITARIO':[]}
print(df)
def cadastro(dataframe):
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO 
                        INSUMOS_AGRIGOLAS (
                            id,
                            insumo, 
                            categoria, 
                            fabricante, 
                            validade, 
                            qtde_em_estoque, 
                            unidade_de_medida, 
                            aquisição, 
                            valor_unitário)
                        VALUES({dataframe})
                   ''')
 
while True:
    menu_option = int(input(f'''{'-'*15}
                            Seleciona a ação que deseja realizar
                        
                            [1] Cadastrar novo insumo
                            [2] Consultar insumos
                            [3] Atualizar insumo
                            [4] Excluir insumo
                            [5] Sair
                            {'-'*15}
'''))
    match menu_option:
        case 1:
            condition = int(input("Você possui um arquivo formatado com os dados que deseja inserir?:\n [1] SIM\n [2]NAO\nDigite: "))
            if condition == 1:
                try:
                    path = input('Digite aqui o diretório do arquivo: ')
                    with open(path, 'r') as archive:
                        archive.read()
                except:
                    print('erro')
            df['INSUMOS'] = input("Digite o insumo que deseja inserir: ")
            df['CATEGORIA'] = input("Digite a categoria do insumo inserido: ")
            df['FABRICANTE'] = input("Digite quem é o fabricante deste insumo: ")
            df['VALIDADE'] = input("Digite a validade do insumo: ")
            df['QTDE_EM_ESTOQUE'] = float(input("Digite a quantidade em estoque deste insumo: "))
            df['UNIDADE_DE_MEDIDA'] = input("Digite qual a unidade de medida adequada para este insumo: ")
            df['AQUISICAO'] = input("Digite a data de aquisição do insumo: ")
            df['VALOR_UNITARIO'] = float(input("Digite o valor unitário do insumo: "))
            os.system('cls')
            sleep()

        case 2:
            df_cosulta = pd.read_sql('SELECT * FROM INSUMOIS_AGRICOLAS')
            print(df_cosulta)

            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')
        
        # case 3:

            
