import random

import joblib
import numpy as np
import pandas as pd

import ppdeep.ppdeep
from user.models import Transaction


def ipInfo():
    import urllib.request
    import json

    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        data = json.loads(url.read().decode())

        user_data = {'ip': data['IPv4'], 'country': data['country_name'], 'city': data['city'], 'state': data['state']}
        return user_data


def makeTrancation(request, money, user_from, user_to):
    user_agent = request.META['HTTP_USER_AGENT']
    color_depth = request.session['colorDepth']
    resolution = request.session['resolution'].replace(',', 'x')
    platform = request.session['platform']
    max_touch = int(request.session['max_touch'])
    device_type = 'desktop' if max_touch == 0 else 'mobile'

    slitted_agent = user_agent.split(' ')
    os_version = slitted_agent[1].replace('(', '') + ' ' + slitted_agent[3].replace(';', '')
    brouser_version = slitted_agent[10].replace('/', ' ').split(' ')[0] + ' ' + \
                      slitted_agent[10].replace('/', ' ').split(' ')[1].split('.')[0] + '.' + \
                      slitted_agent[10].replace('/', ' ').split(' ')[1].split('.')[1]

    c = []
    d = []
    m1 = []
    m2 = []
    v = []
    id35_38 = []
    for i in range(0, 14):
        c_distribution = random.randint(1, 100)
        if c_distribution < 40:
            c.append(0)
        elif c_distribution >= 50:
            c.append(1)
        else:
            c.append(random.randint(2, 4))
    for i in range(0, 15):
        d.append(random.randint(0, 315))

    for i in range(0, 339):
        v_distribution = random.randint(1, 100)
        if v_distribution >= 50:
            v.append(0)
        elif v_distribution < 40:
            v.append(1)
        else:
            v.append(random.randint(2, 38000))
    for i in range(0, 3):
        litres = "TF"
        m1.append(random.choice(litres))
    for i in range(0, 5):
        litres = "TF"
        m2.append(random.choice(litres))
    for i in range(0, 4):
        litres = "TF"
        id35_38.append(random.choice(litres))

    c_str = ''
    d_str = ''
    v_str = ''
    m1_str = ''
    m2_str = ''
    id35_38_str = ''

    for i in c:
        c_str += str(i) + ' '
    for i in d:
        d_str += str(i) + ' '
    for i in v:
        v_str += str(i) + ' '
    for i in m1:
        m1_str += str(i) + ' '
    for i in m2:
        m2_str += str(i) + ' '
    for i in id35_38:
        id35_38_str += str(i) + ' '

    c_str = c_str[:len(c_str) - 1]
    d_str = d_str[:len(d_str) - 1]
    v_str = v_str[:len(v_str) - 1]
    m1_str = m1_str[:len(m1_str) - 1]
    m2_str = m2_str[:len(m2_str) - 1]
    id35_38_str = id35_38_str[:len(id35_38_str) - 1]

    card_type1 = random.choice(['visa', 'mastercard'])
    card_type2 = random.choice(['debit', 'credit'])

    transaction = Transaction(money=money, user_from=user_from, user_to=user_to, screen_resolution=resolution,
                              color_depth=color_depth, id_35_38=id35_38_str, device_type=device_type,
                              card_type_1=card_type1,
                              card_type_2=card_type2, c1_c14=c_str, d1_d15=d_str, m1_m3=m1_str, m5_m9=m2_str,
                              v1_v339=v_str, os=os_version, brouser=brouser_version)
    transaction.save()
    return transaction


def get_data_for_fingerprint(request):
    user_info = {}
    locate_info = ipInfo()
    request_info = {}

    request_info['user_agent'] = request.META["HTTP_USER_AGENT"]
    request_info['http_accept'] = request.META["HTTP_ACCEPT"]
    request_info['accept_language'] = request.META["HTTP_ACCEPT_LANGUAGE"]
    request_info['accept_encoding'] = request.META["HTTP_ACCEPT_ENCODING"]

    user_info['locate'] = locate_info
    user_info['request'] = request_info
    print(request_info)

    return user_info


def get_fp_js(request):
    #  print(request.POST['fonts'])
    request.session['colorDepth'] = request.POST['colorDepth']
    request.session['resolution'] = request.POST['resolution']
    request.session['platform'] = request.POST['platform']
    request.session['max_touch'] = request.POST['max_touch']

    colorDepht = request.POST['colorDepth']
    plugins = request.POST['plugins'].split(',')
    resolution = request.POST['resolution'].split(',')
    hardware = request.POST['hardwareConcurrency']
    platform = request.POST['platform']
    audio = request.POST['audio']
    index_db = request.POST['index_db']
    max_touches = request.POST['max_touch']
    locale_storage = request.POST['localStorage']
    gamut = request.POST['gamut']
    canvas = {}
    canvas['geometry'] = request.POST['canvas_geometry']
    canvas['text'] = request.POST['canvas_text']

    math = {}
    math_const = ['acos', 'acosh', 'acoshPf', 'asin', 'asinh', 'asinhPf', 'atanh', 'atanhPf', 'sin', 'cosh', 'coshPf',
                  'tan', 'tanh', 'tanhPf', 'exp', 'expm1', 'expm1Pf', 'log1p', 'expm1Pf', 'powPI']
    for key in math_const:
        math[key] = request.POST[f'math[{key}]']

    fonts_settings = {}
    fonts_settings_keys = ['default', 'apple', 'serif', 'sans', 'mono', 'min', 'system']
    for key in fonts_settings_keys:
        fonts_settings[key] = request.POST[f'fontPreferences[{key}]']

    result = {'colorDepht': colorDepht, 'resolution': resolution, 'plugins': plugins,
              'hardware': hardware,
              'platform': platform, 'audio': audio, 'index_db': index_db, 'max_touches': max_touches,
              'locale_storage': locale_storage,
              'gamut': gamut, 'canvas': canvas, 'math': math, 'fonts_settings': fonts_settings}


def get_hash_peaces(req_data, fp_data):
    math_string = ''
    fonts_string = ''
    plugins_string = ''
    fonts_settings_string = ''
    resolution_string = ''
    for key in fp_data['math']:
        math_string += fp_data['math'][key]

    for key in fp_data['fonts_settings']:
        fonts_settings_string += fp_data['fonts_settings'][key]

    for i in range(len(fp_data['fonts'])):
        fonts_string += fp_data['fonts'][i]

    for i in range(len(fp_data['resolution'])):
        resolution_string += fp_data['resolution'][i]

    for i in range(len(fp_data['plugins'])):
        plugins_string += fp_data['plugins'][i]

    math_hash = ppdeep.ppdeep.hash(math_string)
    fonts_hash = ppdeep.ppdeep.hash(fonts_string)
    fonts_settings_hash = ppdeep.ppdeep.hash(fonts_settings_string)
    plugins_hash = ppdeep.ppdeep.hash(plugins_string)
    resolution_hash = ppdeep.ppdeep.hash(resolution_string)
    geometry_hash = ppdeep.ppdeep.hash(fp_data['canvas']['geometry'])
    text_hash = ppdeep.ppdeep.hash(fp_data['canvas']['text'])
    audio_hash = ppdeep.ppdeep.hash(fp_data['audio'])
    platform_hash = ppdeep.ppdeep.hash(fp_data['platform'])
    index_db_hash = ppdeep.ppdeep.hash(fp_data['index_db'])
    max_touches_hash = ppdeep.ppdeep.hash(fp_data['max_touches'])
    locale_storage_hash = ppdeep.ppdeep.hash(fp_data['locale_storage'])
    gamut_hash = ppdeep.ppdeep.hash(fp_data['gamut'])
    colorDepht_hash = ppdeep.ppdeep.hash(fp_data['colorDepht'])
    hardware_hash = ppdeep.ppdeep.hash(fp_data['hardware'])

    location_string = ''
    request_string = ''

    for key in req_data['locate']:
        location_string += req_data['locate'][key]

    for key in req_data['request']:
        if key != 'user_agent':
            request_string += req_data['request'][key]

    user_agent_hash = ppdeep.ppdeep.hash(req_data['request']['user_agent'])
    location_hash = ppdeep.ppdeep.hash(location_string)
    request_hash = ppdeep.ppdeep.hash(request_string)

    # There is dict. Structure is simple, so it is 'key: [hash, price]'
    # Price it is the parameter which symbolise the costs of this 'key' for main fingerprint

    hash_dict = {'ua': [user_agent_hash, 10], 'locate': [location_hash, 5], 'request': [request_hash, 2],
                 'hard': [hardware_hash, 2], 'cDepth': [colorDepht_hash, 2], 'gamut': [gamut_hash, 1],
                 'localStr': [locale_storage_hash, 2],
                 'touches': [max_touches_hash, 2], 'indexDB': [index_db_hash, 2], 'platform': [platform_hash, 5],
                 'audio': [audio_hash, 10], 'canvasText': [text_hash, 10], 'canvasGeometry': [geometry_hash, 10],
                 'resolution': [resolution_hash, 2], 'plugins': [plugins_hash, 10], 'fonts': [fonts_hash, 10],
                 'fonts_settings': [fonts_settings_hash, 5], 'math': [math_hash, 10]}

    return hash_dict


def comapre_hash(db_hash_items, current_hash_items, user):
    total_price = 0
    string_for_update = ''
    for item in current_hash_items:
        if item != '':
            string_for_update += item + ';'

    for item in range(len(current_hash_items) - 1):
        if db_hash_items[item] != '' and current_hash_items[item] != '':
            db_item = db_hash_items[item].split('-')
            curr_item = current_hash_items[item].split('-')

            if db_item[0] != '' and curr_item[0] != '':
                db_hash = db_item[1].split(',')[0]
                curr_hash = curr_item[1].split(',')[0]
                price = int(curr_item[1].split(',')[1])

                cpm_present = ppdeep.ppdeep.compare(db_hash, curr_hash)
                if cpm_present <= 50:
                    total_price += price

    result_message = ''
    if total_price == 0:
        result_message = 'Ваши отпечатки практически идентичны, поздравляем!'
        user.fp = string_for_update
        user.save()
    elif total_price != 0 and total_price < 30:
        result_message = 'Кажется, параметры вашего несколько изменились, однако это всё ещё вы)\n' \
                         f'Ваш risc score: {total_price}%'
        user.fp = string_for_update
        user.save()
    elif total_price >= 30 and total_price < 50:
        result_message = 'Параметры вашего отпечатка значительно изменились, пожалуйста подтвердите что это вы.\n' \
                         f'Ваш risc score: {total_price}%'
    elif total_price >= 50:
        result_message = 'Параметры вашего отпечатка претерпели очень радикальные изменения, пожалуйста подтвердите что это вы.\n' \
                         f'Ваш risc score: {total_price}%'
    return result_message


def isFraude(transaction):
    amt = transaction.money
    # card4 = 4 if transaction.card_type_1 == "visa" else 2
    # card6 = 1 if transaction.card_type_2 == 'credit' else 2
    #
    data = []
    c = list(map(lambda x: float(x), transaction.c1_c14.split(' ')))
    d = list(map(lambda x: float(x), transaction.d1_d15.split(' ')))
    m1_3 = transaction.m1_m3.split(' ')
    m5_m9 = transaction.m5_m9.split(' ')
    v = list(map(lambda x: float(x), transaction.v1_v339.split(' ')))
    card4 = transaction.card_type_1
    card6 = transaction.card_type_2

    # id30
    os = transaction.os
    # id31
    brouser = transaction.brouser
    # id32
    depth = transaction.color_depth
    # id33
    resolution = transaction.screen_resolution

    id35_38 = transaction.id_35_38.split(' ')

    device_type = transaction.device_type

    data.append(amt)
    data.append(card4)
    data.append(card6)
    data += c
    data += d
    data += m1_3
    data += m5_m9
    data += v
    data.append(os)
    data.append(brouser)
    data.append(depth)
    data.append(resolution)
    data += id35_38
    data.append(device_type)
    columns_str = "TransactionAmt	card4	card6	C1	C2	C3	C4	C5	C6	C7	C8	C9	C10	C11	C12	C13	C14	D1	D2	D3	D4	D5	D6	D7	D8	D9	D10	D11	D12	D13	D14	D15	M1	M2	M3	M5	M6	M7	M8	M9	V1	V2	V3	V4	V5	V6	V7	V8	V9	V10	V11	V12	V13	V14	V15	V16	V17	V18	V19	V20	V21	V22	V23	V24	V25	V26	V27	V28	V29	V30	V31	V32	V33	V34	V35	V36	V37	V38	V39	V40	V41	V42	V43	V44	V45	V46	V47	V48	V49	V50	V51	V52	V53	V54	V55	V56	V57	V58	V59	V60	V61	V62	V63	V64	V65	V66	V67	V68	V69	V70	V71	V72	V73	V74	V75	V76	V77	V78	V79	V80	V81	V82	V83	V84	V85	V86	V87	V88	V89	V90	V91	V92	V93	V94	V95	V96	V97	V98	V99	V100	V101	V102	V103	V104	V105	V106	V107	V108	V109	V110	V111	V112	V113	V114	V115	V116	V117	V118	V119	V120	V121	V122	V123	V124	V125	V126	V127	V128	V129	V130	V131	V132	V133	V134	V135	V136	V137	V138	V139	V140	V141	V142	V143	V144	V145	V146	V147	V148	V149	V150	V151	V152	V153	V154	V155	V156	V157	V158	V159	V160	V161	V162	V163	V164	V165	V166	V167	V168	V169	V170	V171	V172	V173	V174	V175	V176	V177	V178	V179	V180	V181	V182	V183	V184	V185	V186	V187	V188	V189	V190	V191	V192	V193	V194	V195	V196	V197	V198	V199	V200	V201	V202	V203	V204	V205	V206	V207	V208	V209	V210	V211	V212	V213	V214	V215	V216	V217	V218	V219	V220	V221	V222	V223	V224	V225	V226	V227	V228	V229	V230	V231	V232	V233	V234	V235	V236	V237	V238	V239	V240	V241	V242	V243	V244	V245	V246	V247	V248	V249	V250	V251	V252	V253	V254	V255	V256	V257	V258	V259	V260	V261	V262	V263	V264	V265	V266	V267	V268	V269	V270	V271	V272	V273	V274	V275	V276	V277	V278	V279	V280	V281	V282	V283	V284	V285	V286	V287	V288	V289	V290	V291	V292	V293	V294	V295	V296	V297	V298	V299	V300	V301	V302	V303	V304	V305	V306	V307	V308	V309	V310	V311	V312	V313	V314	V315	V316	V317	V318	V319	V320	V321	V322	V323	V324	V325	V326	V327	V328	V329	V330	V331	V332	V333	V334	V335	V336	V337	V338	V339	id_30	id_31	id_32	id_33	id_35	id_36	id_37	id_38	DeviceType"
    columns = columns_str.split('	')
    encoder = joblib.load('encoder.pkl')
    data2 = np.array(data)
    x = pd.DataFrame([data2], columns=columns, dtype=float)
    for f in x.columns:
        if x[f].dtype == 'object':
            encoder.fit(list(x[f].values))
            x[f] = encoder.transform(list(x[f].values))
    model = joblib.load('fraud_model.pkl')
    y_pred = model.predict(x)


    return y_pred[0]
    # return y_pred.iat[0,0]
    # m1_3 = list(map(lambda x: 1 if x == 'T' else 0, transaction.m1_m3.split(' ')))
    # m1_3[0] = int(not bool(m1_3[0]))
    # m5_m9 = list(map(lambda x: 1 if x == 'T' else 0, transaction.m5_m9.split(' ')))
    # v = list(map(lambda x: float(x), transaction.v1_v339.split(' ')))
    #
    # devise_type = 1 if transaction.device_type == 'mobile' else 0
    # id35_38 = list(map(lambda x: 1 if x == 'T' else 0, transaction.id_35_38.split(' ')))
    # os_type = 0
    # if transaction.os.lower() == 'windows 10':
    #     os_type = 38
    # elif transaction.os.lower() == 'windows 7':
    #     os_type = 39
    # elif transaction.os.lower().contains('ios'):
    #     os_type = 59
    # elif transaction.os.lower().contains('android'):
    #     os_type = 7
    # elif transaction.os.lower().contains('mac'):
    #     os_type = 10

    pass
