-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS sistema_reclamacoes;
USE sistema_reclamacoes;

-- Tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    bairro VARCHAR(255) NOT NULL,
    profissao VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE, -- Adicionando campo de email como único
    senha VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela reclamacoes
CREATE TABLE IF NOT EXISTS reclamacoes (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária
    usuario_id INT, -- Chave estrangeira referenciando a tabela usuarios
    tipo_reclamacao VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    cidade VARCHAR(255) NOT NULL, -- Cidade do usuário que fez a reclamação (FK)
    bairro VARCHAR(255) NOT NULL, -- Bairro do usuário que fez a reclamação (FK)
    anexo VARCHAR(255) NULL, -- Indica se há anexo ou não
    status VARCHAR(20) DEFAULT 'pendente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id), -- Chave estrangeira que refere a usuários
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    usuario = db.relationship("Usuario", backref="reclamacoes")
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

CREATE TABLE reclamacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    tipo_reclamacao VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    bairro VARCHAR(255) NOT NULL,
    anexo VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pendente',
    anonimo BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

