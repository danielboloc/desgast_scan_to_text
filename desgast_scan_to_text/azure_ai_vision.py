import json
import re


azure_vision_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_1.json"


def get_next_words(words, idx, pattern):
    l_of_words = []
    # give a certain range (will capture the max next 10 words, which is enough)
    for i in range(1,10):
        # if it matches the next question stop
        if words[idx+i]['content'] == pattern:
            break
        # until then keep adding the words to the list
        else:
            l_of_words.append(words[idx+i]['content'])

    # save list as only one string
    return " ".join(l_of_words)

def check_yes_no(Q00):
    # this is a question text
    if re.search('no', Q00, re.IGNORECASE):
        return 0
    if re.search('si', Q00, re.IGNORECASE):
        return 1

# Bloque 1

with open(azure_vision_json) as json_file:
    data = json.load(json_file)


    words = data['words']
    lines = data['lines']

    print("Type:", type(data))
    print("Type:", type(words))
    print("Type:", type(lines))

    # give an id code, starting with 38
    current_n = 38

    # data to recover as we progress through the words/lines
    GRAL = {
        "N": current_n,
    }

    for idx, word in enumerate(words):
        #print("CONTENT: ", word['content'])

        # Data
        if word['content'] == "Data:":
            print("Data: ", words[idx+1]['content'])
            GRAL["Data"] = words[idx+1]['content']
        
        # Codi
        if word['content'] == "d'identificació:":
            print("Codi: ", words[idx+1]['content'])
            GRAL["Q00"] = words[idx+1]['content']
            
        # Grup
        if word['content'] == "Grup:":
            print("Grup: ", words[idx+1]['content'])
            GRAL["Grup"] = words[idx+1]['content']
            
        # Data Naix
        if word['content'] == "Nacimiento":
            print("Data Naix: ", words[idx+1]['content'])
            GRAL["Data Naix"] = words[idx+1]['content']

        # Q02
        if word['content'] == "Sexo":
            print("Sexo: ", words[idx+1]['content'])
            GRAL["Q02"] = words[idx+1]['content']

        # Q03
        if word['content'] == "(cm)":
            print("Altura: ", words[idx+1]['content'])
            GRAL["Q03"] = words[idx+1]['content']

        # Q04
        peso = re.compile(r"(kg)")
        if peso.search(word['content']):
            print("Peso: ", words[idx+1]['content'])
            GRAL["Q04"] = words[idx+1]['content']
        
        # Q05, patologia importante
        if word['content'] == "importante?":
            print("Patología: ", words[idx+1]['content'])
            Q05 = words[idx+1]['content']

            GRAL["Q05"] = check_yes_no(Q05)
            GRAL["Q05_full_text"] = get_next_words(words, idx, "¿Ha")

        # Q06, operado
        if word['content'] == "vez?":
            print("Operado: ", words[idx+1]['content'])
            Q06 = words[idx+1]['content']

            GRAL["Q06"] = check_yes_no(Q06)
            GRAL["Q06_full_text"] = get_next_words(words, idx, "¿Presenta")

        # Q07, alergia
        if word['content'] == "alergia?":
            print("Alergia: ", words[idx+1]['content'])
            Q07 = words[idx+1]['content']

            GRAL["Q07"] = check_yes_no(Q07)
            GRAL["Q07_full_text"] = get_next_words(words, idx, "¿Toma")

            # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
            if GRAL["Q07"] == None and GRAL["Q07_full_text"] is not None:
                GRAL["Q07"] = 1

        # Q08, medicacion
        if word['content'] == "habitual?" and \
            words[idx-1]['content'] == "manera" and \
            words[idx-2]['content'] == "de" and \
            words[idx-3]['content'] == "medicación":

            print("Medicacion: ", words[idx+1]['content'])
            Q08 = words[idx+1]['content']

            GRAL["Q08"] = check_yes_no(Q08)
            GRAL["Q08_full_text"] = get_next_words(words, idx, "¿Toma")

            # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
            if GRAL["Q08"] == None and GRAL["Q08_full_text"] is not None:
                GRAL["Q08"] = 1

        # Q09, medicacion
        if word['content'] == "cuál:":
            print("Efervescentes: ", words[idx+1]['content'])
            Q09 = words[idx+1]['content']

            GRAL["Q09"] = check_yes_no(Q09)
            GRAL["Q09_full_text"] = get_next_words(words, idx, "¿Consume")

            # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
            if GRAL["Q09"] == None and GRAL["Q09_full_text"] is not None:
                GRAL["Q09"] = 1

        # Q10, alcohol
        if word['content'] == "habitual?" and \
            words[idx-1]['content'] == "manera" and \
            words[idx-2]['content'] == "de" and \
            words[idx-3]['content'] == "drogas":

            # get 'NO' box bounderies
            NO_box = words[idx+1]['boundingBox']
            # get 'SI' box bounderies
            SI_box = words[idx+2]['boundingBox']
            Cantidad_box = words[idx+3]['boundingBox']

            # a ------ b
            # |        |
            # d ------ c
            # example [ 1093, 987, 1228, 984, 1229, 1019, 1094, 1023 ]
            #             ax   ay    bx   by   cx    cy    dx    dy
            ax = NO_box[0]
            ay = NO_box[1]
            bx = NO_box[2]
            by = NO_box[3]
            cx = NO_box[4]
            cy = NO_box[5]
            dx = NO_box[6]
            dy = NO_box[7]

            ax_si = SI_box[0]
            ay_si = SI_box[1]
            bx_si = SI_box[2]
            by_si = SI_box[3]
            cx_si = SI_box[4]
            cy_si = SI_box[5]
            dx_si = SI_box[6]
            dy_si = SI_box[7]

            ax_cant = Cantidad_box[0]
            bx_cant = Cantidad_box[2]

            print("NO box:", ax, " - ", bx)
            print("SI box:", ax_si, " - ", bx_si)
            print("Cantidad box:", ax_cant, " - ", bx_cant)

print("GRAL: ", GRAL)


