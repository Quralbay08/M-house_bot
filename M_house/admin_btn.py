from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from datas import cur

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.add(KeyboardButton(text='Jumısshılardı kóriw'))
admin_menu.add(KeyboardButton(text="Jumısshı qosıw"),KeyboardButton(text='Qarz qosıw'))
admin_menu.add(KeyboardButton(text='Qarzdı ózgertiriw'),KeyboardButton(text='Qarzdı óshiriw'))
admin_menu.add(KeyboardButton(text='Jumısshı halatın qosıw'),KeyboardButton(text='Jumısshı halatın ógertiriw'))

def create_worker_buttons():
    cur.execute('SELECT * FROM workers')
    rows = cur.fetchall()
    cur.execute('SELECT * FROM at_about_worker')
    about = cur.fetchall()
    
    if not rows:
        return None
    if not about:
        return None
    
    keyboard = InlineKeyboardMarkup()
    for about in about:
        for row in rows:
            if about==row:
                button_text = f"Ati:{row[1]} Familiasi:{row[2]}"  # name, surname va phone_num
                keyboard.add(InlineKeyboardButton(button_text, callback_data=f"delete_{row[0]}"))

    return keyboard

def workers_buttons():
    cur.execute('''SELECT w.id, w.name, w.surname 
    FROM workers w
    LEFT JOIN at_about_worker aw ON w.id = aw.id
    WHERE aw.is_at_work IS NULL AND aw.is_working_now IS NULL''')
    workers = cur.fetchall()
    
    markup = InlineKeyboardMarkup(row_width=1)
    for worker in workers:
        button = InlineKeyboardButton(f"{worker[1]} {worker[2]}", callback_data=f"worker_{worker[0]}")
        markup.add(button)
    return markup

# Ish holati uchun inline tugmalar
def status1_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("awa", callback_data="status1_awa"), InlineKeyboardButton("yaq", callback_data="status1_yaq"))
    return markup

def status2_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("awa", callback_data="status2_awa"), InlineKeyboardButton("yaq", callback_data="status2_yaq"))
    return markup

def update_worker_buttons():
    cur.execute('SELECT * FROM workers')
    workers = cur.fetchall()
    
    if not workers:
        return None

    keyboard = InlineKeyboardMarkup()
    for worker in workers:
        button_text = f"{worker[1]} {worker[2]}"  # name, surname va phone_num
        keyboard.add(InlineKeyboardButton(button_text, callback_data=f"_update_{worker[0]}"))

    return keyboard

def update_status1_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("awa", callback_data="update_status1_awa"), InlineKeyboardButton("yaq", callback_data="update_status1_yaq"))
    return markup

def update_status2_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("awa", callback_data="update_status2_awa"), InlineKeyboardButton("yaq", callback_data="update_status2_yaq"))
    return markup


    