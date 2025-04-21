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

## Extabelece uma conexão com o banco de dados local
conn = oracledb.connect(user="sys", password="090402", dsn='localhost:1521/XEPDB1', mode=oracledb.SYSDBA)

## Cria um cursor
cursor = conn.cursor()

## Procedimento de cadastro de dados
def cadastro(dataframe):
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

# MENU
## Laço de execução do MENU
while True:
    os.system('cls')
    df_list = []
    ## Opções do MENU
    menu_option = int(input(f'''{'-'*15}
Seleciona a ação que deseja realizar

[1] Cadastrar novo insumo
[2] Consultar insumos
[3] Atualizar insumo
[4] Excluir insumo
[5] Sair
{'-'*15}
'''))
    
    ## Identificador de opções validas para o MENU
    if menu_option > 5 or menu_option < 1:
        os.system('cls')
        print("Ops, algo deu errado\nDigite uma opção valida")
        sleep(1)
        os.system('cls')
        continue
    
    ## Bloco condicional: Executará as opções do MENU com base na resposta do usuário
    match menu_option:

        ## Bloco condicional: Seleção de ações de opção 1 do MENU
        case 1:
            os.system('cls')

            ## Bloco de excessão: Evitar erro Datatype invalido
            try:

                ## Captura a resposta do usuario para execução de blocos condicionais
                condition = int(input("Você possui um arquivo JSON formatado com os dados que deseja inserir?:\n [1] SIM\n [2] NAO\nDigite: "))
            except:
                os.system('cls')
                print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                sleep(2)
                os.system('cls')
                continue

            ## Bloco condicional: Verificar se a opção é igual a "1" e executar o código
            if condition == 1:

                ## Bloco de excessão: Evitar erros de campo não preenchido
                try:
                    print('O Arquivo deve conter as colunas estrutradas na seguinte ordem:\nINSUMO, CATEGORIA, FABRICANTE, VALIDADE, QUANTIDADE EM ESTOQUE, UNIDADE DE MEDIDA, DATA DE AQUISICAO, VALOR UNITARIO\n')

                    ## Caputra o caminho do arquivo salvo
                    path = input('Digite aqui o diretório do arquivo: ')

                    ## Realiza a abertura do arquivo Json
                    with open(rf'{path}', 'r') as archive:
                        df = json.load(archive)

                    ## Transforma o JSON em DataFrame
                    df = pd.DataFrame(df)
                    df.columns = ['INSUMO', 'CATEGORIA', 'FABRICANTE', 'VALIDADE', 'QTDE_EM_ESTOQUE', 'UNIDADE_DE_MEDIDA', 'AQUISICAO', 'VALOR_UNITARIO']

                except:
                    os.system('cls')
                    print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                    sleep(2)
                    os.system('cls')
                    continue
                    
            
            ## Bloco condicional: Verificar se a opção é igual a "2" e executar o código.
            elif condition == 2:
                os.system('cls')

                ## Bloco de loop: Executa um loop para realizar cadastros de dados até que o usuário realize a quebra.
                while True:

                    ## Cria uma lista vazia
                    df_list = []

                    ## Bloco de excessão: Valida se os dados inseridos serão corretos
                    try:

                    ## Armazena os dados de cadastro em formato de dicionário
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
                    except:
                        print(f'O valor digitado não é valido, tente novamente')
                        sleep(2)
                        os.system('cls')
                        continue
                
                    os.system('cls')

                    ## Adiciona o dicionário dentro de uma lista
                    df_list.append(registro)

                    ## Transforma a lista em DataFrame
                    df = pd.DataFrame(df_list)
                    df = df.astype({'INSUMO':str, 'CATEGORIA':str, 'FABRICANTE':str, 'VALIDADE':str, 'QTDE_EM_ESTOQUE':float, 'UNIDADE_DE_MEDIDA':str, 'AQUISICAO':str, 'VALOR_UNITARIO':float})

                    ## Captura a resposta do usuario
                    resp = float(input('Gostaria de inserir mais dados ?:\n[1] SIM\n[2] NAO\nDigite: '))

                    ## Bloco condicional: Caso a resposta seja 2, realiza a quebra
                    if resp == 2:
                        os.system('cls')
                        break
            ## Bloco condicional: Verifica se a resposta foi fora das opções oferecidas.
            else:
                os.system('cls')
                print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                sleep(2)
                os.system('cls')
                continue

            ## PROCEDIMENTO: Realiza cadastro dos dados inseridos no DataFrame  
            cadastro(df)

            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')

        ## Bloco condicional: Seleção de ações de opção 2 do MENU
        case 2:
            os.system('cls')

            ## Bloco de loop: Executa um loop para validar se a resposta do usuario é valida para que assim o loop seja executado novamente.
            while True:

                ## Bloco de excessão: Verifica se a resposta do usuário é valida.
                try:

                    ## Caputura a opção que o usuário deseja utilizar
                    option = int(input('Qual o tipo de consulta que gostaria de realizar?\n[1] Consulta de registros por lote\n[2] Consulta de registro unico\nDigite aqui: '))
                    break
                except:
                    os.system('cls')
                    print('Digite um valor valido.')
                    os.system('cls')
                    continue
            
            ## Bloco condicional: Executa a opção "1" caso o usuário tenha a selecionado (Filtragem por lote)
            if option == 1:

                ## Variavel que armazena uma parte de uma Query
                sql = 'SELECT * FROM INSUMOS_AGRICOLAS WHERE '

                ## Bloco de loop: Executara repetidamente o código, enquanto o usuário precisar inserir condições
                while True:
                    os.system('cls')

                    ## Captura o tipo de consulta que o usuário deseja realizar
                    ask = int(input('''Quais filtros gostaria de fazer ?\n[1] Filtro de data de valiade\n[2] Filtro de insumos\n[3] Filtro de fabricante\n[4] Filtro de categoria\n\nLEMBRETE: Caso queira refazer algum filtro ja feito, os dados serão sobrepostos\nDigite aqui: '''))
                    
                    ## Bloco condicional das opções de filtros do usuário:
                    match ask:

                        ## Bloco condicional: Insere filtro de data e concatena na variavel "sql"
                        case 1:
                            data_1 = input('Digite a data de validade inicial: ')
                            data_2 = input('Digite a data de validade final: ')
                            sql = sql + f"VALIDADE BETWEEN '{data_1}' and '{data_2}'" if sql[-6:-1] == 'WHERE' else sql + f" and VALIDADE BETWEEN '{data_1}' and '{data_2}'"
                        
                        ## Bloco condicional: Insere filtro de insumos e concatena na variavel "sql"
                        case 2:
                            insumos = input('Digite separando cada elemento por "," sem espaço, quais insumos deseja analisar: ')
                            sql = sql + ("INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')") if sql[-6:-1] == 'WHERE' else sql + (" and INSUMO in (" + "'" + "', '".join([i for i in insumos.split(',')]) + "')")
                        
                        ## Bloco condicional: Insere filtro de fabricante e concatena na variavel "sql"
                        case 3:
                            fabricante = input('Digite separando cada elemento por "," sem espaço, quais fabricantes deseja consultar: ')
                            sql = sql + ("FABRICANTE in (" + "'" + "', '".join([i for i in fabricante.split(',')]) + "')")  if sql[-6:-1] == 'WHERE' else sql + (" and FABRICANTE in (" + "'" + "', '".join([i for i in fabricante.split(',')]) + "')")
                            print(fabricante)
                        
                        ## Bloco condicional: Insere filtro de categoria e concatena na variavel "sql"
                        case 4:
                            categoria = input('Digite separando cada elemento por "," sem espaço, quais fabricantes deseja consultar: ')
                            sql = sql + ("CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')") if sql[-6:-1] == 'WHERE' else sql + (" and CATEGORIA in (" + "'" + "', '".join([i for i in categoria.split(',')]) + "')")
                    
                    ## Bloco condicional: Verifica se o usuário deseja inserir mais filtros ou não, e realiza a quebra do bloco de loop
                    if int(input('Gostaria de adicionar mais dados\n[1] SIM\n[2] NAO\nDigite: ')) == 2:
                        os.system('cls')

                        ## Exibe os filtros que o usuário realizou
                        print(F"INSUMOS: {insumos}\nDATA: {data_1} - {data_2}\nFABRICANTE: {fabricante}\nCATEGORIA: {categoria}")
                        sleep(2)
                        break
            ## Bloco condicional: Executa a opção "2" caso o usuário tenha a selecionado (Filtro por ID)            
            elif option == 2:    

                ## Captura o ID selecionado para realizar a consulta
                id_consulta = int(input("Insira o ID do registro que deseja vizualizar: "))
                sql = f'SELECT * FROM INSUMOS_AGRICOLAS WHERE ID = {id_consulta}'
            
            ## Bloco condicional: Verifica se a resposta foi fora das opções oferecidas
            else:
                os.system('cls')
                print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                sleep(2)
                os.system('cls')
                continue

            

            ## Bloco de excessão: Verifica se a consulta será realizada corretamente e se tem dados no DataFrame
            try:

                ## Realiza a consulta no SQL e trás para um DataFrame
                df_consulta = pd.read_sql(sql, conn)

                ## Bloco condicional: Analisa se há dados no DataFrame
                if len(df_consulta) == 0:
                    raise(ValueError)
            except Exception as e:
                os.system('cls')
                print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                sleep(2)
                os.system('cls')
                continue

            os.system('cls')

            ## Exibe os dados de consulta
            print(df_consulta)

            ## Captura a resposta do usuário sobre a extração de dados para um arquivo
            resp = int(input('Deseja extrair os dados?\n[1] SIM\n[2] NAO\nDigite: '))

            ## Bloco de excessão: Verifica se a resposta do usuário é valida
            try:

                ## Bloco condicional: Verifica se a resposta é igual a "1", realiza as ações realiza a quebra do bloco
                if resp == 1:
                    df_consulta.to_csv(rf'{input("Digite o caminho onde deseja armazenar o arquivo: ")}\{input("Digite um nome para salvar o arquivo: ")}', index=False, sep=';')
                    break

                ## Bloco condicional: Verifica se a resposta é invalida e retorna um erro.
                elif resp > 2 or resp <1:
                    raise(ValueError)
            except ValueError as e:
                print(f'{e} Valor digitado invalido!')
            input('Pressione ENTER para prosseguir para o MENU.')
            os.system('cls')
        
        ## Bloco condicional: Seleção de ações de opção 3 do MENU
        case 3:
            os.system('cls')
            
            ## Bloco de excessão: Verifica se a consulta realizada retora dados no DataFrame
            try:

                ## Captura o ID selecionado para realizar a consulta
                id = int(input('Digite o ID do registro que você deseja alterar: '))

                ## Realiza a consulta no banco de daados e tras para um DataFrame
                df_att = pd.read_sql(f"SELECT * FROM INSUMOS_AGRICOLAS WHERE ID = {id}", conn)

                ## Bloco condicional: Verifica se o DataFrame não possui dados e retorna um erro
                if len(df_att) == 0:
                    raise(ValueError)
                print(df_att)

                ## Bloco de loop: Realiza alterações no DataFrame de forma individual com repetição
                while True:
                        os.system('cls')

                        ## Captura qual campo o usuario deseja alterar
                        alteracao = int(input('Digite o dado que deseja fazer alteração\n[0] Insumo\n[1] Categoria\n[2] Fabricante\n[3] Validade\n[4]Quantidade em estoque\n[5] Unidade de medida\n[6] Aquisicao\n[7] Valor unitario\nDigite aqui: '))
                        
                        ## Cria uma lista de opções validas para puxar no dataframe
                        option_list = ['INSUMO', 'CATEGORIA', 'FABRICANTE', 'VALIDADE', 'QTDE_EM_ESTOQUE', 'UNIDADE_DE_MEDIDA', 'AQUISICAO', 'VALOR_UNITARIO']

                        ## Caputra o dado que o usuario vai realizar alteração
                        df_att[option_list[alteracao]] = input('Digite o valor que deseja atribuir ao campo: ')
                        print(df_att)
                        
                        ## Captura se o usuário deseja prosseguir ou não com mais alterações
                        resp = int(input('Deseja atualizar mais algum registro?\n[1] SIM\n[2] NAO\nDigite: '))

                        ## Bloco condicional: Verifica a resposta do usuário e retorna uma quebra de bloco
                        if resp == 2:
                            break

                        ## Bloco condicional: Valida se a reposta do usuário está dentro das opções fornecidas e retorna um erro.
                        if resp > 2 or resp < 1:
                            raise(TypeError)
            except Exception as e:
                os.system('cls')
                print('Ops! algo não saiu como esperado!\nExecute o código novamente e preencha os campos solicitados de forma correta.')
                sleep(2)
                os.system('cls')
                continue

            ## Definindo constantes para Update.
            INSUMO = df_att['INSUMO'].iloc[0]
            CATEGORIA = df_att['CATEGORIA'].iloc[0]
            FABRICANTE = df_att['FABRICANTE'].iloc[0]
            VALIDADE = df_att['VALIDADE'].iloc[0]
            QTDE_EM_ESTOQUE = df_att['QTDE_EM_ESTOQUE'].iloc[0]
            UNIDADE_DE_MEDIDA = df_att['UNIDADE_DE_MEDIDA'].iloc[0]
            AQUISICAO = df_att['AQUISICAO'].iloc[0]
            VALOR_UNITARIO = df_att['VALOR_UNITARIO'].iloc[0]

            ## Bloco de excessão
            try:

                ## Realiza um update na tabela do banco de dados
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
            except Exception as e:
                print(f'Erro ao atualizar registro: {e}')
                continue
        
        ## Bloco condicional: Seleção de ações de opção 4 do MENU
        case 4:
            os.system('cls')

            ## Bloco de excessão: Analisa se o dado inserido na captura esta correto
            try:

                ## Captura o ID que o usuário deseja limpar
                id = int(input("Digite o ID do insumo que deseja eliminar do banco de dados: "))
            except:
                print('Algo deu errado!')
                sleep(3)
                continue
            cursor = conn.cursor()

            ## Bloco de excessão: Verifica se a limpeza será realizada corretamente
            try:

                ## Executa uma limpeza na tabela do banco de dados.
                cursor.execute(F"DELETE FROM INSUMOS_AGRICOLAS WHERE ID = {id}")
            except Exception as e:
                print(f'{e} O ID indicado não existe.')

            conn.commit()
            os.system('cls')

        ## Bloco condicional: Seleção de ações de opção 5 do MENU
        case 5:

            ## Encerra a conexão com o banco de dados
            conn.close()

            ## Encerra a script
            exit()
