import sqlite3

connection = sqlite3.connect('database/database.db')

with open('database/usuarios.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
            ('admin', 
             'admin')
            )

cur.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
            ('arthur', 
             '1234')
            )


connection.commit()
connection.close()

connection = sqlite3.connect('database/database.db')

with open('database/coletas.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO coletas (descricao, quantidade, endereco, telefone, diacoleta, horacoleta, situacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Geladeira', 
             '1', 
             'Prefeitura Municipal de Orlandia', 
             '(16) 99316-2959',
             'Domingo',
             '15:00',
             'Concluída')
            )

cur.execute("INSERT INTO coletas (descricao, quantidade, endereco, telefone, diacoleta, horacoleta, situacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Computador', 
             '12', 
             'Rua Quatro, 520 - Centro', 
             '(34) 99889-2822',
             'Quinta-feira',
             '17:00',
             'Concluída')
            )

cur.execute("INSERT INTO coletas (descricao, quantidade, endereco, telefone, diacoleta, horacoleta, situacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Forno', 
             '2', 
             'ETEC Prof. Alcídio de Souza Prado - Centro', 
             '(16) 99988-0774',
             'Segunda-feira',
             '08:20',
             'Cancelada')
            )

cur.execute("INSERT INTO coletas (descricao, quantidade, endereco, telefone, diacoleta, horacoleta, situacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Micro-ondas', 
             '6', 
             'Rua Vinte e Seis, 1494 - Jardim Cidade Alta', 
             '(16) 99214-5034',
             'Terça-feira',
             'Terça-feira',
             'Concluída')
            )

connection.commit()
connection.close()
