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
            diaria_box = words[idx+4]['boundingBox']

            # a ------ b
            # |        |
            # d ------ c
            # example [ 1093, 987, 1228, 984, 1229, 1019, 1094, 1023 ]
            #             ax   ay    bx   by   cx    cy    dx    dy
            ax = NO_box[0] - 20 # some buffer
            ay = NO_box[1]
            bx = NO_box[2] + 20
            by = NO_box[3]
            cx = NO_box[4]
            cy = NO_box[5]
            dx = NO_box[6]
            dy = NO_box[7]

            ax_si = SI_box[0] - 20 
            ay_si = SI_box[1]
            bx_si = SI_box[2] + 20
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

            alcohol = words[idx+5]['content']
            alcohol_response = words[idx+6]['content']
            alcohol_box = words[idx+6]['boundingBox']
            if ax <= alcohol_box[0] <= bx:
                GRAL["Q10"] = 0
            elif ax_si <= alcohol_box[0] <= bx_si:
                GRAL["Q10"] = 1

        # Q11, Tabaco
        if word['content'] == "Tabaco":
            print("Tabaco: ", words[idx+1]['content'])
            Q11 = words[idx+1]['content']

            tabaco_response = words[idx+1]['content']
            tabaco_box = words[idx+1]['boundingBox']
            if ax <= tabaco_box[0] <= bx:
                GRAL["Q11"] = 0
            elif ax_si <= tabaco_box[0] <= bx_si:
                GRAL["Q11"] = 1

        # Q12, Otras drogas
        if word['content'] == "Otras" and \
            words[idx+1]['content'] == "drogas":

            print("Otras drogas: ", words[idx+2]['content'])
            Q12 = words[idx+2]['content']

            drogas_response = words[idx+2]['content']
            drogas_box = words[idx+2]['boundingBox']
            if ax <= drogas_box[0] <= bx:
                GRAL["Q12"] = 0
            elif ax_si <= drogas_box[0] <= bx_si:
                GRAL["Q12"] = 1

        # Q13, GERD (to be reviewed)
        # Q14, TCA (to be reviewed)
        # Q15, JOC (to be reviewed)
        # Q16, Bso (to be reviewed)
        # Q17, Bdi (to be reviewed)
        # It is calculated as 0,1,2,3, there's no 1.5 or 4 or 2.5
        # From the first part of the table: "Alguna vez ha sufrido..."
        if word['content'] == "Alguna" and \
            words[idx+1]['content'] == "vez" and \
            words[idx+2]['content'] == "ha" and \
            words[idx+3]['content'] == "sufrido" and \
            words[idx+4]['content'] == "...":

            # Only the 0 and 2 indexes for these
            NO_alguna_vez_sufrido_box = words[idx+5]['boundingBox']
            SI_alguna_vez_sufrido_box = words[idx+6]['boundingBox']
            # there are '|' in between
            AFECTACION_LIGERA_alguna_vez_box = words[idx+7]['boundingBox']
            AFECTACION_MODERADA_alguna_vez_box = words[idx+9]['boundingBox']
            AFECTACION_SEVERA_alguna_vez_box = words[idx+11]['boundingBox']

            # idx + 12 -> LIGERA
            # idx + 13 -> MODERADA
            # idx + 14 -> SEVERA
            # idx + 15 -> Regurgitacion/quemazon

            # Q13, GERD
            # print("Regurgitacion/quemazon: ", words[idx+16]['content'])
            # Q13_response = words[idx+16]['content']
            # Q13_box = words[idx+16]['boundingBox']
            # if (NO_alguna_vez_sufrido_box[0] - 20) <= Q13_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
            #     GRAL["Q13"] = 0
            # elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q13_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
            #     GRAL["Q13"] = 1
            for i in range(1,60):
                # matches the next question
                if words[idx+i]['content'] == "Regurgitación/quemazón":
                    # get the 'X' and box of the match
                    print("Regurgitacion/quemazon: ", words[idx+i+1]['content'])
                    Q13_response = words[idx+i+1]['content']
                    Q13_box = words[idx+i+1]['boundingBox']
                    if (NO_alguna_vez_sufrido_box[0] - 20) <= Q13_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
                        GRAL["Q13"] = 0
                    elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q13_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
                        Q13_box_afectacion = words[idx+i+2]['boundingBox']
                        if (AFECTACION_LIGERA_alguna_vez_box[0] - 20) <= Q13_box_afectacion[0] <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20):
                            GRAL["Q13"] = 1
                        if (AFECTACION_MODERADA_alguna_vez_box[0] - 20) <= Q13_box_afectacion[0] <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20):
                            GRAL["Q13"] = 2
                        if (AFECTACION_SEVERA_alguna_vez_box[0] - 20) <= Q13_box_afectacion[0] <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20):
                            GRAL["Q13"] = 3
                    
                    break
            
            # idx + 17 -> 'Anorexia/'
            # idx + 18 -> 'Bulimia'
            # idx + 19 -> 'con'
            # idx + 20 -> 'vomito'
            # idx + 21 -> 'X'
            # Q14, TCA
            # print("Anorexia/Bulimia con vomito: ", words[idx+21]['content'])
            # Q14_response = words[idx+21]['content']
            # Q14_box = words[idx+21]['boundingBox']
            # if (NO_alguna_vez_sufrido_box[0] - 20) <= Q14_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
            #     GRAL["Q14"] = 0
            #     idx_for_next_row = 21
            # elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q14_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
            #     if (AFECTACION_LIGERA_alguna_vez_box[0] - 20) <= Q14_box[0] <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20):
            #         GRAL["Q14"] = 1
            #     if (AFECTACION_MODERADA_alguna_vez_box[0] - 20) <= Q14_box[0] <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20):
            #         GRAL["Q14"] = 2
            #     if (AFECTACION_SEVERA_alguna_vez_box[0] - 20) <= Q14_box[0] <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20):
            #         GRAL["Q14"] = 3
            #     idx_for_next_row = 22
            for i in range(1,60):
                # matches the next question
                if words[idx+i]['content'] == "Anorexia/" and \
                    words[idx+i+1]['content'] == "Bulimia" and \
                    words[idx+i+2]['content'] == "con" and \
                    words[idx+i+3]['content'] == "vómito":
                    # get the 'X' and box of the match
                    print("Anorexia/ Bulimia con vomito: ", words[idx+i+4]['content'])
                    Q14_response = words[idx+i+4]['content']
                    Q14_box = words[idx+i+4]['boundingBox']
                    if (NO_alguna_vez_sufrido_box[0] - 20) <= Q14_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
                        GRAL["Q14"] = 0
                    elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q14_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
                        Q14_box_afectacion = words[idx+i+5]['boundingBox']
                        if (AFECTACION_LIGERA_alguna_vez_box[0] - 20) <= Q14_box_afectacion[0] <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20):
                            GRAL["Q14"] = 1
                        if (AFECTACION_MODERADA_alguna_vez_box[0] - 20) <= Q14_box_afectacion[0] <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20):
                            GRAL["Q14"] = 2
                        if (AFECTACION_SEVERA_alguna_vez_box[0] - 20) <= Q14_box_afectacion[0] <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20):
                            GRAL["Q14"] = 3
                    break

            # idx + idx_for_next_row -> Juego
            # idx + idx_for_next_row + 1 -> patológico
            # idx + idx_for_next_row + 2 -> y
            # idx + idx_for_next_row + 3 -> bruxismo
            # idx + idx_for_next_row + 3 -> diurno
            # idx + idx_for_next_row + 3 -> X
            # Q15, JOC
            # idx_for_next_row += 5
            # print("Juego patologico y bruxismo diurno: ", words[idx+idx_for_next_row]['content'])
            # Q15_response = words[idx+idx_for_next_row]['content']
            # Q15_box = words[idx+idx_for_next_row]['boundingBox']
            # if (NO_alguna_vez_sufrido_box[0] - 20) <= Q15_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
            #     GRAL["Q15"] = 0
            #     idx_for_next_row = 17
            # elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q15_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
            #     if (AFECTACION_LIGERA_alguna_vez_box[0] - 20) <= Q15_box[0] <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20):
            #         GRAL["Q15"] = 1
            #     if (AFECTACION_MODERADA_alguna_vez_box[0] - 20) <= Q15_box[0] <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20):
            #         GRAL["Q15"] = 2
            #     if (AFECTACION_SEVERA_alguna_vez_box[0] - 20) <= Q15_box[0] <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20):
            #         GRAL["Q15"] = 3
            #     idx_for_next_row = 18
            for i in range(1,60):
                # matches the next question
                if words[idx+i]['content'] == "Juego" and \
                    words[idx+i+1]['content'] == "patológico" and \
                    words[idx+i+2]['content'] == "y" and \
                    words[idx+i+3]['content'] == "bruxismo" and \
                    words[idx+i+4]['content'] == "diurno":

                    # get the 'X' and box of the match
                    print("Juego patologico y bruxismo diurno: ", words[idx+i+5]['content'])
                    Q15_response = words[idx+i+5]['content']
                    Q15_box = words[idx+i+5]['boundingBox']
                    if (NO_alguna_vez_sufrido_box[0] - 20) <= Q15_box[0] <= (NO_alguna_vez_sufrido_box[2] + 20):
                        GRAL["Q15"] = 0
                    elif (SI_alguna_vez_sufrido_box[0] - 20) <= Q15_box[0] <= (SI_alguna_vez_sufrido_box[2] + 20):
                        Q15_box_afectacion = words[idx+i+6]['boundingBox']
                        if (AFECTACION_LIGERA_alguna_vez_box[0] - 20) <= Q15_box_afectacion[0] <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20):
                            GRAL["Q15"] = 1
                        if (AFECTACION_MODERADA_alguna_vez_box[0] - 20) <= Q15_box_afectacion[0] <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20):
                            GRAL["Q15"] = 2
                        if (AFECTACION_SEVERA_alguna_vez_box[0] - 20) <= Q15_box_afectacion[0] <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20):
                            GRAL["Q15"] = 3
                    break

        if word['content'] == "En" and \
            words[idx+1]['content'] == "el" and \
            words[idx+2]['content'] == "último" and \
            words[idx+3]['content'] == "mes" and \
            words[idx+4]['content'] == "ha" and \
            words[idx+5]['content'] == "sufrido" and \
            words[idx+6]['content'] == "...":

            # Only the 0 and 2 indexes for these
            NO_ultimo_mes_sufrido_box = words[idx+7]['boundingBox']
            SI_ultimo_mes_sufrido_box = words[idx+8]['boundingBox']
            # there are '|' in between
            AFECTACION_LIGERA_ultimo_mes_box = words[idx+9]['boundingBox']
            AFECTACION_MODERADA_ultimo_mes_box = words[idx+11]['boundingBox']
            AFECTACION_SEVERA_ultimo_mes_box = words[idx+13]['boundingBox']

print("GRAL: ", GRAL)


