import json
import re


azure_vision_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_1.json"
azure_page_3_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_page_3.json"
azure_page_4_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_page_4.json"
azure_page_6_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_page_6.json"
azure_page_7_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_page_7.json"
azure_page_10_json = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/azure_ai_vision_studio/test_case_page_10.json"


def get_next_words(words, idx, pattern, range_length=10):
    l_of_words = []
    # give a certain range (will capture the max next 10 words, which is enough)
    for i in range(1, range_length):
        # if it matches the next question stop
        if words[idx + i]["content"] == pattern:
            break
        # until then keep adding the words to the list
        else:
            l_of_words.append(words[idx + i]["content"])

    # save list as only one string
    return " ".join(l_of_words)


def check_yes_no(Q00):
    # this is a question text
    if re.search("no", Q00, re.IGNORECASE):
        return 0
    if re.search("si", Q00, re.IGNORECASE):
        return 1


def determine_afectacion(
    NO_box,
    SI_box,
    AFECTACION_LIGERA_box,
    AFECTACION_MODERADA_box,
    AFECTACION_SEVERA_box,
    words,
    idx,
    conditions,
    min_lookahead=1,
    max_lookahead=60,
):
    for i in range(min_lookahead, max_lookahead):
        all_conditions_true = all(
            words[idx + i + index]["content"] == element
            for index, element in enumerate(conditions)
        )

        if all_conditions_true:
            # get the 'X' and box of the match
            print(" ".join(conditions), words[idx + i + len(conditions)]["content"])
            Q_box = words[idx + i + len(conditions)]["boundingBox"]

            if (NO_box[0] - 20) <= Q_box[0] <= (NO_box[2] + 20):
                return 0
            elif (SI_box[0] - 20) <= Q_box[0] <= (SI_box[2] + 20):
                # get the next 'X' if the response is 'SI'
                Q_box_afectacion = words[idx + i + len(conditions) + 1]["boundingBox"]
                if (
                    (AFECTACION_LIGERA_box[0] - 20)
                    <= Q_box_afectacion[0]
                    <= (AFECTACION_LIGERA_box[2] + 20)
                ):
                    return 1
                if (
                    (AFECTACION_MODERADA_box[0] - 20)
                    <= Q_box_afectacion[0]
                    <= (AFECTACION_MODERADA_box[2] + 20)
                ):
                    return 2
                if (
                    (AFECTACION_SEVERA_box[0] - 20)
                    <= Q_box_afectacion[0]
                    <= (AFECTACION_SEVERA_box[2] + 20)
                ):
                    return 3
            break

def lookahead_and_get_index(words, idx, pattern):
    index_when_matched = 0
    # take the whole range of the words list
    for i in range(1, len(words)):
        # if it matches the next question stop
        if words[idx + i]["content"] == pattern:
            index_when_matched = idx + i
            break

    # return the index
    return index_when_matched

# give an id code, starting with 38
current_n = 38

# data to recover as we progress through the words/lines
# dangerous for tests, because values will be overwritten, so create multiple for different sections
GRAL = {
    "N": current_n,
}

# Bloque 1, page 2 in file
def read_and_extract_page_two(azure_vision_json):

    with open(azure_vision_json) as json_file:
        data = json.load(json_file)

        words = data["words"]
        lines = data["lines"]

        print("Type:", type(data))
        print("Type:", type(words))
        print("Type:", type(lines))

        for idx, word in enumerate(words):
            # print("CONTENT: ", word['content'])

            # Data
            if word["content"] == "Data:":
                print("Data: ", words[idx + 1]["content"])
                GRAL["Data"] = words[idx + 1]["content"]

            # Codi
            if word["content"] == "d'identificació:":
                print("Codi: ", words[idx + 1]["content"])
                GRAL["Q00"] = words[idx + 1]["content"]

            # Grup
            if word["content"] == "Grup:":
                print("Grup: ", words[idx + 1]["content"])
                GRAL["Grup"] = words[idx + 1]["content"]

            # Data Naix
            if word["content"] == "Nacimiento":
                print("Data Naix: ", words[idx + 1]["content"])
                GRAL["Data Naix"] = words[idx + 1]["content"]

            # Q02
            if word["content"] == "Sexo":
                print("Sexo: ", words[idx + 1]["content"])
                GRAL["Q02"] = words[idx + 1]["content"]

            # Q03
            if word["content"] == "(cm)":
                print("Altura: ", words[idx + 1]["content"])
                GRAL["Q03"] = words[idx + 1]["content"]

            # Q04
            peso = re.compile(r"(kg)")
            if peso.search(word["content"]):
                print("Peso: ", words[idx + 1]["content"])
                GRAL["Q04"] = words[idx + 1]["content"]

            # Q05, patologia importante
            if word["content"] == "importante?":
                print("Patología: ", words[idx + 1]["content"])
                Q05 = words[idx + 1]["content"]

                GRAL["Q05"] = check_yes_no(Q05)
                GRAL["Q05_full_text"] = get_next_words(words, idx, "¿Ha")

            # Q06, operado
            if word["content"] == "vez?":
                print("Operado: ", words[idx + 1]["content"])
                Q06 = words[idx + 1]["content"]

                GRAL["Q06"] = check_yes_no(Q06)
                GRAL["Q06_full_text"] = get_next_words(words, idx, "¿Presenta")

            # Q07, alergia
            if word["content"] == "alergia?":
                print("Alergia: ", words[idx + 1]["content"])
                Q07 = words[idx + 1]["content"]

                GRAL["Q07"] = check_yes_no(Q07)
                GRAL["Q07_full_text"] = get_next_words(words, idx, "¿Toma")

                # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
                if GRAL["Q07"] == None and GRAL["Q07_full_text"] is not None:
                    GRAL["Q07"] = 1

            # Q08, medicacion
            if (
                word["content"] == "habitual?"
                and words[idx - 1]["content"] == "manera"
                and words[idx - 2]["content"] == "de"
                and words[idx - 3]["content"] == "medicación"
            ):
                print("Medicacion: ", words[idx + 1]["content"])
                Q08 = words[idx + 1]["content"]

                GRAL["Q08"] = check_yes_no(Q08)
                GRAL["Q08_full_text"] = get_next_words(words, idx, "¿Toma")

                # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
                if GRAL["Q08"] == None and GRAL["Q08_full_text"] is not None:
                    GRAL["Q08"] = 1

            # Q09, medicacion
            if word["content"] == "cuál:":
                print("Efervescentes: ", words[idx + 1]["content"])
                Q09 = words[idx + 1]["content"]

                GRAL["Q09"] = check_yes_no(Q09)
                GRAL["Q09_full_text"] = get_next_words(words, idx, "¿Consume")

                # if there is no 'NO' or 'SI', but there is text, assign to 'SI'/1
                if GRAL["Q09"] == None and GRAL["Q09_full_text"] is not None:
                    GRAL["Q09"] = 1

            # Q10, alcohol
            if (
                word["content"] == "habitual?"
                and words[idx - 1]["content"] == "manera"
                and words[idx - 2]["content"] == "de"
                and words[idx - 3]["content"] == "drogas"
            ):
                # get 'NO' box bounderies
                NO_box = words[idx + 1]["boundingBox"]
                # get 'SI' box bounderies
                SI_box = words[idx + 2]["boundingBox"]
                Cantidad_box = words[idx + 3]["boundingBox"]
                diaria_box = words[idx + 4]["boundingBox"]

                # a ------ b
                # |        |
                # d ------ c
                # example [ 1093, 987, 1228, 984, 1229, 1019, 1094, 1023 ]
                #             ax   ay    bx   by   cx    cy    dx    dy
                ax = NO_box[0] - 20  # some buffer
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

                alcohol = words[idx + 5]["content"]
                alcohol_response = words[idx + 6]["content"]
                alcohol_box = words[idx + 6]["boundingBox"]
                if ax <= alcohol_box[0] <= bx:
                    GRAL["Q10"] = 0
                elif ax_si <= alcohol_box[0] <= bx_si:
                    GRAL["Q10"] = 1

            # Q11, Tabaco
            if word["content"] == "Tabaco":
                print("Tabaco: ", words[idx + 1]["content"])
                Q11 = words[idx + 1]["content"]

                tabaco_response = words[idx + 1]["content"]
                tabaco_box = words[idx + 1]["boundingBox"]
                if ax <= tabaco_box[0] <= bx:
                    GRAL["Q11"] = 0
                elif ax_si <= tabaco_box[0] <= bx_si:
                    GRAL["Q11"] = 1

            # Q12, Otras drogas
            if word["content"] == "Otras" and words[idx + 1]["content"] == "drogas":
                print("Otras drogas: ", words[idx + 2]["content"])
                Q12 = words[idx + 2]["content"]

                drogas_response = words[idx + 2]["content"]
                drogas_box = words[idx + 2]["boundingBox"]
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
            if (
                word["content"] == "Alguna"
                and words[idx + 1]["content"] == "vez"
                and words[idx + 2]["content"] == "ha"
                and words[idx + 3]["content"] == "sufrido"
                and words[idx + 4]["content"] == "..."
            ):
                # Only the 0 and 2 indexes for these
                NO_alguna_vez_sufrido_box = words[idx + 5]["boundingBox"]
                SI_alguna_vez_sufrido_box = words[idx + 6]["boundingBox"]
                # there are '|' in between
                AFECTACION_LIGERA_alguna_vez_box = words[idx + 7]["boundingBox"]
                AFECTACION_MODERADA_alguna_vez_box = words[idx + 9]["boundingBox"]
                AFECTACION_SEVERA_alguna_vez_box = words[idx + 11]["boundingBox"]

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
                for i in range(1, 60):
                    # matches the next question
                    if words[idx + i]["content"] == "Regurgitación/quemazón":
                        # get the 'X' and box of the match
                        print("Regurgitacion/quemazon: ", words[idx + i + 1]["content"])
                        Q13_response = words[idx + i + 1]["content"]
                        Q13_box = words[idx + i + 1]["boundingBox"]
                        if (
                            (NO_alguna_vez_sufrido_box[0] - 20)
                            <= Q13_box[0]
                            <= (NO_alguna_vez_sufrido_box[2] + 20)
                        ):
                            GRAL["Q13"] = 0
                        elif (
                            (SI_alguna_vez_sufrido_box[0] - 20)
                            <= Q13_box[0]
                            <= (SI_alguna_vez_sufrido_box[2] + 20)
                        ):
                            Q13_box_afectacion = words[idx + i + 2]["boundingBox"]
                            if (
                                (AFECTACION_LIGERA_alguna_vez_box[0] - 20)
                                <= Q13_box_afectacion[0]
                                <= (AFECTACION_LIGERA_alguna_vez_box[2] + 20)
                            ):
                                GRAL["Q13"] = 1
                            if (
                                (AFECTACION_MODERADA_alguna_vez_box[0] - 20)
                                <= Q13_box_afectacion[0]
                                <= (AFECTACION_MODERADA_alguna_vez_box[2] + 20)
                            ):
                                GRAL["Q13"] = 2
                            if (
                                (AFECTACION_SEVERA_alguna_vez_box[0] - 20)
                                <= Q13_box_afectacion[0]
                                <= (AFECTACION_SEVERA_alguna_vez_box[2] + 20)
                            ):
                                GRAL["Q13"] = 3

                        break

                # Q14, TCA

                GRAL["Q14"] = determine_afectacion(
                                NO_alguna_vez_sufrido_box,
                                SI_alguna_vez_sufrido_box,
                                AFECTACION_LIGERA_alguna_vez_box,
                                AFECTACION_MODERADA_alguna_vez_box,
                                AFECTACION_SEVERA_alguna_vez_box,
                                words,
                                idx,
                                ["Anorexia/", "Bulimia", "con", "vómito"],
                                min_lookahead=1,
                                max_lookahead=60,
                                )

                # Q15, JOC
                GRAL["Q15"] = determine_afectacion(
                                NO_alguna_vez_sufrido_box,
                                SI_alguna_vez_sufrido_box,
                                AFECTACION_LIGERA_alguna_vez_box,
                                AFECTACION_MODERADA_alguna_vez_box,
                                AFECTACION_SEVERA_alguna_vez_box,
                                words,
                                idx,
                                ["Juego", "patológico", "y", "bruxismo", "diurno"],
                                min_lookahead=1,
                                max_lookahead=60,
                                )

                # Q17, Bdi
                # To be reviewed
                GRAL["Q17_Bdi"] = GRAL["Q15"]

                # Q16, Bso
                GRAL["Q16_Bso"] = determine_afectacion(
                                NO_alguna_vez_sufrido_box,
                                SI_alguna_vez_sufrido_box,
                                AFECTACION_LIGERA_alguna_vez_box,
                                AFECTACION_MODERADA_alguna_vez_box,
                                AFECTACION_SEVERA_alguna_vez_box,
                                words,
                                idx,
                                ["Bruxismo", "nocturno"],
                                min_lookahead=1,
                                max_lookahead=60,
                                )

            if (
                word["content"] == "En"
                and words[idx + 1]["content"] == "el"
                and words[idx + 2]["content"] == "último"
                and words[idx + 3]["content"] == "mes"
                and words[idx + 4]["content"] == "ha"
                and words[idx + 5]["content"] == "sufrido"
                and words[idx + 6]["content"] == "..."
            ):
                # Only the 0 and 2 indexes for these
                NO_ultimo_mes_sufrido_box = words[idx + 7]["boundingBox"]
                SI_ultimo_mes_sufrido_box = words[idx + 8]["boundingBox"]
                # there are '|' in between
                AFECTACION_LIGERA_ultimo_mes_box = words[idx + 9]["boundingBox"]
                AFECTACION_MODERADA_ultimo_mes_box = words[idx + 11]["boundingBox"]
                AFECTACION_SEVERA_ultimo_mes_box = words[idx + 13]["boundingBox"]

                # Q17, GERD
                GRAL["Q17"] = GRAL["Q13"]
                # Q18, TCA
                GRAL["Q17"] = GRAL["Q14"]
                # Q19, JOC
                GRAL["Q17"] = GRAL["Q15"]
                # Q20, Bdo
                GRAL["Q20"] = GRAL["Q16_Bso"]

            # Q21, Entusiasta deporte
            if (
                word["content"] == "Es"
                and words[idx + 1]["content"] == "un"
                and words[idx + 2]["content"] == "entusiasta"
                and words[idx + 3]["content"] == "de"
                and words[idx + 4]["content"] == "la"
                and words[idx + 5]["content"] == "activada"
                and words[idx + 6]["content"] == "física"
                and words[idx + 7]["content"] == "(realiza"
                and words[idx + 8]["content"] == "deporte"
                and words[idx + 9]["content"] == "un"
                and words[idx + 10]["content"] == "mínimo"
                and words[idx + 11]["content"] == "de"
                and words[idx + 12]["content"] == "3"
                and words[idx + 13]["content"] == "veces"
                and words[idx + 14]["content"] == "a"
                and words[idx + 15]["content"] == "la"
                and words[idx + 16]["content"] == "semana)?"
            ):
                print("Entusiasta deporte: ", words[idx + 17]["content"])
                Q21 = words[idx + 17]["content"]

                GRAL["Q21"] = check_yes_no(Q21)
                GRAL["Q21_full_text"] = get_next_words(words, idx + 17, "Es")

            # Q22, Nadador Profesional
            nadador_pro = ["Es","o","ha","sido","nadador/a","profesional","o","ha",
                        "practicado","deportes","acuáticos","frecuentemente?"]
            if words[idx]["content"] == "Es":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(nadador_pro)
                )
                if res:
                    print("Entusiasta deporte: ", words[idx + len(nadador_pro)]["content"])
                    Q22 = words[idx + len(nadador_pro)]["content"]

                    GRAL["Q22"] = check_yes_no(Q22)
                    GRAL["Q22_full_text"] = get_next_words(words, idx + len(nadador_pro), "(indicar")

def read_and_extract_page_three(azure_page_3_json):
    with open(azure_page_3_json) as json_file:
        data = json.load(json_file)

        words = data["words"]
        lines = data["lines"]

        print("Type:", type(data))
        print("Type:", type(words))
        print("Type:", type(lines))

        for idx, word in enumerate(words):
            # print("CONTENT: ", word['content'])

            # Q23, Dormir posicion
            posicion_dormir = ["En","qué","posición","suele","dormir","con","más", "frecuencia?"]
            if words[idx]["content"] == "En":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(posicion_dormir)
                )
                if res:
                    boca_arriba_box = words[idx + len(posicion_dormir)]["boundingBox"]
                    boca_abajo_box = words[idx + len(posicion_dormir) + 1]["boundingBox"]
                    # "Lado"
                    lado_derecho_lado_box = words[idx + len(posicion_dormir) + 2]["boundingBox"]
                    # "derecho"
                    lado_derecho_derecho_box = words[idx + len(posicion_dormir) + 3]["boundingBox"]
                    # "Lado"
                    lado_izquierdo_lado_box = words[idx + len(posicion_dormir) + 4]["boundingBox"]
                    # "izquierdo"
                    lado_izquierdo_izquierda_box = words[idx + len(posicion_dormir) + 5]["boundingBox"]

                    cabeza = words[idx + len(posicion_dormir) + 7]["boundingBox"]
                    cuerpo = words[idx + len(posicion_dormir) + 9]["boundingBox"]
                    
                    if (boca_arriba_box[0] - 20) <= cabeza[0] <= (boca_arriba_box[2] + 20):
                        Q23 = 1
                    elif (boca_abajo_box[0] - 20) <= cabeza[0] <= (boca_abajo_box[2] + 20):
                        Q23 = 2
                    elif (lado_derecho_lado_box[0] - 20) <= cabeza[0] <= (lado_derecho_derecho_box[2] + 20):
                        Q23 = 3
                    elif (lado_izquierdo_lado_box[0] - 20) <= cabeza[0] <= (lado_izquierdo_izquierda_box[2] + 20):
                        Q23 = 4
                    print("Posicion dormir, cabeza: ", Q23)
                    GRAL["Q23_posB"] = Q23

                    if (boca_arriba_box[0] - 20) <= cuerpo[0] <= (boca_arriba_box[2] + 20):
                        GRAL["Q23_posH"] = 1
                    elif (boca_abajo_box[0] - 20) <= cuerpo[0] <= (boca_abajo_box[2] + 20):
                        GRAL["Q23_posH"] = 2
                    elif (lado_derecho_lado_box[0] - 20) <= cuerpo[0] <= (lado_derecho_derecho_box[2] + 20):
                        GRAL["Q23_posH"] = 3
                    elif (lado_izquierdo_lado_box[0] - 20) <= cuerpo[0] <= (lado_izquierdo_izquierda_box[2] + 20):
                        GRAL["Q23_posH"] = 4
                    print("Posicion dormir, cuerpo: ", GRAL["Q23_posH"])

            # Q24, Higiene oral
            cepillar_dientes = ["¿Cuántas","veces","al","día","se","cepilla","los", "dientes?"]
            if words[idx]["content"] == "¿Cuántas":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(cepillar_dientes)
                )
                if res:
                    print("Cuantas veces cepilla dientes: ", words[idx + len(cepillar_dientes)]["content"])
                    GRAL["Q24"] = words[idx + len(cepillar_dientes)]["content"]

            # Q25, Cepillo manual
            cepillo_manual = ["¿Utiliza","cepillo","manual","o","eléctrico?"]
            if words[idx]["content"] == "¿Utiliza":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(cepillo_manual)
                )
                if res:
                    print(" ".join(cepillo_manual), words[idx + len(cepillo_manual)]["content"])
                    Q25 = words[idx + len(cepillo_manual)]["content"]

                    if re.search("manual", Q25, re.IGNORECASE):
                        GRAL["Q25"] = 0
                    elif re.search("ambos", Q25, re.IGNORECASE):
                        GRAL["Q25"] = "0,5"
                    elif re.search("ctrico", Q25, re.IGNORECASE):
                        GRAL["Q25"] = 1

            # Q26, Blandas, medias o duras
            cerdas = ["¿Utiliza","un","cepillo","de","cerdas","blandas,","medias","o","duras?"]
            if words[idx]["content"] == "¿Utiliza":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(cerdas)
                )
                if res:
                    print(" ".join(cerdas), words[idx + len(cerdas)]["content"])
                    Q26 = words[idx + len(cerdas)]["content"]

                    if re.search("blandas", Q26, re.IGNORECASE):
                        GRAL["Q26"] = 0
                    elif re.search("medias", Q26, re.IGNORECASE):
                        GRAL["Q26"] = 1
                    elif re.search("duras", Q26, re.IGNORECASE):
                        GRAL["Q26"] = 2
 
            # Q27, Presion
            GRAL["Q27"] = "CANNOT_MAP_DATA"

            # Q28, Mano cepillar dientes
            GRAL["Q28"] = "CANNOT_MAP_DATA"

            # Q29, Lado masticar
            GRAL["Q29"] = "CANNOT_MAP_DATA"

            # Q30, Que pasta dientes
            GRAL["Q30"] = "CANNOT_MAP_DATA"

            # Q31, Blanqueamiento dientes
            GRAL["Q31"] = "CANNOT_MAP_DATA"

            # Q25, Cepillo manual
            historia_dental = ["Tratamiento","dental:"]
            if words[idx]["content"] == "Tratamiento":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(historia_dental)
                )
                if res:
                    #print(" ".join(historia_dental), words[idx + len(historia_dental)]["content"])
                    NO_box = words[idx + len(historia_dental)]["boundingBox"]
                    SI_box = words[idx + len(historia_dental) + 2]["boundingBox"]

                    conservador = words[idx + len(historia_dental) + 7]["boundingBox"] # box of 'X'
                    conservador_full_text = get_next_words(words, idx + len(historia_dental) + 7, "Ortodóntico") # words in 'Cual:'
                    GRAL["conservador_full_text"] = conservador_full_text

                    # since conservador can have a lot of text, look for the index of the next word
                    ortodontico_idx = lookahead_and_get_index(words, idx, "Ortodóntico")
                    ortodontico = words[ortodontico_idx + 1]["boundingBox"] # box of 'X'
                    ortodontico_full_text = get_next_words(words, ortodontico_idx + 1, "Quirúrgico") # words in 'Cual:'
                    GRAL["ortodontico_full_text"] = ortodontico_full_text

                    quirurjico_idx = lookahead_and_get_index(words, idx, "etc)")
                    quirurjico = words[quirurjico_idx + 1]["boundingBox"] # box of 'X'
                    quirurjico_full_text = get_next_words(words, quirurjico_idx + 1, "Periodontal") # words in 'Cual:'
                    GRAL["quirurjico_full_text"] = quirurjico_full_text

                    periodontal_idx = lookahead_and_get_index(words, idx, "Periodontal")
                    periodontal = words[periodontal_idx + 1]["boundingBox"] # box of 'X'
                    periodontal_full_text = get_next_words(words, periodontal_idx + 1, "Protésico") # words in 'Cual:'
                    GRAL["periodontal_full_text"] = periodontal_full_text

                    protesico_idx = lookahead_and_get_index(words, idx, "Protésico")
                    protesico = words[protesico_idx + 1]["boundingBox"] # box of 'X'
                    try:
                        protesico_full_text = get_next_words(words, protesico_idx + 1, "") # words in 'Cual:'
                        GRAL["protesico_full_text"] = protesico_full_text
                    except IndexError:
                        GRAL["protesico_full_text"] = ""

                    if NO_box[0] - 20 <= conservador[0] <= NO_box[2] + 20:
                        GRAL["conservador"] = 0
                    elif SI_box[0] - 20 <= conservador[0] <= SI_box[2] + 20:
                        GRAL["conservador"] = 1

                    if NO_box[0] - 20 <= ortodontico[0] <= NO_box[2] + 20:
                        GRAL["ortodontico"] = 0
                    elif SI_box[0] - 20 <= ortodontico[0] <= SI_box[2] + 20:
                        GRAL["ortodontico"] = 1

                    if NO_box[0] - 20 <= quirurjico[0] <= NO_box[2] + 20:
                        GRAL["quirurjico"] = 0
                    elif SI_box[0] - 20 <= quirurjico[0] <= SI_box[2] + 20:
                        GRAL["quirurjico"] = 1

                    if NO_box[0] - 20 <= periodontal[0] <= NO_box[2] + 20:
                        GRAL["periodontal"] = 0
                    elif SI_box[0] - 20 <= periodontal[0] <= SI_box[2] + 20:
                        GRAL["periodontal"] = 1

                    if NO_box[0] - 20 <= protesico[0] <= NO_box[2] + 20:
                        GRAL["protesico"] = 0
                    elif SI_box[0] - 20 <= protesico[0] <= SI_box[2] + 20:
                        GRAL["protesico"] = 1                      

def read_and_extract_page_four(azure_page_4_json):
    with open(azure_page_4_json) as json_file:
        data = json.load(json_file)

        words = data["words"]
        lines = data["lines"]

        print("Type:", type(data))
        print("Type:", type(words))
        print("Type:", type(lines))

        # Extract all "X" occurrences in order of appearance and then map them
        # It is easier and faster that trying to match every text.
        bebidas = ["Q33", "Q34", "Q35", "Q36", "Q37", "Q38"]
        x_appearences = []
        for i,x in enumerate(words):
            if words[i]["content"] == "×" or words[i]["content"] == "X" or words[i]["content"] == "x":
                x_appearences.append(words[i]["boundingBox"])
        
        bebidas_with_boxes = dict(zip(bebidas, x_appearences))

        nunca_box = []
        veces_sem_1_2 = []
        veces_sem_3_4 = []
        veces_sem_5_6 = []
        for idx, word in enumerate(words):

            # Q32, Dieta crudivegana
            crudivegana = ["¿Sigue","una","dieta","crudivegana?"]
            if words[idx]["content"] == "¿Sigue":
                res = all(
                    words[idx + index]["content"] == element
                    for index,element in enumerate(crudivegana)
                )
                print(res)
                if res:
                    print(" ".join(crudivegana), words[idx + len(crudivegana)]["content"])
                    Q32 = words[idx + len(crudivegana)]["content"]

                    GRAL["Q32"] = check_yes_no(Q32)


            if words[idx]["content"] == "Nunca":
                nunca_box = words[idx]["boundingBox"]
                veces_sem_1_2 = words[idx + 1]["boundingBox"]
                veces_sem_3_4 = words[idx + 2]["boundingBox"]
                veces_sem_5_6 = words[idx + 4]["boundingBox"]

        for q,x in bebidas_with_boxes.items():
            if nunca_box[0] - 20 <= x[0] <= nunca_box[2] + 20:
                GRAL[q] = 0
            elif veces_sem_1_2[0] - 20 <= x[0] <= veces_sem_1_2[2] + 20:
                GRAL[q] = 1
            elif veces_sem_3_4[0] - 20 <= x[0] <= veces_sem_3_4[2] + 20:
                GRAL[q] = 2
            elif veces_sem_5_6[0] - 20 <= x[0] <= veces_sem_5_6[2] + 20:
                GRAL[q] = 3
            else:
                GRAL[q] = 4

def read_and_extract_page_six(azure_page_6_json):
    with open(azure_page_6_json) as json_file:
        data = json.load(json_file)

        words = data["words"]
        lines = data["lines"]

        print("Type:", type(data))
        print("Type:", type(words))
        print("Type:", type(lines))

        # Extract all "X" occurrences in order of appearance and then map them
        # It is easier and faster that trying to match every text.
        actividades = ["Q39", "Q40", "Q41", "Q42", "Q43", "Q44", "Q45","Q46","Q47","Q48","Q49","Q50","Q51","Q52","Q53","Q54","Q55","Q56","Q57","Q58","Q59"]
        x_appearences = []
        for i,x in enumerate(words):
            # Be in alert of the tiny 'x' which is not 'x' nor 'X'!!
            if words[i]["content"] == "×" or words[i]["content"] == "X" or words[i]["content"] == "x":
                x_appearences.append(words[i]["boundingBox"])
        
        actividades_with_boxes = dict(zip(actividades, x_appearences))

        ninguna_box = []
        less_one = []
        noches_less_one = []
        noches_1_3 = []
        noches_1_3_mes = []
        noches_1_3_number = []
        noches_1_3_semana = []
        noches_4_7 = []
        noches_4_7_semana = []
        for idx, word in enumerate(words):

            if words[idx]["content"] == "Ninguna":
                ninguna_box = words[idx]["boundingBox"]
                less_one = words[idx + 1]["boundingBox"]
                noches_less_one = words[idx + 2]["boundingBox"]
            
            if words[idx]["content"] == "|1-3":
                noches_1_3 = words[idx]["boundingBox"]
                noches_1_3_mes = words[idx + 1]["boundingBox"]

            if words[idx]["content"] == "1-3":
                noches_1_3_number = words[idx]["boundingBox"]
                noches_1_3_semana = words[idx + 1]["boundingBox"]

            if words[idx]["content"] == "4-7":
                noches_4_7 = words[idx]["boundingBox"]
                noches_4_7_semana = words[idx + 1]["boundingBox"]

        for q,x in actividades_with_boxes.items():
            if ninguna_box[0] - 20 <= x[0] <= ninguna_box[2] + 20:
                GRAL[q] = 0
            elif less_one[0] - 20 <= x[0] <= noches_less_one[2] + 20:
                GRAL[q] = 1
            elif noches_1_3[0] - 20 <= x[0] <= noches_1_3_mes[2] + 20:
                GRAL[q] = 2
            elif noches_1_3_number[0] - 20 <= x[0] <= noches_1_3_semana[2] + 20:
                GRAL[q] = 3
            elif noches_4_7[0] - 20 <= x[0] <= noches_4_7_semana[2] + 20:
                GRAL[q] = 4

def read_and_extract_page_seven(azure_page_7_json):
    GRAL_page_7 = {}
    with open(azure_page_7_json) as json_file:
        data = json.load(json_file)

        words = data["words"]

        # Extract all "X" occurrences in order of appearance and then map them
        # It is easier and faster that trying to match every text.
        stress = ["Q60", "Q61", "Q62", "Q63", "Q64", "Q65", "Q66","Q67","Q68","Q69","Q70","Q71","Q72","Q73"]
        x_appearences = []
        for i,x in enumerate(words):
            # Be in alert of the tiny 'x' which is not 'x' nor 'X'!!
            if words[i]["content"] == "×" or words[i]["content"] == "X" or words[i]["content"] == "x":
                x_appearences.append(words[i]["boundingBox"])
        
        actividades_with_boxes = dict(zip(stress, x_appearences))

        nunca_box = []
        casi_nunca = []
        de_vez = []
        en_cuando = []
        a_ = []
        menudo = []
        muy = []
        _a = []
        for idx, word in enumerate(words):

            if words[idx]["content"] == "Nunca":
                nunca_box = words[idx]["boundingBox"]
            
            if words[idx]["content"] == "nunca":
                casi_nunca = words[idx]["boundingBox"]

            if words[idx]["content"] == "De"\
                and words[idx + 1]["content"] == "vez"\
                and words[idx + 2]["content"] == "en":
                # "De"
                de_vez = words[idx]["boundingBox"]
                # "en"
                en_cuando = words[idx + 2]["boundingBox"]

            if words[idx]["content"] == "A"\
                and words[idx + 1]["content"] == "menudo":
                # "A"
                a_ = words[idx]["boundingBox"]
                # "menudo"
                menudo = words[idx + 1]["boundingBox"]

            if words[idx]["content"] == "Muy"\
                and words[idx + 1]["content"] == "a":
                # "menudo"
                muy = words[idx]["boundingBox"]
                _a = words[idx + 1]["boundingBox"]

        for q,x in actividades_with_boxes.items():
            if nunca_box[0] - 20 <= x[0] <= nunca_box[2] + 20:
                GRAL_page_7[q] = 0
            elif casi_nunca[0] - 20 <= x[0] <= casi_nunca[2] + 20:
                GRAL_page_7[q] = 1
            elif de_vez[0] - 20 <= x[0] <= en_cuando[2] + 20:
                GRAL_page_7[q] = 2
            elif a_[0] - 20 <= x[0] <= menudo[2] + 20:
                GRAL_page_7[q] = 3
            elif muy[0] - 50 <= x[0] <= _a[2] + 50: # add more because the box is smaller
                GRAL_page_7[q] = 4

        return GRAL_page_7

GRAL_page_7 = read_and_extract_page_seven(azure_page_7_json)
print(GRAL_page_7)


def get_number_upper_row(numbers_info, number, teeth_box, sextant_n):
    """"L= number"""
    # padding to the teeth box can be changed
    if (numbers_info[number]["box"][7] >= teeth_box[1] - 10\
        or numbers_info[number]["box"][5] >= teeth_box[1] - 10) \
        and (numbers_info[number]["box"][7] <= teeth_box[5] + 10 \
        or numbers_info[number]["box"][5] <= teeth_box[5] + 10) \
        and sextant_n - 103 <= numbers_info[number]["box"][0] <= sextant_n + 103:

        return True
    else:
        return False

def get_number_lower_row(numbers_info, number, teeth_box, sextant_n):
    """"b= number"""
    if (numbers_info[number]["box"][1] <= teeth_box[5] + 10\
        or numbers_info[number]["box"][3] <= teeth_box[5] + 10) \
        and (numbers_info[number]["box"][1] >= teeth_box[1] - 10 \
        or numbers_info[number]["box"][3] >= teeth_box[1] - 10) \
        and sextant_n - 100 <= numbers_info[number]["box"][0] <= sextant_n + 100:

        return True
    else:
        return False

def read_and_extract_page_ten(azure_page_10):
    GRAL_color_dents = {}
    with open(azure_page_10) as json_file:
        data = json.load(json_file)

        words = data["words"]
        lines = data["lines"]

        print("\n PAGE 10 \n")

        numbers_info = {}
        for idx,word in enumerate(words):

            # check in this order:
            # digits with comma or dot, e.g. 78,2 or 73.2
            # L= or L = or b=56,6
            # 83 and previous matches either 'L=' or 'b= '
            # 8314, where 1 is mapped to a comma later
            if re.match("\d+[,./]\d+", words[idx]["content"])\
                or re.match("\w=\d+[,.]", words[idx]["content"])\
                or (re.match("\d{2,}", words[idx]["content"]) and (words[idx-1]["content"] == 'b=' or words[idx-1]["content"] == 'L='))\
                or re.match("'\d{2,}", words[idx]["content"])\
                or re.match("\d{3,}", words[idx]["content"]):

                change_point_for_comma = re.sub("\.", ",", words[idx]["content"])
                remove_words = re.sub("\w+\s*=\s*", "", change_point_for_comma)
                change_slash_for_comma = re.sub("/", ",", remove_words)
                # change 64'7 for 64,7
                change_quote_for_comma = re.sub(r"(\d)(\d)'(\d)", r"\1\2,\3", change_slash_for_comma)
                # change 12% for 12,1
                change_percent_for_comma = re.sub("%", ",1", change_quote_for_comma)
                remove_quote = re.sub("'", "", change_percent_for_comma)
                change_dolla_for_nine = re.sub(",\$", ",9", remove_quote)
                # for example 7725, to 72,5 -> only 1 decimal they have so that's why it can be done
                # avoid the ones that have '1' in thirs place
                change_one_for_comma = re.sub(r"(\d)(\d)1(\d)", r"\1\2,\3", change_dolla_for_nine)
                change_four_digits_for_comma = re.sub(r"(\d)(\d)(\d)(\d)", r"\2\3,\4", change_one_for_comma)
                # change 123 for 12,3
                # see test 6
                change_three_digits_for_comma = re.sub(r"(\d)(\d)(\d)", r"\1\2,\3", change_four_digits_for_comma)

                print(f"original: {words[idx]['content']}", f"filtered: {change_three_digits_for_comma}")

                # better handle duplicated numbers, add '_dup' to key
                # also add confidence and print them red in final excel
                if numbers_info.get(words[idx]["content"]) is not None:
                    numbers_info[f"{words[idx]['content']}_dup_{words[idx]['boundingBox'][0]}"] = {
                        "filtered_number": change_three_digits_for_comma,
                        "box": words[idx]["boundingBox"],
                        "confidence": words[idx]["confidence"],
                        "idx": idx,
                        "previous_letter": words[idx-1]['content'] # lookback for 'L' or 'b'
                    }
                else:
                    numbers_info[words[idx]["content"]] = {
                        "filtered_number": change_three_digits_for_comma,
                        "box": words[idx]["boundingBox"],
                        "confidence": words[idx]["confidence"],
                        "idx": idx,
                        "previous_letter": words[idx-1]['content'] # lookback for 'L' or 'b'
                    }

        print("numbers_info: ", numbers_info)
        print("numbers_info len: ", len(numbers_info.keys()))

        manbibular_idx = 0
        for idx,word in enumerate(words):

            if words[idx]["content"] == "mandibular":
                manbibular_idx = idx
                print("manbibular_idx", manbibular_idx)
                break

        buccal_was_hit = False
        occlusal_was_hit = False
        palatial_was_hit = False
        lingual_was_hit = False
        occlusal_second_time_was_hit = False
        buccal_second_time_was_hit = False
        maxillary_was_hit = False
        sixteen_was_hit = []
        thirteen_was_hit = []
        twenty_three_was_hit = []
        twenty_six_was_hit = []        
        buccal_box = []
        occlusal_box = []
        palatinal_box = []
        lingual_box = []
        occlusal_second_box = []
        buccal_second_box = []
        sixteen_box = []
        thirteen_box = []
        twenty_three_box = []
        twenty_six_box = []
        for idx,word in enumerate(words):

            if words[idx]["content"] == "buccal" and not buccal_was_hit:
                buccal_was_hit = True
                buccal_box = words[idx]["boundingBox"]
                print("Buccal box: ", buccal_box)

            if words[idx]["content"] == "occlusal/incisal" and not occlusal_was_hit:
                occlusal_was_hit = True
                occlusal_box = words[idx]["boundingBox"]
                print("occlusal box: ", occlusal_box)

            if words[idx]["content"] == "palatinal" and not palatial_was_hit:
                palatial_was_hit = True
                palatinal_box = words[idx]["boundingBox"]
                print("palatinal box: ", palatinal_box)

            if words[idx]["content"] == "lingual" and not lingual_was_hit:
                lingual_was_hit = True
                lingual_box = words[idx]["boundingBox"]
                print("lingual box: ", lingual_box)

            if words[idx]["content"] == "occlusal/incisal" \
                and not occlusal_second_time_was_hit and idx > manbibular_idx:
                occlusal_second_time_was_hit = True
                occlusal_second_box = words[idx]["boundingBox"]
                print("occlusal_second_box: ", occlusal_second_box)

            if words[idx]["content"] == "buccal" \
                and not buccal_second_time_was_hit and idx > manbibular_idx:
                buccal_second_time_was_hit = True
                buccal_second_box = words[idx]["boundingBox"]
                print("buccal_second_box: ", buccal_second_box)

            if words[idx]["content"] == "maxillary"\
                and words[idx + 1]["content"] == "teeth" and not maxillary_was_hit:

                maxillary_was_hit = True
                # get the coordinate where 'teeth' box ends (upper right)
                maxillary_teeth = words[idx + 1]["boundingBox"][2]

                maxillary_second_idx = lookahead_and_get_index(words, idx, "maxillary")
                # get the coordinate where second 'maxillary' box starts (upper left)
                maxillary_second_teeth = words[maxillary_second_idx]["boundingBox"][0]

                # ----(x,y)                                               (x,y)----- 
                # teeth|      16      |     13     |     23     |    26     |maxillary                         
                length_of_full_sextant = maxillary_second_teeth - maxillary_teeth
                length_of_number_sextant = length_of_full_sextant / 4

                sixteen_box = int(maxillary_teeth + (length_of_number_sextant / 2)) # to get the middle of '16' box
                thirteen_box = int(sixteen_box + length_of_number_sextant) # to get the middle of '13' box
                twenty_three_box = int(thirteen_box + length_of_number_sextant) # to get the middle of '23' box
                twenty_six_box = int(twenty_three_box + length_of_number_sextant) # to get the middle of '26' box

                print("sixteen_box: ", sixteen_box)
                print("thirteen_box: ", thirteen_box)
                print("twenty_three_box: ", twenty_three_box)
                print("twenty_six_box: ", twenty_six_box)

        # GRAL.update({"C16V-L": None, "C16V-B": None, "C13V-L": None, "C13V-B": None, "C23V-L": None,
        #              "C23V-B": None, "C26V-L": None, "C26V-B": None, "C16O-L": None, "C16O-B": None,
        #              "C26O-L": None, "C26O-B": None, "C16P-L": None, "C16P-B": None, "C13P-L": None,
        #              "C13P-B": None, "C23P-L": None, "C23P-B": None, "C26P-L": None, "C26P-B": None,
        #              "C46P-L": None, "C46P-B": None, "C43P-L": None, "C43P-B": None, "C33P-L": None,
        #              "C33P-B": None, "C36P-L": None, "C36P-B": None, "C46O-L": None, "C46O-B": None,
        #              "C36O-L": None, "C36O-B": None, "C46V-L": None, "C46V-B": None, "C43V-L": None,
        #              "C43V-B": None, "C33V-L": None, "C33V-B": None, "C36V-L": None, "C36V-B": None})
        for number in numbers_info.keys():

            # buccal
            # use the height of the number box vs the word
            # L= number; 76,5 for first sample
            if get_number_upper_row(numbers_info, number, buccal_box, sixteen_box):
                if "C16V-L" not in GRAL_color_dents: GRAL_color_dents["C16V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 26,8
            if get_number_lower_row(numbers_info, number, buccal_box, sixteen_box):
                if "C16V-B" not in GRAL_color_dents: GRAL_color_dents["C16V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 69,9
            if get_number_upper_row(numbers_info, number, buccal_box, thirteen_box):
                if "C13V-L" not in GRAL_color_dents: GRAL_color_dents["C13V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 25,8
            if get_number_lower_row(numbers_info, number, buccal_box, thirteen_box):
                if "C13V-B" not in GRAL_color_dents: GRAL_color_dents["C13V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 74,0
            if get_number_upper_row(numbers_info, number, buccal_box, twenty_three_box):
                if "C23V-L" not in GRAL_color_dents: GRAL_color_dents["C23V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 29,2
            if get_number_lower_row(numbers_info, number, buccal_box, twenty_three_box):
                if "C23V-B" not in GRAL_color_dents: GRAL_color_dents["C23V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 66,8
            if get_number_upper_row(numbers_info, number, buccal_box, twenty_six_box):
                if "C26V-L" not in GRAL_color_dents: GRAL_color_dents["C26V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 20,1
            if get_number_lower_row(numbers_info, number, buccal_box, twenty_six_box):
                if "C26V-B" not in GRAL_color_dents: GRAL_color_dents["C26V-B"] = numbers_info[number]["filtered_number"]; continue

            # occlusal/incisal
            # L= number; 57,0 for first sample
            if get_number_upper_row(numbers_info, number, occlusal_box, sixteen_box):
                if "C16O-L" not in GRAL_color_dents: GRAL_color_dents["C16O-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 7,9
            if get_number_lower_row(numbers_info, number, occlusal_box, sixteen_box):
                if "C16O-B" not in GRAL_color_dents: GRAL_color_dents["C16O-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 62,2
            if get_number_upper_row(numbers_info, number, occlusal_box, twenty_six_box):
                if "C26O-L" not in GRAL_color_dents: GRAL_color_dents["C26O-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 6,9
            if get_number_lower_row(numbers_info, number, occlusal_box, twenty_six_box):
                if "C26O-B" not in GRAL_color_dents: GRAL_color_dents["C26O-B"] = numbers_info[number]["filtered_number"]; continue

            # palatinal
            # L= number; 74,6 for first sample
            if get_number_upper_row(numbers_info, number, palatinal_box, sixteen_box):
                if "C16P-L" not in GRAL_color_dents: GRAL_color_dents["C16P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 20,3
            if get_number_lower_row(numbers_info, number, palatinal_box, sixteen_box):
                if "C16P-B" not in GRAL_color_dents: GRAL_color_dents["C16P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 75,0 (it reads it as 95)
            if get_number_upper_row(numbers_info, number, palatinal_box, thirteen_box):
                if "C13P-L" not in GRAL_color_dents: GRAL_color_dents["C13P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 27,1
            if get_number_lower_row(numbers_info, number, palatinal_box, thirteen_box):
                if "C13P-B" not in GRAL_color_dents: GRAL_color_dents["C13P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 74,9 (it reads it as 94,9)
            if get_number_upper_row(numbers_info, number, palatinal_box, twenty_three_box):
                if "C23P-L" not in GRAL_color_dents: GRAL_color_dents["C23P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 26,6
            if get_number_lower_row(numbers_info, number, palatinal_box, twenty_three_box):
                if "C23P-B" not in GRAL_color_dents: GRAL_color_dents["C23P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 68,0
            if get_number_upper_row(numbers_info, number, palatinal_box, twenty_six_box):
                print(get_number_upper_row(numbers_info, number, palatinal_box, twenty_six_box), numbers_info[number]["filtered_number"])
                if "C26P-L" not in GRAL_color_dents: GRAL_color_dents["C26P-L"] = numbers_info[number]["filtered_number"]; continue
                #exit()
            # b= number; 15,1
            if get_number_lower_row(numbers_info, number, palatinal_box, twenty_six_box):
                if "C26P-B" not in GRAL_color_dents: GRAL_color_dents["C26P-B"] = numbers_info[number]["filtered_number"]; continue

            # lingual
            # L= number; 77,3 for first sample
            if get_number_upper_row(numbers_info, number, lingual_box, sixteen_box):
                if "C46P-L" not in GRAL_color_dents: GRAL_color_dents["C46P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 18,7
            if get_number_lower_row(numbers_info, number, lingual_box, sixteen_box):
                if "C46P-B" not in GRAL_color_dents: GRAL_color_dents["C46P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 63,2
            if get_number_upper_row(numbers_info, number, lingual_box, thirteen_box):
                if "C43P-L" not in GRAL_color_dents: GRAL_color_dents["C43P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 22,3
            if get_number_lower_row(numbers_info, number, lingual_box, thirteen_box):
                if "C43P-B" not in GRAL_color_dents: GRAL_color_dents["C43P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 63,1
            if get_number_upper_row(numbers_info, number, lingual_box, twenty_three_box):
                if "C33P-L" not in GRAL_color_dents: GRAL_color_dents["C33P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 19,9
            if get_number_lower_row(numbers_info, number, lingual_box, twenty_three_box):
                if "C33P-B" not in GRAL_color_dents: GRAL_color_dents["C33P-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 65,4
            if get_number_upper_row(numbers_info, number, lingual_box, twenty_six_box):
                if "C36P-L" not in GRAL_color_dents: GRAL_color_dents["C36P-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 17,0
            if get_number_lower_row(numbers_info, number, lingual_box, twenty_six_box):
                if "C36P-B" not in GRAL_color_dents: GRAL_color_dents["C36P-B"] = numbers_info[number]["filtered_number"]; continue

            # occlusal/incisal second part
            # L= number; 65,5 for first sample
            if get_number_upper_row(numbers_info, number, occlusal_second_box, sixteen_box):
                if "C46O-L" not in GRAL_color_dents: GRAL_color_dents["C46O-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 8,7
            if get_number_lower_row(numbers_info, number, occlusal_second_box, sixteen_box):
                if "C46O-B" not in GRAL_color_dents: GRAL_color_dents["C46O-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 60,6
            if get_number_upper_row(numbers_info, number, occlusal_second_box, twenty_six_box):
                if "C36O-L" not in GRAL_color_dents: GRAL_color_dents["C36O-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 10,6
            if get_number_lower_row(numbers_info, number, occlusal_second_box, twenty_six_box):
                if "C36O-B" not in GRAL_color_dents: GRAL_color_dents["C36O-B"] = numbers_info[number]["filtered_number"]; continue

            # buccal second part
            # L= number; 82,3 for first sample
            if get_number_upper_row(numbers_info, number, buccal_second_box, sixteen_box):
                if "C46V-L" not in GRAL_color_dents: GRAL_color_dents["C46V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 23,0
            if get_number_lower_row(numbers_info, number, buccal_second_box, sixteen_box):
                if "C46V-B" not in GRAL_color_dents: GRAL_color_dents["C46V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 79,8
            if get_number_upper_row(numbers_info, number, buccal_second_box, thirteen_box):
                if "C43V-L" not in GRAL_color_dents: GRAL_color_dents["C43V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 27,8
            if get_number_lower_row(numbers_info, number, buccal_second_box, thirteen_box):
                if "C43V-B" not in GRAL_color_dents: GRAL_color_dents["C43V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 80,6
            if get_number_upper_row(numbers_info, number, buccal_second_box, twenty_three_box):
                if "C33V-L" not in GRAL_color_dents: GRAL_color_dents["C33V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 28,1
            if get_number_lower_row(numbers_info, number, buccal_second_box, twenty_three_box):
                if "C33V-B" not in GRAL_color_dents: GRAL_color_dents["C33V-B"] = numbers_info[number]["filtered_number"]; continue
            # L= number; 75,8
            if get_number_upper_row(numbers_info, number, buccal_second_box, twenty_six_box):
                if "C36V-L" not in GRAL_color_dents: GRAL_color_dents["C36V-L"] = numbers_info[number]["filtered_number"]; continue
            # b= number; 20,6
            if get_number_lower_row(numbers_info, number, buccal_second_box, twenty_six_box):
                if "C36V-B" not in GRAL_color_dents: GRAL_color_dents["C36V-B"] = numbers_info[number]["filtered_number"]; continue

        return GRAL_color_dents

#read_and_extract_page_two(azure_vision_json)
#read_and_extract_page_three(azure_page_3_json)
#read_and_extract_page_four(azure_page_4_json)
#read_and_extract_page_six(azure_page_6_json)

# PAGE 10
# azure_page_10_test_4 = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_10/pg_0007.json"

# GRAL_returned = read_and_extract_page_ten(azure_page_10_test_4)


# print("GRAL_returned: ", GRAL_returned)
# print("GRAL length: ", len(GRAL_returned.keys())-1) # remove the N

# # (\d+[,.]\d+) -> "$1",
# # (\d+)\s      -> "$1",
# # \s+          -> nothing
# Cs = ["C16V-L","C16V-B","C16O-L","C16O-B","C16P-L","C16P-B","C13V-L","C13V-B","C13P-L","C13P-B","C23V-L","C23V-B","C23P-L","C23P-B","C26V-L","C26V-B","C26O-L","C26O-B","C26P-L","C26P-B","C36P-L","C36P-B","C36O-L","C36O-B","C36V-L","C36V-B","C33P-L","C33P-B","C33V-L","C33V-B","C43P-L","C43P-B","C43V-L","C43V-B","C46P-L","C46P-B","C46O-L","C46O-B","C46V-L","C46V-B"]

# # first sample
# #Ns = ["76,5","26,8","57","7,9","74,6","20,3","69,9","25,8","75","27,1","24","29,2","74,9","26,6","66,8","20,1","62,2","6,9","68","15,1","65,4","17","60,6","10,6","75,8","20,6","63,1","19,9","80,6","28,1","63,2","22,3","79,8","27,8","77,3","18,7","65,5","8,7","82,3","23"]

# # test 6
# Ns=["64,9","17,8","58,4","16,6","72,2","27,1","72,5","29,5","62,7","24,9","74,7","31,1","70,2","32,2","64,7","16,6","62,7","12,1","76,1","36,7","56,6","21,8","68,4","15,5","74","24,4","70,8","16,2","81,5","33,4","69,9","17,7","81,4","30,6","63,1","17,2","66,5","16,8","80,6","25,5"]

# page_test_dict = dict(zip(Cs, Ns))

# for c in Cs:

#     if c in GRAL_returned:
#         print("Column: ", c, "\t", "Ona version: ", page_test_dict[c], "\t", "AI version: ", GRAL_returned[c])
#     else:
#         print("Could not find: ", c)