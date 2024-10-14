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
    senha VARCHAR(10) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela reclamacoes
CREATE TABLE IF NOT EXISTS reclamacoes (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária
    usuario_id INT, -- Chave estrangeira referenciando a tabela usuarios
    tipo_reclamacao_id INT NULL,
    descricao TEXT NOT NULL,
    cidade VARCHAR(255) NOT NULL, -- Cidade do usuário que fez a reclamação (FK)
    bairro VARCHAR(255) NOT NULL, -- Bairro do usuário que fez a reclamação (FK)
    anexo VARCHAR(255), -- Indica se há anexo ou não
    status VARCHAR(20) NULL DEFAULT 'pendente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id), -- Chave estrangeira que refere a usuários
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela tipo_reclamacao
CREATE TABLE IF NOT EXISTS tipos_de_reclamacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL
);

-- Tabela cidades
CREATE TABLE IF NOT EXISTS cidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL
);

-- Tabela bairros
CREATE TABLE IF NOT EXISTS bairros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade_id INT NOT NULL,
    FOREIGN KEY (cidade_id) REFERENCES cidades(id)
);
