-- Certifica-se de que o banco de dados `trecosdb` será excluído, caso já exista
DROP DATABASE IF EXISTS trecosdb;

-- Cria o banco de dados `trecosdb`
CREATE DATABASE trecosdb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

-- Seleciona o banco de dados `trecosdb`
USE trecosdb;

-- Criação da tabela `Users`
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_nascimento DATE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    status ENUM('on', 'off', 'del') DEFAULT 'on'
);

-- Criação da tabela `Trecos`
CREATE TABLE Trecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foto VARCHAR(255),
    nome VARCHAR (255) NOT NULL,
    descricao TEXT NOT NULL,
    localizacao VARCHAR(255) NOT NULL,
    status ENUM('on', 'off', 'del') DEFAULT 'on',
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Insere dados em `Users` e em `Trecos`
INSERT INTO Users (
    data_nascimento,
    nome,
    email,
    senha
    ) VALUES (
    '2000-28-02',
    'Álefe',
    'emailmeu@hotmail.com',
    SHA1('123456')
);

INSERT INTO Trecos (
    foto,
    nome,
    descricao,
    localizacao,
    user_id
    ) VALUES (
    'foto.jpg',
    'Treco Legal',
    'Descrição do treco',
    'São Paulo',
    1
);

-- Vê todos os itens de um usuário
SELECT * FROM Trecos
    WHERE user_id = 1;

-- Vê detalhes do item individualmente
SELECT * FROM Trecos
    WHERE id = 1;

-- Edição do item 1
UPDATE Trecos
    SET nome = 'Treco muito mais legal',
    descricao = 'Esse treco é muito mais legal',
    status = 'off'
    WHERE id = 1;

-- Apaga o item 1
DELETE FROM Trecos
    WHERE id = 1;

-- Insere o usuário Romeu
INSERT INTO Users (
	data_nascimento,
	nome,
	email,
	senha
	) VALUES (
    '2003-04-10',
    'Romeu',
    'romeu@vcnsabenemeu.com',
    SHA1('48465456465')
);

-- Insere o usuário Juliana
INSERT INTO Users (
	nome,
	data_nascimento,
	email,
	senha,
	status
	) VALUES (
    'Juliana Lima Abreu',
    '1999-05-15',
    'juliabr@abreu.com',
    SHA1('1748736987r5'),
    'off'
);

-- Insere um item para o user 2
INSERT INTO Trecos (
    `foto`,
    `nome`,
    `descricao`, 
    `localizacao`,
    `user_id`
	) VALUES (
    'foto2.jpg',
    'Teclado',
    'Um K120 da Logitech',
    'Jericoacoara',
    '2'
);

-- Insere um  item para o usuário 1
INSERT INTO Trecos ( 
    `foto`,
    `nome`, 
    `descricao`, 
    `localizacao`,
    `user_id`
	) VALUES (
    'foto3.jpg',
    'Luvas de frio',
    'Luvas para esquentar a mão quando sentir frio',
    'Rio de Janeiro',
    '1'
);

INSERT INTO Users (
    `data_nascimento`,
    `nome`,
    `email`,
    `senha`
    ) VALUES (
    '1945-03-31',
    'Hildebrando Bravo',
    'hilde@brando.com',
    SHA1('fahuh2984928')
);