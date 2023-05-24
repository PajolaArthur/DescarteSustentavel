DROP TABLE IF EXISTS coletas;

CREATE TABLE coletas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao TEXT NOT NULL,
    quantidade TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    diacoleta TEXT NULL,
    horacoleta TEXT NULL,
    situacao TEXT NOT NULL
)

