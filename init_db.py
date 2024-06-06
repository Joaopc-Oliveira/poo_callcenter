import sqlite3

def init_db():
    conn = sqlite3.connect('hamburgueria.db')
    c = conn.cursor()

    # Criação das tabelas
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            morada TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS hamburgueres (
            nome_hamburguer TEXT PRIMARY KEY,
            ingredientes TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            nome_hamburguer TEXT,
            quantidade INTEGER NOT NULL,
            tamanho TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            valor_total REAL NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
            FOREIGN KEY (nome_hamburguer) REFERENCES hamburgueres (nome_hamburguer)
        )
    ''')

    # Verificar e adicionar a coluna 'imagem' se necessário
    c.execute("PRAGMA table_info(hamburgueres)")
    columns = [column[1] for column in c.fetchall()]
    if 'imagem' not in columns:
        c.execute("ALTER TABLE hamburgueres ADD COLUMN imagem TEXT")

    # Verificar se o registro já existe antes de inserir os dados iniciais
    hamburgueres = [
        ('Cheeseburger', 'Pão, Carne, Queijo, Alface, Tomate', 'cheeseburger.png'),
        ('Hamburger de Frango', 'Pão, Frango, Alface, Maionese', 'frango.png')
    ]

    for hamburguer in hamburgueres:
        c.execute('''
            INSERT OR IGNORE INTO hamburgueres (nome_hamburguer, ingredientes, imagem)
            VALUES (?, ?, ?)
        ''', hamburguer)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
