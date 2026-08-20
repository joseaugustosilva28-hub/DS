-- ============================================================
-- Dados iniciais de exemplo (opcional, para testar a API)
-- Rode depois do schema.sql
-- ============================================================

INSERT INTO autores (nome, nacionalidade, ano_nascimento) VALUES
    ('Machado de Assis', 'Brasileira', 1839),
    ('Clarice Lispector', 'Brasileira', 1920),
    ('George Orwell',    'Britanica',  1903),
    ('Agatha Christie',  'Britanica',  1890);

INSERT INTO livros (titulo, ano, preco, autor_id) VALUES
    ('Dom Casmurro',              1899, 39.90, 1),
    ('Memorias Postumas de Bras Cubas', 1881, 45.50, 1),
    ('Quincas Borba',             1891, 42.00, 1),
    ('A Hora da Estrela',         1977, 34.90, 2),
    ('A Paixao Segundo G.H.',     1964, 52.30, 2),
    ('1984',                      1949, 49.90, 3),
    ('A Revolucao dos Bichos',    1945, 29.90, 3);

-- Obs.: a autora Agatha Christie (id 4) fica sem livros de proposito,
-- para demonstrar a rota com LEFT JOIN (/autores/sem-livros).
