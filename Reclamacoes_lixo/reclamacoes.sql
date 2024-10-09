-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS sistema_reclamacoes;
USE sistema_reclamacoes;

-- Tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    uf VARCHAR(2) NOT NULL, -- Estado, representado com 2 caracteres
    bairro VARCHAR(255) NOT NULL,
    profissao VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE, -- Adicionando campo de email como único
    senha VARCHAR(10) NOT NULL
);

-- Tabela reclamacoes
CREATE TABLE IF NOT EXISTS reclamacoes (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária
    usuario_id INT, -- Chave estrangeira referenciando a tabela usuarios
    descricao TEXT NOT NULL,
    cidade VARCHAR(255) NOT NULL, -- Cidade do usuário que fez a reclamação (FK)
    bairro VARCHAR(255) NOT NULL, -- Bairro do usuário que fez a reclamação (FK)
    data DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data da reclamação
    anexo BOOLEAN DEFAULT FALSE, -- Indica se há anexo ou não
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) -- Chave estrangeira que refere a usuários
);
