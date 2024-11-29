#<----------from and import---------->

from aiogram import types,Bot,Dispatcher,executor
from M_house import datas,user_btn,admin_btn
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
import re,os
from keep_alive import keep_alive
keep_alive()

#<--------bots data--------->
result = []
token = '6667524460:AAHvxu5j0R_9trNtTwtJCJQY7a0b73zxF38'
storage = MemoryStorage()
bot = Bot(token=os.environ.get(token))
dp = Dispatcher(bot,storage=storage)
admin_id =  [5773032217,7580114812]



async def on_startup(_):
    global admin_id
    # admin_id = 5570471897
    # await bot.send_message(
    #     chat_id=admin_id,
    #     text='Botqa zapusk berildi',
    # )
    await datas.start_db()


#<---------------admin function----------------->

#<---------add worker---------->
class AddWorker(StatesGroup):
    name = State()
    surname = State()
    phone_num = State()
    gender = State()


@dp.message_handler(text="Jumısshı qosıw")
async def Add_worker(message: types.Message):
    await message.answer("Jumısshı qosıw! Jumısshınıń atin kiritiń:",reply_markup=user_btn.tiykargi_menu)
    await AddWorker.name.set()

@dp.message_handler(state=AddWorker.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=admin_btn.admin_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer("Axa, endi bizge familiyası kerek:") 
        await AddWorker.next()

@dp.message_handler(state=AddWorker.surname)
async def process_name(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=admin_btn.admin_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['surname'] = message.text
        await message.answer(f"Júdá jaqsı! Endi telefon nawmerin kiritiń:")
        await AddWorker.next()

@dp.message_handler(state=AddWorker.phone_num)
async def process_name(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=admin_btn.admin_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['phone_num'] = message.text
        gender_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        gender_kb.add(KeyboardButton('Erkek'), KeyboardButton('Ayel'))
        gender_kb.add(KeyboardButton('🏠 Tiykarǵı menyu 🏠'))
        await message.answer("Jınsın tanlań:", reply_markup=gender_kb)
        await AddWorker.next()


@dp.message_handler(state=AddWorker.gender)
async def process_name(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=admin_btn.admin_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['gender'] = message.text
        await datas.add_worker(
                            name=data['name'],
                            surname=data['surname'],
                            phone_num=data['phone_num'],
                            gender=data['gender'])

        await state.finish()
        await message.answer("Jumısshı saqlandı!✅", reply_markup=admin_btn.admin_menu)


#<---------add about worker---------->


@dp.message_handler(text='Qarz qosıw')
async def add_about_worker_handler(message: types.Message):
    cur.execute('SELECT id, name, surname FROM workers')
    workers = cur.fetchall()
    if not workers:
        await message.reply("Hesh qanday jumısshı tabılmadı🙄")
        return

    keyboard = InlineKeyboardMarkup()
    for worker in workers:
        keyboard.add(InlineKeyboardButton(f"{worker[1]} {worker[2]}", callback_data=f"add_about_{worker[0]}"))
    await message.reply("Qarz maǵlumatların qosıw ushın jumısshı tanlań👇:", reply_markup=keyboard)

class AddAboutWorkerState(StatesGroup):
    worker_id = State()
    qarz_w = State()
    qarz_s = State()

@dp.callback_query_handler(lambda c: c.data.startswith('add_about_'))
async def process_add_about_worker(callback_query: types.CallbackQuery, state: FSMContext):
    worker_id = int(callback_query.data.split('_')[-1])
    async with state.proxy() as data:
        data['worker_id'] = worker_id
    await callback_query.message.reply("🔢 Qarz sánesin kiritiń (Mısalı: 01.01.2024):")
    await AddAboutWorkerState.qarz_w.set()

@dp.message_handler(state=AddAboutWorkerState.qarz_w)
async def get_debt_date(message: types.Message, state: FSMContext):
    qarz_w = message.text
    async with state.proxy() as data:
        data['qarz_w'] = qarz_w
    await message.reply("💰 Qarz muǵdarın kiritiń (Mısalı: 10000):")
    await AddAboutWorkerState.qarz_s.set()

@dp.message_handler(state=AddAboutWorkerState.qarz_s)
async def get_debt_amount(message: types.Message, state: FSMContext):
    qarz_s = message.text
    async with state.proxy() as data:
        data['qarz_s'] = qarz_s
        await datas.add_about_worker(id=data['worker_id'], qarz_w=data['qarz_w'], qarz_s=data['qarz_s']) 
    await message.reply(f"Qarz maǵlumatları qosıldı✅:\n\n🔢 Sáne: {data['qarz_w']}\n💰 Múǵdarı: {data['qarz_s']}")
    await state.finish() 
    

@dp.message_handler(text='Qarzdı ózgertiriw')
async def update_about_worker_handler(message: types.Message):
    cur.execute('SELECT w.id, w.name, w.surname, a.qarz_w, a.qarz_s FROM workers w INNER JOIN about_worker a ON w.id = a.id')
    workers = cur.fetchall()
    if not workers:
        await message.reply("Hesh qanday qarzı bar jumısshılar tabılmadı🙄")
        return

    keyboard = InlineKeyboardMarkup()
    for worker in workers:
        keyboard.add(InlineKeyboardButton(f"{worker[1]} {worker[2]} - {worker[3]}", callback_data=f"update_about_{worker[3]}_{worker[0]}"))
    await message.reply("Qarz maǵlumatların jańalaw ushın jumısshı tanlań👇:", reply_markup=keyboard)


class UpdateAboutWorkerState(StatesGroup):
    worker_id = State()
    qarz_w = State()
    qarz_s = State()

@dp.callback_query_handler(lambda c: c.data.startswith('update_about_'))
async def process_update_about_worker(callback_query: types.CallbackQuery, state: FSMContext):
    worker_id = int(callback_query.data.split('_')[-1])
    qarz_w = callback_query.data.split('_')[-2]
    cur.execute('SELECT qarz_s FROM about_worker WHERE id = ? AND qarz_w = ?', (worker_id,qarz_w))
    result = cur.fetchone()
    if result:
        async with state.proxy() as data:
            data['worker_id'] = worker_id
            data['qarz_w'] = qarz_w
        await bot.send_message(callback_query.from_user.id, f"💰 Házirgi qarz muǵdarı: {result[0]}\n👉 Jańa qarz muǵdarın kiritiń:")
        await UpdateAboutWorkerState.qarz_s.set()

@dp.message_handler(state=UpdateAboutWorkerState.qarz_s)
async def process_new_debt_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['qarz_s'] = message.text
        await datas.update_about_worker(id=data['worker_id'],qarz_w=data['qarz_w'],qarz_s=message.text)
    await message.reply("Qarz muǵdarı jańalandı😁")
    await state.finish()


        
    
#<-------delete about worker--------->
from datas import cur

async def show_about_workers():
    cur.execute('SELECT * FROM about_worker')
    return cur.fetchall()

async def show_at_about_workers():
    cur.execute('SELECT * FROM at_about_worker')
    return cur.fetchall()

async def get_workers():
    cur.execute("SELECT * FROM workers")
    return cur.fetchall()

@dp.message_handler(text='Qarzdı óshiriw')
async def delete_about_worker_handler(message: types.Message):
    cur.execute('SELECT w.id, w.name, w.surname, a.qarz_w, a.qarz_s FROM workers w INNER JOIN about_worker a ON w.id = a.id')
    workers = cur.fetchall()
    if not workers:
        await message.reply("Qarz bar jumısshılar tabılmadı🙄")
        return

    keyboard = InlineKeyboardMarkup()
    for worker in workers:
        keyboard.add(InlineKeyboardButton(f"{worker[1]} {worker[2]} - {worker[3]}", callback_data=f"delete_about_{worker[3]}_{worker[0]}"))
    await message.reply("Qarz maǵlumatların óshiriw ushın jumısshı tanlań👇:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('delete_about_'))
async def process_delete_about_worker(callback_query: types.CallbackQuery):
    worker_id = int(callback_query.data.split('_')[-1])
    qarz_w = callback_query.data.split('_')[-2]
    await datas.delete_worker(id=worker_id,qarz_w=qarz_w)
    await bot.send_message(callback_query.from_user.id, "Qarz maǵlumatları óshirildi😁")



@dp.message_handler(text='Jumısshı halatın qosıw')
async def jumisshi_halatin_qosiw(message:types.Message):
    markup = admin_btn.workers_buttons()
    await message.answer('Jumısshı tanlań!',reply_markup=markup)

@dp.message_handler(text='Jumısshı halatın ógertiriw')
async def jumisshi_halatin_qosiw(message:types.Message):
    markup = admin_btn.update_worker_buttons()
    await message.answer('Jumısshı tanlań!',reply_markup=markup)



#<----------show worker--------------->

@dp.message_handler(text='Jumısshılardı kóriw')
async def show_workers(message: types.Message):
    # """Ishchilarni va ularning ma'lumotlarini ko'rsatish."""
    workers = datas.get_workers_info()
    if not workers:
        await message.reply("Maǵlumatlaw vazasınan hesh qanday jumısshı tabılmadı")
        return

    response = ""
    for worker in workers:
        response += (f"🆔 ID: {worker[0]}\n"
                     f"👤 Atı: {worker[1]}\n"
                     f"👥 Familiya: {worker[2]}\n"
                     f"📞 Telefon: {worker[3]}\n"
                     f"⚧ Jınsı: {worker[4]}\n"
                     f"💰 Qarz sánesi: {worker[5]}\n"
                     f"💳 Qarz summası: {worker[6]}\n"
                     f"🏢 Jumıstama: {worker[7]}\n"
                     f"🔧 Házir jumıstama: {worker[8]}\n"
                     f"{'-'*30}\n")

    await message.reply(response)



#<---------users function------------>


@dp.message_handler(commands=['about'])
async def send_about(msg: types.Message):
    await msg.answer(text='Bul M-house boti.')

@dp.message_handler(commands=['contacts'])
async def contacts(msg:types.Message):
    await msg.answer(text='''
📱 Baylanıs ushın telefonlar:
1️⃣ +998907273439
2️⃣ +998910973439
3️⃣ +998885073439

''')

@dp.message_handler(commands=['location'])
async def send_about(msg: types.Message):
    await bot.send_message(chat_id=msg.from_user.id,text='''
📍 Manzil: 
Oraylıq bazar, Zuxra sawda orayı arqa tarepinde, Chexov kóshesi, 30/5-uy.  

📌 Kartadan kóriw ushın:
👉 [Google Maps ashıw](https://maps.google.com/maps?q=42.461106,59.607093&ll=42.461106,59.607093&z=16)  
''',parse_mode='Markdown')


@dp.message_handler(commands=['start'])
async def send_hi(msg: types.Message):
    stop = False
    user_id = msg.from_user.id
    users = await datas.show_users()
    if user_id in admin_id:
        await msg.answer('Salem admin',reply_markup=admin_btn.admin_menu)
    else:
        for i in users:
            for j in i:
                if j == user_id:
                    stop = True
                    await msg.answer(text=f'''Assalamu aleykum {msg.from_user.first_name}
                                         
🗒 Bot haqqında maǵlıwmat alıw ushın:
👉 /about

👥 Bot adminleri menen baylanısıw ushın:
👉 /contacts

🏠 Jumıs ornımızdı biliw ushın:
👉 /location
''')
                    await msg.answer(
                            text=f'''Xizmetlerimizden paydalanıw ushın bólim saylań.👇''',
                            reply_markup=user_btn.main_menu)
            if stop:
                break
        if not stop:
            await msg.answer(
                    text=f'''Assalamu aleykum {msg.from_user.first_name}.
M-House Super kelinshekler hám er-jigitler telegram botına xosh kelipsiz!.
Siz botımızǵa birinshi márte kirgenińiz sebebli sizden dizimnen ótiwińizdi soranamız.
Onın ushın '📱Dizimnen o'tiw📱' túymesin basıń ''',
                    reply_markup=user_btn.reg_menu)


class Registration(StatesGroup):
    name = State()
    surname = State()
    phone_num = State()


@dp.message_handler(text="📱Dizimnen o'tiw📱")
async def cmd_start(message: types.Message):
    await message.answer("OOO jańa kilent!\nBizge atıńızdı jazıp jiberiń:",reply_markup=types.ReplyKeyboardRemove())
    await Registration.name.set()
@dp.message_handler(state=Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Axa, endi bizge familiyańız kerek:")
    await Registration.next()

@dp.message_handler(state=Registration.surname)
async def process_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer("Zor, endi bizge telefon nomerinizdi jazıp qaldırıń:")
    await Registration.next()


@dp.message_handler(state=Registration.phone_num)
async def process_phone_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_num'] = message.text

        user_data = {
            'name': data['name'],
            'surname': data['surname'],  
            'phone_num': data['phone_num'],
            
        }

        await message.answer(f"Siz dizimnen awmetli ottińiz.\nEndi arqayın xizmetlerimizden paydalana alasız)",reply_markup=user_btn.main_menu)
    await datas.add_user(id=message.from_user.id,
                         name=user_data['name'],
                         surname=user_data['surname'],
                         phone_num=user_data['phone_num'])

    await state.finish()

@dp.message_handler(text='🏠 Tiykarǵı menyu 🏠')
async def xizmetler(message:types.Message):
    user_id=message.from_user.id
    if user_id in admin_id:
        await bot.send_message(chat_id=user_id,text=message.text,reply_markup=admin_btn.admin_menu)
    elif user_id not in admin_id:
        await bot.send_message(chat_id=user_id,text=message.text,reply_markup=user_btn.main_menu)


@dp.message_handler(text='🗣 Xizmetler 🗣')
async def xizmetler(message:types.Message):
    await message.answer(text="Siz '🗣 Xizmetler 🗣' bólimin sayladıńız",
                         reply_markup=user_btn.xizmetler_menu)

@dp.message_handler(text='🗂 Vakansia 🗂')
async def xizmetler(message:types.Message):
    await message.answer(text="Siz '🗂 Jumıslar 🗂' bólimin sayladıńız",
                         reply_markup=user_btn.jumislar_menu)
    
    
@dp.message_handler(text='📱 telefon/adress 📍')
async def xizmetler(message:types.Message):
    await message.answer(text="""
📱 Baylanıs ushın telefonlar:
1️⃣ +998907273439
2️⃣ +998910973439
3️⃣ +998885073439

📍 Manzil: 
Oraylıq bazar, Zuxra sawda orayı arqa tarepinde, Chexov kóshesi, 30/5-uy.  

📌 Kartadan kóriw ushın:
👉 [Google Maps ashıw](https://maps.google.com/maps?q=42.461106,59.607093&ll=42.461106,59.607093&z=16) 
""",parse_mode='Markdown'
)

@dp.message_handler(text='🏣 Firmamis 🏣')
async def xizmetler(message:types.Message):
    await message.answer(text="""
Bizdiń kompaniyamız rasmiy atı M-house juwapkershiligi sheklengen jámiyeti bolıp, M-house logotipi astında 2019 jılı 20-fevral waqtınan baslap xizmet jùritip keledi.
Kompaniyamızdıń basshısı Abdikerimova Nargiza Jambırbaevna, "Nargizxanım" bolıp esaplanadı.
Kompaniyamız hayal qızlarımızdıñ xizmeti bolǵan úy xizmeti, qonaq kùtisiw, bala qaraw h.t.b. hàmde er-jigitlerimizdiñ xizmeti bolĝan atız awdarıw, svarka, molyarka, elektr xizmetleri h.t. baskada xizmetleri menen kòpden-kòp is beriwshilerimizdiń isenimin aqlap, kewlinen orın alıp kelmekte.
Xizmetlerden tısqarı jas hayal-qızlarımızĝa erteńgi turmısına kerek bolǵan bilimler, "Turmısqa tayarlaw" kursımız ashılǵan bolıp, kursımızda siz òzińizge kerek bolǵan tanıqlı taģamlar, pıshırıqlar hàmde tùrli salatlardı úyrenesiz. Kursımızdıń ishine turmıstaĝı kelispewshiliklerdiñ aldın alıwǵa bizdegi psixologiya sabaǵımızda kiredi.
Bul kursimızdi pitirip "Super kelinshek"  atalıp siz kursımız sertifikatına iye bolasız.
Bizdiń kompaniyamızdıń maqseti jámiyetimizge jaqınnan sıpatlı jàrdem kòrsetiw,xizmetińizdi jeńilletiw hàm waqtıńızdı tejew bolıp esaplanadı.
Bizge isenip bizdi saylaǵanıńızdan júdá quwanıshlımız. 
P.S Hùrmet penen Nargizxanım
""")

class RegistrationJumis(StatesGroup):
    work = State()
    name = State()
    surname = State()
    phone_num = State()

@dp.message_handler(text="👨🏻‍🍳 Aspaz 👩🏻‍🍳")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('''
Assalauma aliykim! 
Aspaz vakansiyası informaciyası :

📌 Jas aralıǵı 25 den 55ge shekem
📌 Jumıs waqtı 8 saat
📌 Bastagı 3 kun sınaw muddeti sebepli xizmet haqı tolenbeydi
📌 Qalǵan is kunleri 20% usluga sıpatında alınadı

Tajriybeli, dalaga milliy awqat hámde basqada tansıq taǵamlar asıp bilseńiz sizdi oz jamiyetimizde kutip qalamız.

P.S   Húrmet penen Nargizxanım!
''')
    async with state.proxy() as data:
        data['work'] = message.text
    await message.answer("Eger razı bolsańız bizge atıńızdı jazıp jiberiń:",reply_markup=user_btn.tiykargi_menu)
    await RegistrationJumis.name.set()

@dp.message_handler(text="🤵🏻 Qonaq kútiw 🤵🏻‍♀️")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('''
Assalauma aliykim! 
Qonaq kútiw vakansiyası informaciyası :

📌 Jas aralıǵı 25 den 45ge shekem
📌 Jumıs waqtı 8 saat
📌 Bastagı 3 kun sınaw muddeti sebepli xizmet haqı tolenbeydi
📌 Qalǵan is kunleri 20% usluga sıpatında alınadı
 
Tajriybeli, salatlar hámde baskada pıshırıqlar turlerinen pisiriwde xabarıńız bolsa oz jamiyetimizde kutip qalamız.

P.S   Húrmet penen Nargizxanım!
''')
    async with state.proxy() as data:
        data['work'] = message.text
    await message.answer("Eger razı bolsańız bizge atıńızdı jazıp jiberiń:",reply_markup=user_btn.tiykargi_menu)
    await RegistrationJumis.name.set()

@dp.message_handler(text="👶🏻 Bala qaraw 👧🏻")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('''
Assalauma aliykim! 
Bala qaraw vakansiyası informaciyası :

📌 Jas aralıǵı 25 den 55ge shekem
📌 Jumıs waqtı 8 saat
📌 Bastagı 3 kun sınaw muddeti sebepli xizmet haqı tolenbeydi
📌 Qalǵan is kunleri 20% usluga sıpatında alınadı

Bala qarawda tajriybeli, miyrimli, azada hámde balanı jaqsı kóretuǵın bolsańız sizdi oz jamiyetimizde kutip qalamız.

P.S   Húrmet penen Nargizxanım!
''')
    async with state.proxy() as data:
        data['work'] = message.text
    await message.answer("Eger razı bolsańız bizge atıńızdı jazıp jiberiń:",reply_markup=user_btn.tiykargi_menu)
    await RegistrationJumis.name.set()

@dp.message_handler(text="🧹 Uborka 🧹")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('''
Assalauma aliykim! 
Bala qaraw vakansiyası informaciyası :

📌 Jas aralıǵı 25 den 45ge shekem
📌 Jumıs waqtı 8 saat
📌 Bastagı 3 kun sınaw muddeti sebepli xizmet haqı tolenbeydi
📌 Qalǵan is kunleri 20% usluga sıpatında alınadı

Úy jiynaw, vlajnaya uborka hám generalnaya uborkadan xabarıńız bolsa sizdi oz jamiyetimizde kutip qalamız

P.S   Húrmet penen Nargizxanım!
''')
    async with state.proxy() as data:
        data['work'] = message.text
    await message.answer("Eger razı bolsańız bizge atıńızdı jazıp jiberiń:",reply_markup=user_btn.tiykargi_menu)
    await RegistrationJumis.name.set()

@dp.message_handler(state=RegistrationJumis.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=user_btn.main_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer("Axa, endi bizge familiyańız kerek:")
        await RegistrationJumis.next()

@dp.message_handler(state=RegistrationJumis.surname)
async def process_surname(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=user_btn.main_menu)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['surname'] = message.text
        await message.answer("Zor, endi bizge telefon nomerinizdi jazıp qaldırıń:")
        await RegistrationJumis.next()


@dp.message_handler(state=RegistrationJumis.phone_num)
async def process_phone_num(message: types.Message, state: FSMContext):
    if message.text=='🏠 Tiykarǵı menyu 🏠':
        await message.answer(text=message.text,reply_markup=user_btn.main_menu)
    else:  
        async with state.proxy() as data:
            data['phone_num'] = message.text
            for i in admin_id:
                await bot.send_message(
                    chat_id=i,
                    text=f'''
Taza jumısshı:

🗣 Jumıs túri: {data['work']}
👤 Atı: {data['name']}
👤 Familyası: {data['surname']}
📞 Telefoni: {data['phone_num']}
'''
                )
        await message.answer(f"Sizdiń sorawıńız qabıl qılındı✅\nAdminlerimiz siz benen baylanısadı)",reply_markup=user_btn.main_menu)
    await state.finish()


user_data = {}

@dp.message_handler(text='🤵🏻 Er jigitler 🤵🏻')
async def send_er_menu(message:types.Message):
    chat_id = message.from_user.id
    await message.answer(text='Bizde tomendegishe xizmetler bar👇:',
                         reply_markup=user_btn.erler_menu)
    result.append(message.text)
    user_data.pop(chat_id, None)


@dp.message_handler(text='🤵🏻‍♀️ Super kelinshekler 🤵🏻‍♀️')
async def send_er_menu(message:types.Message):
    chat_id = message.from_user.id
    await message.answer(text='Bizde tomendegishe xizmetler bar👇:',
                         reply_markup=user_btn.qizlar_menu)
    result.append(message.text)
    user_data.pop(chat_id, None)


#1 adam ushin jumis senasi
price_per_worker = {
    'dasturxan': 150000, 
    'uy': 150000,              
}

#1 den kop adam ushin jumis senasi
discounted_price = {
    'dasturxan': 115000,  
    'uy': 115000,              
}


# basqa jumislar ushin jumis senasi
fixed_price_others = {
    'pro_qonaq_k': 165000,
    'qonaq_k': 115000,
    'dana': 4500,
    'sebetshe': 30000,
    'idis': 200000,
    'dalaga': 200000,
    'Kfs qanatları':80000,
    'Kfs ayaqları':100000,
    'Kurniy rulet':110000,
    'Shokolad':60000,
    'Cirniy shariky':110000,
    'Bawirsaq':25000, 
    'Miyweli salat':'Adminge xabarlasıń',
    '3 turli xit salat':23000, 
    'Somsa':4500,
    'Belyashi':4500,
    'Dunganskiy somsa':10000,  
    'bala':115000,  
    'jumsaq':'Adminge xabarlasıń',
    'atiz': 150000,
    'svarka': 150000,
    'dala_tazalaw': 150000,
    'elektr': 150000,
    'uy_buyim': 150000,
    'burshatka': 150000,
    'bagban': 150000,
    'juklew': 150000
}



# jumis senasin esaplaw funksiasi
def calculate_total_cost(work_type, num_workers, dasturxan_j, tayarlaw, s_b_d_q, kfs_t, qonaq_k_t,room_count,kfs_kg,kurniy_kg,shokolad_kg,cirniy_kg,bawirsaq_kg,miyweli_salat_tarelki,salat_3_tarelki,somsa_dana,belyashi_dana,dungan_dana,dana,sebetshe):
    if work_type=='qonaq':
        if qonaq_k_t=='pro_qonaq_k':
            price=fixed_price_others['pro_qonaq_k']
            all_price=num_workers*price
            return all_price
        elif qonaq_k_t=='qonaq_k':
            price=fixed_price_others['qonaq_k']
            all_price=num_workers*price
            return all_price
    elif work_type=='dasturxan_j':
        all_all_price=0
        all_dasturxan_price='\n'
        for i in dasturxan_j:
            if i=='Kurniy rulet':#,'Shokolad','Cirniy shariky','Bawirsaq']:
                price=fixed_price_others[i]
                kg = int(kurniy_kg.split(' ')[0])
                all_price=price*kg
                all_all_price+=all_price
                all_dasturxan_price+=f'- {kg}kg {i} : {all_price}som\n'
            elif i=='Shokolad':
                price=fixed_price_others[i]
                kg = int(shokolad_kg.split(' ')[0])
                all_price=price*kg
                all_all_price+=all_price
                all_dasturxan_price+=f'- {kg}kg {i} : {all_price}som\n'
            elif i=='Cirniy shariky':
                price=fixed_price_others[i]
                kg = int(cirniy_kg.split(' ')[0])
                all_price=price*kg
                all_all_price+=all_price
                all_dasturxan_price+=f'- {kg}kg {i} : {all_price}som\n'
            elif i=='Bawirsaq':
                price=fixed_price_others[i]
                kg = int(bawirsaq_kg.split(' ')[0])
                all_price=price*kg
                all_all_price+=all_price
                all_dasturxan_price+=f'- {kg}kg {i} : {all_price}som\n'
            elif i=='Somsa, belyashi, dunganskiy somsa':
                if s_b_d_q=='Somsa':
                    price=fixed_price_others[s_b_d_q]
                    dana = int(somsa_dana.split(' ')[0])
                    all_price=price*dana
                    all_all_price+=all_price
                    all_dasturxan_price+=f'- {dana}dana {i} : {all_price}som\n'
                elif s_b_d_q=='Belyashi':
                    price=fixed_price_others[s_b_d_q]
                    dana = int(belyashi_dana.split(' ')[0])
                    all_price=price*dana
                    all_all_price+=all_price
                    all_dasturxan_price+=f'- {dana}dana {i} : {all_price}som\n'
                elif s_b_d_q=='Dunganskiy somsa':
                    price=fixed_price_others[s_b_d_q]
                    dana = int(dungan_dana.split(' ')[0])
                    all_price=price*dana
                    all_all_price+=all_price
                    all_dasturxan_price+=f'- {dana}dana {i} : {all_price}som\n'
            elif i=='Kfs':
                price=fixed_price_others[kfs_t]
                kg = int(kfs_kg.split(' ')[0])
                all_price=price*kg
                all_all_price+=all_price
                all_dasturxan_price+=f'- {kg}kg {i} : {all_price}som\n'
            elif i=='Miyweli salat':
                price=fixed_price_others[i]
                tarelki = int(miyweli_salat_tarelki.split(' ')[0])
                all_dasturxan_price+=f'- {tarelki}tarelki {i} : {price}\n'
            elif i=='3 turli xit salat':
                price=fixed_price_others[i]
                tarelki = int(salat_3_tarelki.split(' ')[0])
                all_price=price*tarelki
                all_all_price+=all_price
                all_dasturxan_price+=f'- {tarelki}tarelki {i} : {all_price}som\n'
        
        all_all_price+=num_workers*100000
        return f'{all_dasturxan_price}\n💰 Jámi : {all_all_price}'
    
    elif work_type in ['dasturxan','uy']:
        base_price = price_per_worker[work_type]
        if num_workers == 1:
            return base_price
        else:
            additional_price = num_workers * discounted_price[work_type]
            return additional_price
    elif work_type in ['dalaga','bala']:
        price=fixed_price_others[work_type]
        all_price=price*num_workers
        return all_price
    elif work_type in ['mebel_j','gilem_j','banka_b']:
        price=fixed_price_others['jumsaq']
        return price
    elif work_type=='somsa':
        price=fixed_price_others['dana']
        dana = int(dana.split(' ')[0])
        all_price=dana*price+num_workers*100000
        return f'{price}x{dana}+{num_workers}x100000={all_price} som'
    elif work_type=='qiz_uzatiw':
        price=fixed_price_others['sebetshe']
        sebetshe = int(sebetshe.split(' ')[0])
        all_price=sebetshe*price
        return all_price
    elif work_type=='idis':
        price=fixed_price_others['idis']
        return price
    else:
        price=fixed_price_others[work_type]
        all_price=num_workers*price
        return all_price


text_work=''



def work_text(data,chat_id):
    translation = {
        'work': '🗣 Jumıs turi',
        'dasturxan_j': '📌 Dasturxanǵa qoyılatuǵın zat',
        'tayarlaw': '📌 Tayyarlaw',
        'qonaq_k': '📌 Qonaq kutiwshi',
        'kfs_t':'📌 Kfs turi',
        'idis_arenda': '📌 Ídıs arendası',
        'mebel_j': '📌 Mebel juwıw',
        'sebetshe': '📌 Sebetshe sanı',
        'bolme': '📌 Bólme sanı',
        'tarelki': '📌 Tarelka sanı',
        'dana': '📌 Danası',
        'worker_count': '👥 Jumısshılar sanı',
        'work_price': '💰 Senaları',
        'jumis_w': '⌛️ Jumıs waqtı',
        'lokatsia': '📍 Lokatsiya'
    }
    # def format_dasturxan_j(dasturxan_j):
    #     if isinstance(dasturxan_j, list) and dasturxan_j:  
    #         return "\n".join([f"- {item}" for item in dasturxan_j])
    #     return str(dasturxan_j) if dasturxan_j else "" 
    # def format_tayarlaw(tayarlaw):
    #     if isinstance(tayarlaw, list) and tayarlaw: 
    #         return "\n".join([f"- {item}" for item in tayarlaw])
    #     return str(tayarlaw) if tayarlaw else "" 

    # return "\n".join(
    #     "\n".join(
    #         [
    #             f"{translation.get(key, key)} : {format_dasturxan_j(value) if key == 'dasturxan_j' else format_tayarlaw(value) if key == 'tayarlaw' else value}"
    #             for key, value in data_point.items()
    #             if value is not None and key not in ('work_type', 'qonaq_k_t', 'kfs_kg', 'kurniy_kg', 'shokolad_kg', 'cirniy_kg', 'bawirsaq_kg',
    #                                                 'miyweli_salat_tarelki', '3_salat_tarelki', 'somsa_dana', 'belyashi_dana', 'dungan_dana')
    #         ]
    #     )
    #     for chat_id, data_point in data.items()
    # )
    def format_list(value):
        if isinstance(value, list) and value:  
            return "\n".join([f"- {item}" for item in value])
        return str(value) if value else ""

    # Foydalanuvchi ID bo'yicha ma'lumotlarni olish
    user_data = data.get(chat_id, None)
    if not user_data:
        return "Xesh qanday maǵlumat tawılmadı."

    # Foydalanuvchi ma'lumotlarini formatlash
    return "\n".join(
        [
            f"{translation.get(key, key)} : {format_list(value) if key in ('dasturxan_j', 'tayarlaw') else value}"
            for key, value in user_data.items()
            if value is not None and 
            (key not in ('dasturxan_j', 'tayarlaw') or (isinstance(value, list) and value)) and
            key not in ('work_type', 'qonaq_k_t', 'kfs_kg', 'kurniy_kg', 'shokolad_kg', 'cirniy_kg', 'bawirsaq_kg',
                        'miyweli_salat_tarelki', '3_salat_tarelki', 'somsa_dana', 'belyashi_dana', 'dungan_dana')
        ]
    )



@dp.message_handler(regexp=r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}")
async def handle_date_input(message: types.Message):
    chat_id = message.from_user.id
    date_input = message.text.strip()
    
    work_type = user_data[chat_id]['work_type']
    num_workers = user_data[chat_id]['worker_count']
    dasturxan_j = user_data[chat_id]['dasturxan_j']
    tayarlaw = user_data[chat_id]['tayarlaw']
    s_b_d_q = user_data[chat_id]['tayarlaw']
    kfs_t = user_data[chat_id]['kfs_t']
    qonaq_k_t = user_data[chat_id]['qonaq_k_t']
    room_count = user_data[chat_id]['bolme']
    kfs_kg = user_data[chat_id]['kfs_kg']
    kurniy_kg = user_data[chat_id]['kurniy_kg']
    shokolad_kg = user_data[chat_id]['shokolad_kg']
    cirniy_kg = user_data[chat_id]['cirniy_kg']
    bawirsaq_kg = user_data[chat_id]['bawirsaq_kg']
    miyweli_salat_tarelki = user_data[chat_id]['miyweli_salat_tarelki']
    salat_3_tarelki = user_data[chat_id]['3_salat_tarelki']
    somsa_dana = user_data[chat_id]['somsa_dana']
    belyashi_dana = user_data[chat_id]['belyashi_dana']
    dungan_dana = user_data[chat_id]['dungan_dana']
    dana = user_data[chat_id]['dana']
    sebetshe = user_data[chat_id]['sebetshe']
    
    total_cost = calculate_total_cost(
        work_type, num_workers, dasturxan_j,tayarlaw,
        s_b_d_q, kfs_t, qonaq_k_t,room_count,
        kfs_kg,kurniy_kg,shokolad_kg,cirniy_kg,bawirsaq_kg,
        miyweli_salat_tarelki,salat_3_tarelki,
        somsa_dana,belyashi_dana,dungan_dana,
        dana,sebetshe)
    
    user_data[chat_id]['work_price'] = total_cost
    user_data[chat_id]['jumis_w'] = date_input
    
    await bot.send_message(
            chat_id=chat_id,
            text="Raxmet! Endi jumıs bolatuǵın jerdiń lokatsiyasın jiberiń."
        )


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def lokatsia(message: types.Message):
    chat_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    # user_data[chat_id]['lokatsia'] = google_maps_url
    
    result = work_text(data=user_data,chat_id=chat_id)
    
    await bot.send_message(
            chat_id=chat_id,
            text=f"""Buyırtpańız qabıl qılındı✅
            
{result}

ESLETPE!!!
💰 Tólemi aldınnan 100% hám jol haqıda bar.
⌛️ Jumıs waqtı 8 saat. Eger jumıs waqtı belgilengen waqttan asıp ketse 1 saatı har jumısshı ushın 15 000 som.
"""
        )
    
    reg_m = ''
    reg = await datas.show_users()
    for i in reg:
        if message.from_user.id==i[0]:
            reg_m+=f'👤 Ati: {i[1]}\n👤 Familiası: {i[2]}\n📱 Telefon nawmeri: {i[4]}'
            
    for i in admin_id:
        await bot.send_message(
            chat_id=i,
            text=f'''
Taza buyırtpa qabıl qılındı✅

{result}

Paydalanıwshı:
{reg_m}

Lokatsia:
{google_maps_url}
'''
        )
    user_data.pop(chat_id, None)

worker_about={}
update_about={}
# Callback handler
@dp.callback_query_handler()
async def send_work_menu(call: types.CallbackQuery):
    data = call.data
    chat_id = call.from_user.id

    if chat_id not in user_data:
        user_data[chat_id] = {'work_type':None,'work':None,'dasturxan_j':[],'tayarlaw':[],
                              'kfs_t':None,'qonaq_k_t':None,'qonaq_k':None,'idis_arenda':None,
                              'mebel_j':None,'sebetshe':None,'bolme':None,'dana':None,
                              'kfs_kg':None,'kurniy_kg':None,'shokolad_kg':None,'cirniy_kg':None,
                              'bawirsaq_kg':None,'miyweli_salat_tarelki':None,'3_salat_tarelki':None,
                              'somsa_dana':None,'belyashi_dana':None,'dungan_dana':None,
                              'work_price':None,'worker_count':None,'jumis_w':None,'lokatsia':None}

    
    # jumis turleri
    work_list = {
        'dasturxan': 'Dasturxanlardi bezew',
        'dasturxan_j': 'Dasturxan jayıp beriw(ozlerimizden)',
        'uy': 'Uydi tazalaw',
        'qonaq': "Qonaq ku'tiw",
        'dalaga': "Dalaga awqat asiw",
        'somsa': "Somsa, belyashi, blinchik tayarlaw",
        'mebel_j': "Jumsaq mebel juwiw",
        'idis': "Idis ayaq arendasi",
        'qiz_uzatiw': 'Qiz uzatiw seti',
        'banka_b': 'Banka basiw',
        'gilem_j': 'Gilem juwiw',
        'bala':'Bala qaraw',
        'atiz': 'Atiz awdariw',
        'svarka': 'Svarka, malyarka',
        'dala_tazalaw': 'Dala tazalaw',
        'elektr': 'Elektr xizmetleri',
        'uy_buyim': "Uy buyimlarin tuzetiw",
        'burshatka': 'Burshatka juwiw',
        'bagban': "Bag'ban xizmeti",
        'juklew': "Juklew ham tiyew"
    }
    all_button={'kfs':'Kfs','kuriniy':'Kurniy rulet',
                'shokolad':'Shokolad','cirniy':'Cirniy shariky',
                'bawirsaq':'Bawirsaq','miyweli_salat':'Miyweli salat',
                '3_salat':'3 turli xit salat','somsa_belyashi_dunganskiy':'Somsa, belyashi, dunganskiy somsa',
                'somsa_t':'Somsa tayarlaw','belyashi_t':'Belyashi tayarlaw','blinchik_t':'Blinchik tayarlaw',
                'somsa_q':'Somsa','belyashi_q':'Belyashi','dunganskiy_q':'Dunganskiy somsa',
                'pro_qonaq_k':'Profisianal qonaq kutiwshi','qonaq_k':'Qonaq kutiwshi(ápiwayi)',
                'kfs_80':'Kfs qanatları','kfs_100':'Kfs ayaqları',
                '12_adam':'12 adamlıq',
                '1_divan':'1 divan juwıw','2_stol':'2 stol juwıw'}
    
    # Xona sonlari ro'yxati
    all_num = { '1s':'1 sebetshe', '2s':'2 sebetshe', '3s':'3 sebetshe', '4s':'4 sebetshe', '5s':'5 sebetshe', '6s':'6 sebetshe',
                '1b':'1 bólme', '2b':'2 bólme', '3b':'3 bólme', '4b':'4 bólme', '5b':'5 bólme', '6b':'6 bólme', '7b':'7 bólme', '8b':'8 bólme',
                '1kg': '1 kg', '2kg': '2 kg', '3kg': '3 kg', '4kg': '4 kg', '5kg': '5 kg', '6kg': '6 kg', '7kg': '7 kg', '8kg': '8 kg', '9kg': '9 kg', '10kg': '10 kg',
                '11kg': '11 kg', '12kg': '12 kg', '13kg': '13 kg', '14kg': '14 kg', '15kg': '15 kg', '16kg': '16 kg', '17kg': '17 kg', '18kg': '18 kg', '19kg': '19 kg', '20kg': '20 kg',
                '2t': '2 tarelki', '3t': '3 tarelki', '4t': '4 tarelki', '5t': '5 tarelki',
                '6t': '6 tarelki', '7t': '7 tarelki', '8t': '8 tarelki', '9t': '9 tarelki',
                '10t': '10 tarelki', '11t': '11 tarelki', '12t': '12 tarelki', '13t': '13 tarelki',
                '14t': '14 tarelki', '15t': '15 tarelki', '16t': '16 tarelki', '17t': '17 tarelki',
                '18t': '18 tarelki', '19t': '19 tarelki', '20t': '20 tarelki', '21t': '21 tarelki',
                '10d':'10 dana','20d':'20 dana','30d':'30 dana','40d':'40 dana','50d':'50 dana','60d':'60 dana',
                '10sht':'10 dana','20sht':'20 dana','30sht':'30 dana','40sht':'40 dana','50sht':'50 dana','60sht':'60 dana'}
    # Ishchi sonlari ro'yxati
    worker_counts = ['1', '2', '3', '4', '5', '6']
    # Qalalar ro'yxati
    # qalalar = ['nukus', 'xojeli', 'shimbay', 'qonirat', 'taqiyatas', 'qaraozek', 'kegeyli', 'tortkul']
    
    # Ish turi tanlanganda
    if data in work_list:
        user_data[chat_id]['work_type'] = data
        user_data[chat_id]['work'] = work_list[data]
        if data=='uy':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nEndi xana sanın tańlań👇:",
                reply_markup=user_btn.bolme_sani_menu)
        elif data=='dasturxan_j':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nEndi dasturxanǵa ne zatlar qoymaqshısız👇:",
                reply_markup=user_btn.dasturxan
            )
        elif data=='somsa':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nEndi tómendegilerden qay birin tayarlaw kerek👇:",
                reply_markup=user_btn.somsa_beleshey_blinchik
            )
        elif data=='qonaq':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nEndi qonaq kútiwshini tanlań👇:",
                reply_markup=user_btn.qonaq
            )
        elif data=='qiz_uzatiw':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nEndi neshe sebet kerekligin tanlań👇:",
                reply_markup=user_btn.sebet_sani_menu   #sebet
            )
        elif data=='idis':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nBizde tómendegishe pasudalar bar👇:",
                reply_markup=user_btn.idis_ayaq
            )
        elif data=='mebel_j':
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nBizde tómendegishe mebel juwıw xizmetleri bar👇:",
                reply_markup=user_btn.mebel_j
            )
        elif data in ['gilem_j','banka_b']:
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmetin tanladıńız.\nAdmin menen baylanısıń! /contacts"
            )
        else:
            # Boshqa ish turlari uchun ishchi sonini so'rash
            await bot.send_message(
                chat_id=chat_id,
                text=f"Siz '{work_list[data]}' xizmatin tanladıńız.\nNeshe jumısshı kerakligin tanlań👇:",
                reply_markup=user_btn.adam_sani_menu)
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            

    # Xona soni tanlanganda
    elif data in all_button:
        if data in ['kuriniy','shokolad','cirniy','bawirsaq','somsa_belyashi']:
            user_data[chat_id]['dasturxan_j'].append(all_button[data])
            await bot.send_message(
                chat_id=chat_id,
                text="Neshe kilogram kerakligin tanlań👇:",
                reply_markup=user_btn.kglar)
        if data == 'kfs':
            user_data[chat_id]['dasturxan_j'].append(all_button[data])
            await bot.send_message(
                chat_id=chat_id,
                text="Endi kfs túrin tanlań👇:",
                reply_markup=user_btn.kfs_turi)
        elif data in ['miyweli_salat','3_salat']:
            user_data[chat_id]['dasturxan_j'].append(all_button[data])
            await bot.send_message(
                chat_id=chat_id,
                text="Neshe tarelka kerakligin tanlań👇:",
                reply_markup=user_btn.plate_keyboard)
        elif data in ['somsa_belyashi_dunganskiy']:
            user_data[chat_id]['dasturxan_j'].append(all_button[data])
            await bot.send_message(
                chat_id=chat_id,
                text="Endi tómendegilerden birin tanlań👇:",
                reply_markup=user_btn.somsa_beleshey_dunganskiy)
        elif data in ['somsa_q','belyashi_q','dunganskiy_q']:
            user_data[chat_id]['tayarlaw'].append(all_button[data])
            await bot.send_message(
                chat_id=chat_id,
                text=f"Neshe {all_button[data]} kerekligin tanlań👇:",
                reply_markup=user_btn.tayarlaw_d_sani
            )
        elif data in ['somsa_t','belyashi_t','blinchik_t']:
            user_data[chat_id]['tayarlaw']=all_button[data]
            await bot.send_message(
                chat_id=chat_id,
                text=f"Neshe {all_button[data]} kerekligin tanlań👇:",
                reply_markup=user_btn.tayarlaw_sani
            )
        elif data in ['kfs_80','kfs_100']:
            user_data[chat_id]['kfs_t']=all_button[data]
            await bot.send_message(
                chat_id=chat_id,
                text=f'Neshe kilogram kerakligin tanlań👇:',
                reply_markup=user_btn.kglar
            )
        elif data in ['pro_qonaq_k','qonaq_k']:
            user_data[chat_id]['qonaq_k']=all_button[data]
            user_data[chat_id]['qonaq_k_t']=data
            await bot.send_message(
                chat_id=chat_id,
                text=f'Neshe {all_button[data]} kerekligin tanlań👇:',
                reply_markup=user_btn.adam_sani_menu
            )
        elif data=='12_adam':
            user_data[chat_id]['idis_arenda']=all_button[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Endi jumıs waqtın kiritiń!\nMaselen:(01.01.2024 06:00)',
                # reply_markup=
            )
        elif data in ['1_divan','2_stol']:
            user_data[chat_id]['mebel_j']=all_button[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Endi jumıs waqtın kiritiń!\nMaselen:(01.01.2024 06:00)',
                # reply_markup=
            )
        
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        
    elif data in all_num:
        if data in ['1s','2s','3s','4s','5s','6s']:
            user_data[chat_id]['sebetshe']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Endi jumıs waqtın kiritiń!\nMaselen:(01.01.2024 06:00)'
            )
        elif data in ['1b','2b','3b','4b','5b','6b','7b','8b']:
            user_data[chat_id]['bolme']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Endi jumısshi sanın tanlań👇',
                reply_markup=user_btn.adam_sani_menu
            )
        elif data in ['1kg', '2kg', '3kg', '4kg', '5kg', '6kg', '7kg', '8kg', '9kg', '10kg', '11kg', '12kg', '13kg', '14kg', '15kg', '16kg', '17kg', '18kg', '19kg', '20kg']:
            if user_data[chat_id]['dasturxan_j'][-1]=='Kfs':
                user_data[chat_id]['kfs_kg']=all_num[data]
            elif user_data[chat_id]['dasturxan_j'][-1]=='Kurniy rulet':
                user_data[chat_id]['kurniy_kg']=all_num[data]
            elif user_data[chat_id]['dasturxan_j'][-1]=='Shokolad':
                user_data[chat_id]['shokolad_kg']=all_num[data]
            elif user_data[chat_id]['dasturxan_j'][-1]=='Cirniy shariky':
                user_data[chat_id]['cirniy_kg']=all_num[data]
            elif user_data[chat_id]['dasturxan_j'][-1]=='Bawirsaq':
                user_data[chat_id]['bawirsaq_kg']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Jáne dasturxanǵa ne qoymaqshısız👇',
                reply_markup=user_btn.dasturxan_t
            )
        elif data in ['2t', '3t', '4t', '5t', '6t', '7t', '8t', '9t', '10t', '11t', '12t', '13t', '14t', '15t', '16t', '17t', '18t', '19t', '20t', '21t']:
            if user_data[chat_id]['dasturxan_j'][-1]=='Miyweli salat':
                user_data[chat_id]['miyweli_salat_tarelki']=all_num[data]
            elif user_data[chat_id]['dasturxan_j'][-1]=='3 turli xit salat':
                user_data[chat_id]['3_salat_tarelki']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Jáne dasturxanǵa ne qoymaqshısız👇',
                reply_markup=user_btn.dasturxan_t
            )
        elif data in ['10d','20d','30d','40d','50d','60d']:
            if user_data[chat_id]['tayarlaw'][-1]=='Somsa':
                user_data[chat_id]['somsa_dana']=all_num[data]
            elif user_data[chat_id]['tayarlaw'][-1]=='Belyashi':
                user_data[chat_id]['belyashi_dana']=all_num[data]
            elif user_data[chat_id]['tayarlaw'][-1]=='Dunganskiy somsa':
                user_data[chat_id]['dungan_dana']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Jáne dasturxanǵa ne qoymaqshısız',
                reply_markup=user_btn.dasturxan_t
            )
            
        elif data in ['10sht','20sht','30sht','40sht','50sht','60sht']:
            user_data[chat_id]['dana']=all_num[data]
            await bot.send_message(
                chat_id=chat_id,
                text='Endi jumısshi sanın tanlań👇',
                reply_markup=user_btn.adam_sani_menu
            )
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            
    # Ishchi soni tanlanganda
    elif data in worker_counts:
        user_data[chat_id]['worker_count'] = int(data)
        await bot.send_message(
            chat_id=chat_id,
            text=f"Axa, endi jumıs waqtın kiritiń!\nMaselen:(01.01.2024 06:00)",
        )
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)

    elif data=='otkeriw':
        await bot.send_message(
                chat_id=chat_id,
                text='Endi jumısshi sanın tanlań👇',
                reply_markup=user_btn.adam_sani_menu
            )

    
    if chat_id not in worker_about:
        worker_about[chat_id] = {}
        update_about[chat_id] = {}
    
    if data.startswith('worker_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        worker_id = int(call.data.split('_')[-1])  # Ishchi ID ni olish
        worker_about[chat_id]['worker_id']=worker_id  
        await call.message.answer(f"Jumısshı jumistama:", reply_markup=admin_btn.status1_buttons())
        await call.answer()
        
    elif data.startswith('status1_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        is_at_work = call.data.split('_')[1]
        worker_about[chat_id]['is_at_work']=is_at_work
        await call.message.answer("Jumısshı hazir jumıstama:", reply_markup=admin_btn.status2_buttons())
        await call.answer()

    elif data.startswith('status2_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        is_working_now = call.data.split('_')[1] 
        worker_id=worker_about[chat_id]['worker_id']
        is_at_work=worker_about[chat_id]['is_at_work']
        await datas.add_at_about_worker(id=worker_id, is_at_work=is_at_work, is_working_now=is_working_now)
        await call.message.answer("Jumsshınıń is halatı belgilendi.")
        worker_about.clear()
        await call.answer()
        
        
    if data.startswith('_update_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        worker_id = int(call.data.split('_')[-1])  # Ishchi ID ni olish
        update_about[chat_id]['worker_id']=worker_id
        await call.message.answer(f"Jumısshı jumistama:", reply_markup=admin_btn.update_status1_buttons())
        await call.answer()
        
    elif data.startswith('update_status1_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        is_at_work = call.data.split('_')[-1]
        update_about[chat_id]['is_at_work']=is_at_work
        await call.message.answer("Jumısshı hazir jumıstama:", reply_markup=admin_btn.update_status2_buttons())
        await call.answer()

    elif data.startswith('update_status2_'):
        await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        is_working_now = call.data.split('_')[-1] 
        worker_id=update_about[chat_id]['worker_id']
        is_at_work=update_about[chat_id]['is_at_work']
        await datas.update_worker_about(worker_id, is_at_work, is_working_now)
        await call.message.answer("Jumsshınıń is halatı ózgertildi.")
        worker_about.clear()
        await call.answer()
      
      
      


       
            



if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)

