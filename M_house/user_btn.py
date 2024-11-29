from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


reg_menu = ReplyKeyboardMarkup(resize_keyboard=True)
reg_menu.add(KeyboardButton(text="📱Dizimnen o'tiw📱"))

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton(text='🗣 Xizmetler 🗣'),KeyboardButton(text='🗂 Vakansia 🗂'))
main_menu.add(KeyboardButton(text='📱 telefon/adress 📍'),KeyboardButton(text='🏣 Firmamis 🏣'))

tiykargi_menu = ReplyKeyboardMarkup(resize_keyboard=True)
tiykargi_menu.add(
              KeyboardButton(text='🏠 Tiykarǵı menyu 🏠'))


xizmetler_menu = ReplyKeyboardMarkup(resize_keyboard=True)
xizmetler_menu.add(KeyboardButton(text='🤵🏻 Er jigitler 🤵🏻'),
              KeyboardButton(text='🤵🏻‍♀️ Super kelinshekler 🤵🏻‍♀️'))
xizmetler_menu.add(
              KeyboardButton(text='🏠 Tiykarǵı menyu 🏠'))


jumislar_menu = ReplyKeyboardMarkup(resize_keyboard=True)

jumislar_menu.add(KeyboardButton(text='👨🏻‍🍳 Aspaz 👩🏻‍🍳'),KeyboardButton(text='👶🏻 Bala qaraw 👧🏻'))
jumislar_menu.add(KeyboardButton(text='🤵🏻 Qonaq kútiw 🤵🏻‍♀️'),KeyboardButton(text='🧹 Uborka 🧹'))
jumislar_menu.add(KeyboardButton(text='🏠 Tiykarǵı menyu 🏠'))

qizlar_menu = InlineKeyboardMarkup()

qizlar_menu.add(
    InlineKeyboardButton(text="Somsa, belyashi, blinchik tayarlaw",callback_data='somsa'),
)

qizlar_menu.add(
    InlineKeyboardButton(text='Dasturxan jayıp beriw(ozlerimizden)',callback_data='dasturxan_j')
)

qizlar_menu.add(
    InlineKeyboardButton(text='Dasturxanlardi bezew',callback_data='dasturxan'),
    InlineKeyboardButton(text='Uydi tazalaw',callback_data='uy'),
)
qizlar_menu.add(
    InlineKeyboardButton(text="Qonaq ku'tiw",callback_data='qonaq'),
    InlineKeyboardButton(text="Dalag'a awqat asiw",callback_data='dalaga'),

)
qizlar_menu.add(
    InlineKeyboardButton(text='Bala qaraw',callback_data='bala'),
    InlineKeyboardButton(text="Jumsaq mebel juwiw",callback_data='mebel_j'),

)
qizlar_menu.add(
    InlineKeyboardButton(text="Idis ayaq arendasi",callback_data='idis'),
    InlineKeyboardButton(text='Qiz uzatiw seti',callback_data='qiz_uzatiw')
)
qizlar_menu.add(
    InlineKeyboardButton(text='Banka basiw',callback_data='banka_b'),
    InlineKeyboardButton(text='Gilem juwiw',callback_data='gilem_j')
    
)


erler_menu = InlineKeyboardMarkup()

erler_menu.add(
    InlineKeyboardButton(text='Atiz awdariw',callback_data='atiz'),
    InlineKeyboardButton(text='Svarka,malyarka',callback_data='svarka'),
)

erler_menu.add(
    InlineKeyboardButton(text='Dala tazalaw',callback_data='dala_tazalaw'),
    InlineKeyboardButton(text='Elektr xizmetleri',callback_data='elektr'),
)

erler_menu.add(
    InlineKeyboardButton(text="U'y buyimlarin tuzetiw",callback_data='uy_buyim'),
    InlineKeyboardButton(text='Burshatka juwiw',callback_data='burshatka'),
)

erler_menu.add(
    InlineKeyboardButton(text="Bag'ban xizmeti",callback_data='bagban'),
    InlineKeyboardButton(text="Ju'klew ham tiyew",callback_data='juklew'),
)

dasturxan = InlineKeyboardMarkup()

dasturxan.add(
    InlineKeyboardButton(text='Kfs',callback_data='kfs'),
    InlineKeyboardButton(text='Kuriniy rulet',callback_data='kuriniy'),
)
dasturxan.add(    
    InlineKeyboardButton(text='Shokolad',callback_data='shokolad'),
    InlineKeyboardButton(text='Cirniy shariky',callback_data='cirniy'),
)
dasturxan.add(
    InlineKeyboardButton(text='Bawırsaq',callback_data='bawirsaq'),
    InlineKeyboardButton(text='Miyweli salat',callback_data='miyweli_salat'),
)
dasturxan.add(   
    InlineKeyboardButton(text='3 turli xit salat',callback_data='3_salat'),
    InlineKeyboardButton(text='Somsa, belyashi, dunganskiy somsa',callback_data='somsa_belyashi_dunganskiy')
)

dasturxan_t = InlineKeyboardMarkup()

dasturxan_t.add(
    InlineKeyboardButton(text='Kfs',callback_data='kfs'),
    InlineKeyboardButton(text='Kuriniy rulet',callback_data='kuriniy'),
)
dasturxan_t.add(    
    InlineKeyboardButton(text='Shokolad',callback_data='shokolad'),
    InlineKeyboardButton(text='Cirniy shariky',callback_data='cirniy'),
)
dasturxan_t.add(
    InlineKeyboardButton(text='Bawırsaq',callback_data='bawirsaq'),
    InlineKeyboardButton(text='Miyweli salat',callback_data='miyweli_salat'),
)
dasturxan_t.add(   
    InlineKeyboardButton(text='3 turli xit salat',callback_data='3_salat'),
    InlineKeyboardButton(text='Somsa, belyashi, dunganskiy somsa',callback_data='somsa_belyashi_dunganskiy')
)
dasturxan_t.add(
    InlineKeyboardButton(text='Ótkeriw ➡️',callback_data='otkeriw')
)

kfs_turi = InlineKeyboardMarkup()

kfs_turi.add(
    InlineKeyboardButton(text='Kfs qanatları',callback_data='kfs_80'),
    InlineKeyboardButton(text='Kfs ayaqları',callback_data='kfs_100')
)

somsa_beleshey_blinchik = InlineKeyboardMarkup()

somsa_beleshey_blinchik.add(
    InlineKeyboardButton(text='Somsa',callback_data='somsa_t'),
    InlineKeyboardButton(text='Belyashi',callback_data='belyashi_t'),
    InlineKeyboardButton(text='Blinchik',callback_data='blinchik_t')
)

somsa_beleshey_dunganskiy = InlineKeyboardMarkup()

somsa_beleshey_dunganskiy.add(
    InlineKeyboardButton(text='Somsa',callback_data='somsa_q'),
    InlineKeyboardButton(text='Belyashi',callback_data='belyashi_q'),
    InlineKeyboardButton(text='Dunganskiy Somsa',callback_data='dunganskiy_q')
)


qonaq = InlineKeyboardMarkup()
qonaq.add(
    InlineKeyboardButton(text='Profissinal qonaq kútiwshi',callback_data='pro_qonaq_k'),
    InlineKeyboardButton(text='Qonaq kútiwshi(ápiwayi)',callback_data='qonaq_k')
)

idis_ayaq = InlineKeyboardMarkup()

idis_ayaq.add(
    InlineKeyboardButton(text='12 adamliq komlpekt',callback_data='12_adam'),
)

mebel_j = InlineKeyboardMarkup()

mebel_j.add(
    InlineKeyboardButton(text='1 divan juwıw',callback_data='1_divan'),
    InlineKeyboardButton(text='2 stolchik juwıw',callback_data='2_stol')
)

kglar = InlineKeyboardMarkup()

kglar = InlineKeyboardMarkup(row_width=5).add(
    *[InlineKeyboardButton(text=str(i), callback_data=f"{i}kg") for i in range(1, 21)]
)


tarelka_sani = InlineKeyboardMarkup()

tarelka_sani.add(
    InlineKeyboardButton(text='5',callback_data='5t'),
    InlineKeyboardButton(text='10',callback_data='10t'),
    InlineKeyboardButton(text='15',callback_data='15t')
)

tarelka_sani.add(
    InlineKeyboardButton(text='20',callback_data='20t'),
    InlineKeyboardButton(text='25',callback_data='25t')
)



plate_keyboard = InlineKeyboardMarkup(row_width=5).add(
    *[InlineKeyboardButton(text=str(i), callback_data=f"{i}t") for i in range(2, 22)]
)


tayarlaw_d_sani = InlineKeyboardMarkup()

tayarlaw_d_sani.add(
    InlineKeyboardButton(text='10',callback_data='10d'),
    InlineKeyboardButton(text='20',callback_data='20d'),
    InlineKeyboardButton(text='30',callback_data='30d')
)

tayarlaw_d_sani.add(
    InlineKeyboardButton(text='40',callback_data='40d'),
    InlineKeyboardButton(text='50',callback_data='50d'),
    InlineKeyboardButton(text='60',callback_data='60d')
)

tayarlaw_sani = InlineKeyboardMarkup()

tayarlaw_sani.add(
    InlineKeyboardButton(text='10',callback_data='10sht'),
    InlineKeyboardButton(text='20',callback_data='20sht'),
    InlineKeyboardButton(text='30',callback_data='30sht')
)

tayarlaw_sani.add(
    InlineKeyboardButton(text='40',callback_data='40sht'),
    InlineKeyboardButton(text='50',callback_data='50sht'),
    InlineKeyboardButton(text='60',callback_data='60sht')
)


bolme_sani_menu = InlineKeyboardMarkup()

bolme_sani_menu.add(
                   InlineKeyboardButton(text='1',callback_data='1b'),
                   InlineKeyboardButton(text='2',callback_data='2b'),
                   InlineKeyboardButton(text='3',callback_data='3b'),
                   InlineKeyboardButton(text='4',callback_data='4b'),
)
bolme_sani_menu.add(
                   InlineKeyboardButton(text='5',callback_data='5b'),
                   InlineKeyboardButton(text='6',callback_data='6b'),
                   InlineKeyboardButton(text='7',callback_data='7b'),
                   InlineKeyboardButton(text='8',callback_data='8b'),              
)

sebet_sani_menu = InlineKeyboardMarkup()

sebet_sani_menu.add(InlineKeyboardButton(text='1',callback_data='1s'),
                   InlineKeyboardButton(text='2',callback_data='2s'),
                   InlineKeyboardButton(text='3',callback_data='3s'),
)
sebet_sani_menu.add(
                   InlineKeyboardButton(text='4',callback_data='4s'),
                   InlineKeyboardButton(text='5',callback_data='5s'),
                   InlineKeyboardButton(text='6',callback_data='6s')
)


adam_sani_menu = InlineKeyboardMarkup()

adam_sani_menu.add(InlineKeyboardButton(text='1',callback_data=1),
                   InlineKeyboardButton(text='2',callback_data=2),
                   InlineKeyboardButton(text='3',callback_data=3),
)
adam_sani_menu.add(
                   InlineKeyboardButton(text='4',callback_data=4),
                   InlineKeyboardButton(text='5',callback_data=5),
                   InlineKeyboardButton(text='6',callback_data=6)
)


qalalar = InlineKeyboardMarkup()

qalalar.add(InlineKeyboardButton(text='Nukus',callback_data='nukus'),
            InlineKeyboardButton(text='Xojeli',callback_data='xojeli'))

qalalar.add(InlineKeyboardButton(text='Shimbay',callback_data='shimbay'),
            InlineKeyboardButton(text='Qonirat',callback_data='qonirat'))
            
qalalar.add(InlineKeyboardButton(text='Taqiyatas',callback_data='taqiyatas'),
            InlineKeyboardButton(text='Qaraozek',callback_data='qaraozek'))

qalalar.add(InlineKeyboardButton(text='Kegeyli',callback_data='kegeyli'),
            InlineKeyboardButton(text='Tortkul',callback_data='tortkul'))