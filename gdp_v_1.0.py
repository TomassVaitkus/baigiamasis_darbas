import pandas as pd
from sqlalchemy import create_engine

db_uri = 'sqlite:///L:/baigiamasis_darbas/database_file.db'
engine = create_engine(db_uri)

adresai1 = ['Laisvės al. 123',
'Vytauto pr. 55-4',
'Vilniaus g. 10A-15',
'Maironio g. 7',
'Kęstučio g. 19-5',
'Savanorių pr. 85B',
'Žemaičių g. 14-2',
'Partizanų g. 30-8',
'Petrašiūnų g. 2C',
'Gėlių g. 11-3',
'Kauno pilis',
'Nemuno g. 27',
'Kareivių g. 7-9',
'Radvilėnų pl. 21A-6',
'A. Mickevičiaus g. 29-12',
'J. Basanavičiaus g. 40',
'Varnių g. 9-2',
'Taikos pr. 72',
'Tauro g. 17-1',
'M. K. Čiurlionio g. 82',
'Žaliakalnio g. 117A-8',
'P. Vileišio g. 18-3',
'Karaliaus Mindaugo pr. 51',
'St. Donelaičio g. 62',
'Daukanto g. 27-4',
'Jonavos g. 45-2',
'Smėlio g. 4-6',
'Žirmūnų g. 12A',
'J. Gruodžio g. 14-1',
'V. Kudirkos g. 2-10']

adresai2 = [
    'Savanorių pr. 123',
    'Kęstučio g. 7-3',
    'Gedimino pr. 56-2',
    'Raudondvario pl. 18',
    'Jonavos pl. 9A',
    'Kazimiero g. 33',
    'Gričiupio g. 15-4',
    'Birutės al. 91',
    'Basanavičiaus al. 74',
    'Geležinkelio g. 12-6',
    'Naujakiemio g. 29',
    'Radvilėnų g. 3-2',
    'Gruodžio g. 19',
    'Šviesos g. 8A-10',
    'Aukštaičių g. 21',
    'Kuršių g. 37-5',
    'Neries krantinė 7',
    'Ateities g. 53',
    'Pilies g. 26-1',
    'Lukšio g. 4-8',
    'Kotrynos g. 92',
    'Veiverių g. 63-9',
    'Baršausko g. 14A',
    'Pramonės pr. 39',
    'Saulės g. 16',
    'Daukanto al. 81',
    'Gabių g. 47',
    'Jotvingių g. 5-3',
    'Vienybės pl. 22',
    'S. Daukanto g. 11-7'
]
telefonu_numeriai = [
    "+37061234567",
    "+37065543210",
    "+37064123456",
    "+37067890123",
    "+37069987654",
    "+37060000000",
    "+37061111111",
    "+37062222222",
    "+37063333333",
    "+37064444444",
    "+37065555555",
    "+37066666666",
    "+37067777777",
    "+37068888888",
    "+37069999999",
    "+37061010101",
    "+37062121212",
    "+37063232323",
    "+37064343434",
    "+37065454545",
    "+37066565656",
    "+37067676767",
    "+37068787878",
    "+37069898989",
    "+37060909090",
    "+37062020202",
    "+37063131313",
    "+37064242424",
    "+37065353535",
    "+37066464646"
]

svoriai = [
    0.5,
    1.2,
    2.8,
    3.5,
    0.7,
    2.1,
    4.9,
    6.3,
    0.9,
    1.8,
    5.2,
    3.1,
    0.3,
    2.5,
    1.5,
    4.7,
    7.8,
    0.6,
    3.8,
    2.3,
    1.1,
    4.5,
    6.7,
    2.2,
    0.8,
    3.2,
    1.6,
    5.9,
    4.3,
    0.4
]


df = pd.DataFrame({'Paemimo': adresai1,
                   "Pristatymo": adresai2, 
                   "Svoris": svoriai, 
                   "Tel_nr":telefonu_numeriai,
                   "user_id":'',
                   "delivered": False})
df['id'] = range(1, len(df) + 1)
df.to_sql('data', con=engine, if_exists='replace', index=False)
