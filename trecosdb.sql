DROP DATABASE IF EXISTS trecosdb;

CREATE DATABASE trecosdb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE trecosdb;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_nascimento DATE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    status ENUM('on', 'off', 'del') DEFAULT 'on'
);

CREATE TABLE Trecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foto VARCHAR(255),
    nome VARCHAR (255) NOT NULL,
    descricao TEXT,
    localizacao VARCHAR(255),
    status ENUM('on', 'off', 'del') DEFAULT 'on',
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

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
    data,
    foto,
    nome,
    descricao,
    localizacao,
    user_id
    ) VALUES (
        CURRENT_DATE,
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

-- Edita o item
UPDATE Trecos
    SET nome = 'Treco muito mais legal',
    descricao = 'Esse treco é muito mais legal',
    status = 'off'
    WHERE id = 1;

-- Apaga o item
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