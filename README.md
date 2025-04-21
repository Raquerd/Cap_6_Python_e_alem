# FIAP - INTELIGENCIA ARTIFICIAL- 2025

Este repositório armazena a atividade "Cap 6 - Python e além", proposto pela FIAP.

https://github.com/Raquerd/Cap_6_Python_e_alem

## Proposta
**Analise e armazenamento de dados de insumos utilizando banco de dados**

O agronegócio digital vem passando por profundas transformações, impulsionado pelo uso de tecnologias e ferramentas que permitem maior controle, automação e tomada de decisão baseada em dados. Dentro desse cenario, o gerenciamento de recursos se destaca como uma área estratégica, capaz de impactar diretamente os custos e a eficiência operacional das propriedades rurais.

O problema escolhido para este estudo está diretamente relacionado à falta de gerenciamento adequado dos recursos no agronegócio, o que resulta em custos adicionais, desperdício de insumos e uso ineficiente de equipamentos e mão de obra. Essa situação é recorrente em diversas regiões produtoras e, frequentemente, decorre da ausência de sistemas de monitoramento, controle e planejamento integrados.

Diante desse cenário, foi desenvolvido um script capaz de realizar as operações de consulta, inserção, extração e limpeza de dados. O objetivo dessa solução é organizar, centralizar e otimizar o controle das informações, proporcionando uma gestão mais eficiente dos recursos utilizados nas atividades agrícolas, além de apoiar a tomada de decisão baseada em dados confiáveis e atualizados.

### Problemas enfrentados durante o desenvolvimento
**Conexão**
Durante o desenvolvimento da atividade, enfrentei diversos desafios, mas, sem dúvida, o que mais me limitou foi a dificuldade de acesso ao banco de dados Oracle disponibilizado pela FIAP.

Iniciei o desenvolvimento dos scripts no sábado, após já ter realizado testes prévios de conexão, onde tudo parecia funcionar corretamente. No entanto, ao tentar implementar essa conexão em um ambiente Python, tive meu acesso negado pelo servidor.

Essa limitação me obrigou a adaptar a solução, utilizando o banco de dados local (sys) para realizar os testes e execuções dos scripts. Embora essa alternativa tenha permitido a continuidade do projeto, ela acabou restringindo algumas funcionalidades e simulações que só seriam possíveis no ambiente Oracle institucional.

**Update dos dados**
Por motivos desconhecido, durante o desenvolvimento da opção de atualização de dados, ao tentar realizar o update no banco de dados local, nenhuma ação era realizada.

Esse problema persistiu por algumas horas, mas foi resolvida apenas no momento em que decidimos reiniciar minha maquina, o que resolveu todo o problema.

### Diferenciais
- Opção de consulta em lote ou registro unico.
- Opção de extração de dados de consulta, o que possibilita analise com ferramentas externas.
- Loop de alteração para realizar update de todos os dados de uma só vez.
- Opção de inserção de dados em lote utilizando arquivo externo.

## Chat GPT

### Prompts utilizados

**Resumo de atividades**

Para evitar ter que reler as atividades e resumir o que é necessário para ser feito, utilizei um prompt que me deu um bom direcionamento e dicas de como realizar as tarefas.
```bash
Boa noite, gostaria que você fosse meu assistente na Faculdade FIAP. 
Atualmente entrei na Faculdade da FIAP na área de Inteligência Artificial e Machine Learning. 
Gostaria que você fosse meu colega veterano, que me ajudasse com as atividades e a entender melhor como elas funcionam. 
Gostaria que evitasse fantasias computacionais, a não ser em exemplos, e que utilizasse uma linguagem não muito técnica.
```
**Ajuda com Oracle e duvidas de banco de dados.**

Eu ja tenho costume de mexer com banco de dados, mais especificamente SQL Server, MySQL e Redshift.

Entretanto Oracle é novo para mim, o que me fez precisar de conselhos para desenvolvimento de colunas alto incrementais e tipagem dos dados.
```bash
Boa tarde.
Gostaria que seguisse o {ROTEIRO} e aplicasse as {REGRAS}

{ROTEIRO}
Gostaria que você se comportasse como um Especialista na area de dados.
Seja meu instrutor e me ajude na retirada de duvidas relacionadas a banco de dados.

{REGRAS}
>Evite ao máximo fantasias computacionais.
>Utilize uma linguagem clara e não muito técnica.
>Me apresente exemplos.
>Me passe instruções com base na documentação atualizada do Oracle.
```

**Python.**

Durante o desenvolvimento da script tive diversos problemas relacionados a conexão, inclusive meu loggin no servidor da FIAP foi barrado.

Para resolver esses problemas, chat que ja utilizo todos os dias em meu trabalho relacionado a python.
```bash
Quero que você atue como um especialista da linguagem python, seguindo a {BASE} e as {REGRAS}

{BASE}
Você deve atuar como um especialista na linguagem python, optando por sempre que montar um código, desenvolve-lo com boas práticas evitando soluções medíocres ou sem embasamento.

{REGRAS}
>O código deve ser funcional.
>Evite fantasias computacionais em casos onde eu lhe forneço uma situação para ser trabalhada.
>Apresente explicações breves sobre cada parte do código com uma linguagem simples para facilitação do aprendizado.
```
