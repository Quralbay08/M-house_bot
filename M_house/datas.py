import sqlite3


db = sqlite3.connect('work.db')
cur = db.cursor()
async def start_db():

    #--------------qollaniwshilar--------------------
    cur.execute('''
CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                username TEXT,
                phone_num TEXT,
                adress TEXT
)
''')
    #--------------jumisshilaar--------------------
    cur.execute('''
CREATE TABLE IF NOT EXISTS workers(
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                phone_num TEXT,
                gender TEXT
)
''')
    #<----------about worker----------->
    cur.execute('''
CREATE TABLE IF NOT EXISTS about_worker(
                id INTEGER,
                qarz_w TEXT,
                qarz_s TEXT,
                FOREIGN KEY(id) REFERENCES workers(id)
)
''')
    cur.execute('''
CREATE TABLE IF NOT EXISTS at_about_worker(
                id INTEGER,
                is_at_work TEXT,
                is_working_now TEXT,
                FOREIGN KEY(id) REFERENCES workers(id)
)
''')



def get_workers_info():

    query = '''
    SELECT w.id, 
           w.name, 
           w.surname, 
           w.phone_num, 
           w.gender, 
           COALESCE(aw.qarz_w, 'joq') AS qarz_w, 
           COALESCE(aw.qarz_s, 'joq') AS qarz_s, 
           COALESCE(aaw.is_at_work, 'joq') AS is_at_work, 
           COALESCE(aaw.is_working_now, 'joq') AS is_working_now
    FROM workers w
    LEFT JOIN about_worker aw ON w.id = aw.id
    LEFT JOIN at_about_worker aaw ON w.id = aaw.id
    '''
    
    cur.execute(query)
    workers = cur.fetchall()

    return workers



#------------add worker----------  
async def add_worker(name,surname,phone_num,gender):
    cur.execute('''INSERT INTO workers(name,surname,phone_num,gender)
                    VALUES(?,?,?,?)
''',(name,surname,phone_num,gender))
    db.commit()


#<------------add about worker------------->
async def add_about_worker(id,qarz_w,qarz_s):
    cur.execute('''INSERT INTO about_worker(id,qarz_w,qarz_s)
                      VALUES(?,?,?)
''',(id,qarz_w,qarz_s))
    db.commit()

async def add_at_about_worker(id,is_at_work,is_working_now):
    cur.execute('''INSERT INTO at_about_worker(id,is_at_work,is_working_now)
                      VALUES(?,?,?)
''',(id,is_at_work,is_working_now))
    db.commit()



#<---------update about worker--------->

async def update_about_worker(id,qarz_s,qarz_w):
    cur.execute('''UPDATE about_worker 
        SET qarz_s = ?
        WHERE id = ? AND qarz_w = ?
        ''', (qarz_s, id, qarz_w))
    db.commit()


async def update_worker_about(id,is_at_work,is_working_now):
    cur.execute('''UPDATE at_about_worker 
        SET is_at_work = ?, is_working_now = ?
        WHERE id = ?
        ''', (is_at_work, is_working_now, id))
    db.commit()


#<---------delete about worker------------>
async def delete_worker(id,qarz_w):
    cur.execute('''DELETE FROM about_worker
    WHERE id=? AND qarz_w=?
    ''', (id,qarz_w))
    db.commit()



#------------users-------------

async def show_users():
    users = cur.execute('SELECT * FROM users')
    return users.fetchall()


#--------------------------------qollaniwshilar ushin----------------------------
    
async def add_user(id,name,surname,phone_num):
    cur.execute('''INSERT INTO users(id,name,surname,phone_num)
                VALUES(?,?,?,?)
''',(id,name,surname,phone_num,))
    db.commit()
















