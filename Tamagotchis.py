"""
    --Monika Sawicka s1097259 bin 2c--
    -- 29.01.2017--
"""

from os import path
import io
import random
import datetime


def datum():
    """
    Deze functie slaat de huidige datum op in een variable.
    :return: date
    """
    date = datetime.date.today()
    return date


def file_controleren(path_to_check):
    """
    Deze functie controleert of het bestand bestaat.
    :param path_to_check: bestands path en naam
    :return tuple
    """
    if not path.isfile(path_to_check):
        return False, 'Het bestand \'{}\' bestaat niet. Download ' \
                      'het bestand en probeer het openieuw.\n' \
                      'Het spel wordt afgesloten.' \
            .format(path_to_check)
    return True, ''


def voeding_bestand_inlezen():
    """
    Deze functie leest het voeding bestand tot een dictionary.
    :return: dictionary
    """
    voeding_dict = {}
    with open("voeding.txt", 'r') as f:
        for line in f:
            items = line.strip('\n').split(':')
            key, values = items[0], items[1]
            voeding_dict[key] = values
    return voeding_dict


def plaatjes_bestand_inlezen():
    """
    Deze functie leest het bestand met tamagotchi plaatjes tot een
    lijst.
    :return: lijst
    """
    plaatjes_lijst = []
    with io.open("pet_pictures.txt", encoding='utf-8') as f:
        for line in f:
            items = line.split(';')
            items.remove(items[0])
            plaatjes_lijst.append(items)
    return plaatjes_lijst


def input_voeding_controleren(voeding, voeding_dict):
    """
    Deze functie controleert of ingevoerde voedings naam nog niet in de
    bestaande voedings lijst is en haalt alle vreemde tekens van het
    woord uit.
    :param voeding: ingevoerde woord
    :param voeding_dict: dictionary met alle bestaande voeding namen
    :return tuple: melding: bericht dat gebruiker krijgt van het
    programma, waarde: markeert voeding met o of g, v_woord: aangepaste
    woord.
    """
    v_woord = ''
    for letter in voeding:
        if letter.isalpha():
            v_woord += letter
    if v_woord in voeding_dict:
        melding = "Deze voeding soort komt al voor in de lijst.\n"
        return melding, '', ''
    elif len(v_woord) < 3 or len(v_woord) > 38:
        melding = ("\nUw woord is: " + v_woord + ". \nDeze woord niet "
                                                 "toegevoegd tot het "
                                                 "lijst.\nHet woord moet "
                                                 "langer dan 3 en korter "
                                                 "dan 38 letters zijn.\n")
        return melding, '', ''
    else:
        v_woord = v_woord
        waarde = input_waarde_controleren()
        return '', waarde, v_woord


def input_waarde_controleren():
    """
    Deze functie controleert of ingevoerde voeding waarte is correct.
    :return: voeding waarde
    """
    herhalen = True
    waarde = str(input('\nIs deze voeding gezond (g) '
                       'of ongezond (o)?'))
    while herhalen:
        if waarde != "g" and waarde != "o":
            waarde = str(input(
                "\nIs deze voeding gezond (g) of "
                "ongezond (o)?"))
        else:
            return waarde


def voeding_toevoegen(voeding, voeding_dict, waarde):
    """
    Deze functie controleert of ingevoerde voeding en zijn waarde al te
    vinden zijn in bestaande voeding dictionary. Als niet wordt de
    voeding als een key tot dictionary toegevoed en waarde als zijn
    value.
    :param voeding: ingevorde voeding naam
    :param voeding_dict: voeding dictionary
    :param waarde: ingevoerde voeding waarde
    :return: string - bericht voor de gebruiker
    """
    if voeding not in voeding_dict:
        voeding_dict[voeding] = waarde
        voeding_lijst = []
        for a in voeding_dict:
            voeding_lijst.append(a + ':' + voeding_dict[a])
        voeding_lijst.sort(key=lambda x: (len(x), x))
        w_file = open('voeding.txt', 'w')
        w_file.write('\n'.join(voeding_lijst))
        w_file.close()
        melding = ('Het voeding soort ' + voeding + ' is toegevoegd tot het '
                                                    'voeding lijst.')
        return melding
    else:
        melding = 'Dit woord komt al voor in deze lijst.'
        return melding


def leeftijden(beurt):
    """
    Deze functie bepaald een waarde, die later gebruikt wordt in het
    keuze van de plaatjes.
    :param beurt: beurt nr
    :return: integer
    """
    if beurt in range(0, 7):
        return 0
    elif beurt in range(7, 14):
        return 6
    elif beurt in range(14, 21):
        return 12
    elif beurt in range(21, 25):
        return 17


def volwassen(v_totaal, v_plaatjes):
    """
    Deze functie bepaald welke plaatje moet worden gebruikt als
    Tamagotchi volwassen wordt.
    :param v_totaal: totale waarde van alle statussen
    :param v_plaatjes: lijst van lijsten met Tamagotchi plaatjes
    :return: lijst van gekozen plaatje
    """
    if v_totaal in range(0, 6):
        return v_plaatjes[25]
    if v_totaal in range(6, 10):
        return v_plaatjes[26]
    if v_totaal in range(10, 14):
        return v_plaatjes[27]
    if v_totaal in range(14, 18):
        return v_plaatjes[28]
    if v_totaal > 17:
        return v_plaatjes[29]


def plaatje_kiezen(p_beurt, p_honger, p_afval, p_geluk, p_plaatjes,
                   p_totaal, p_ranking_lijst, p_speller_naam, p_taam_naam,
                   p_kopje, p_bericht, p_leeftijd):
    """
    Deze functie
    :param p_leeftijd: leeftijd waarde voor plaatjes
    :param p_beurt: aantal beurten
    :param p_honger: aantal honger punten
    :param p_afval: aantal afval punten
    :param p_geluk: aantal geluk punten
    :param p_plaatjes: lijst van plaatjes lijsten
    :param p_totaal: totaal van alle statussen
    :param p_ranking_lijst: ranking lijst uit het bestand
    :param p_speller_naam: speler naam
    :param p_taam_naam: tamagotchi naam
    :param p_kopje: eerste rij van het ranking uit het bestand
    :param p_bericht: melding om te weergeven
    :return: string met het lay out van het scherm met updated waardes
    en plaatje, boolean, afhankelijk van het staats - lege string of
    ranking melding, afhankelijk van het staats - lege string of
    updated ranking string
    """
    if p_totaal < 6 and p_beurt < 25:
        return plaatjes_layout(p_beurt, p_afval, p_geluk,
                               p_taam_naam, p_honger, p_bericht,
                               p_plaatjes[1 + p_leeftijd]), True, '', ''
    elif p_totaal in range(6, 10) and p_beurt < 25:
        return plaatjes_layout(p_beurt, p_afval, p_geluk,
                               p_taam_naam, p_honger, p_bericht,
                               p_plaatjes[2 + p_leeftijd]), True, '', ''
    elif p_totaal in range(10, 14) and p_honger < 13 and p_afval < 13 and \
                    p_geluk < 12 and p_beurt < 25:
        return plaatjes_layout(p_beurt, p_afval, p_geluk,
                               p_taam_naam, p_honger, p_bericht,
                               p_plaatjes[3 + p_leeftijd]), True, '', ''
    elif p_totaal in range(14, 18) and p_honger < 13 and p_afval < 13 and \
                    p_geluk < 13 and p_beurt < 25:
        return plaatjes_layout(p_beurt, p_afval, p_geluk,
                               p_taam_naam, p_honger, p_bericht,
                               p_plaatjes[4 + p_leeftijd]), True, '', ''
    elif p_totaal > 17 and p_honger < 13 and p_afval < 13 and \
                    p_geluk < 13 and p_beurt < 25:
        return plaatjes_layout(p_beurt, p_afval, p_geluk,
                               p_taam_naam, p_honger, p_bericht,
                               p_plaatjes[5 + p_leeftijd]), True, '', ''
    else:
        scherm, spelen, ranking_bericht, rank = game_over(p_honger,
                                                          p_ranking_lijst,
                                                          p_speller_naam,
                                                          p_taam_naam,
                                                          p_beurt, p_totaal,
                                                          p_afval, p_geluk,
                                                          p_plaatjes,
                                                          p_leeftijd, p_kopje)
        return scherm, spelen, ranking_bericht, rank


def game_over(g_honger, g_ranking_lijst, g_speller_naam, g_t_naam,
              g_beurt, g_totaal, g_afval, g_geluk, g_plaatjes,
              g_leeftijd, g_kopje):
    """
    Deze functie bepaald welke plaatje woord getoond in het gevaal
    van te gohe statussen en eindingt het spel.
    :param g_honger:  honger punten
    :param g_ranking_lijst: ranking lijst uit de bedstand
    :param g_speller_naam: speler naam
    :param g_t_naam: Tamagotchi naam
    :param g_beurt: aantal beurten
    :param g_totaal: totaal alle statussen
    :param g_afval: aantal afval punten
    :param g_geluk: aantal geluk punten
    :param g_plaatjes: lijst van plaatjes lijsten
    :param g_leeftijd: leeftijd waarde
    :param g_kopje: eerste regel van ranking bestand
    :return: string voor het scherm layout, boolean, string met
    melding voor de gebruiker,string met updated ranking layout
    """
    if g_honger >= 13:
        rank_voor_wegschrijven, rank_bericht = ranking_vullen(
            g_ranking_lijst, g_speller_naam,
            g_t_naam,
            g_beurt, g_totaal)
        ranking_wegschrijven(rank_voor_wegschrijven, g_kopje)
        scherm = plaatjes_layout(g_beurt, g_afval, g_geluk,
                                 g_t_naam, g_honger,
                                 'Je moet de Tamagotchi wel eten geven...',
                                 g_plaatjes[6 + g_leeftijd])
        rank = ranking_layout()
        return scherm, False, rank_bericht, rank
    elif g_afval >= 13:
        rank_voor_wegschrijven, rank_bericht = ranking_vullen(
            g_ranking_lijst, g_speller_naam,
            g_t_naam,
            g_beurt, g_totaal)
        ranking_wegschrijven(rank_voor_wegschrijven, g_kopje)
        scherm = plaatjes_layout(g_beurt, g_afval, g_geluk,
                                 g_t_naam, g_honger, 'Ik ga weg, '
                                                     'er is teveel rommel!',
                                 g_plaatjes[30])
        rank = ranking_layout()
        return scherm, False, rank_bericht, rank
    elif g_geluk >= 13:
        rank_voor_wegschrijven, rank_bericht = ranking_vullen(
            g_ranking_lijst, g_speller_naam,
            g_t_naam,
            g_beurt, g_totaal)
        ranking_wegschrijven(rank_voor_wegschrijven, g_kopje)
        scherm = plaatjes_layout(g_beurt, g_afval, g_geluk,
                                 g_t_naam, g_honger, 'Varwel, ik heb er meer'
                                                     ' van verwacht!',
                                 g_plaatjes[30])
        rank = ranking_layout()
        return scherm, False, rank_bericht, rank
    elif g_beurt == 25:
        rank_voor_wegschrijven, rank_bericht = ranking_vullen(
            g_ranking_lijst, g_speller_naam,
            g_t_naam,
            g_beurt, g_totaal)
        ranking_wegschrijven(rank_voor_wegschrijven, g_kopje)
        plaatje = volwassen(g_totaal, g_plaatjes)
        scherm = plaatjes_layout(g_beurt, g_afval, g_geluk,
                                 g_t_naam, g_honger,
                                 '{}{}{}'.format('Hoera ', g_t_naam,
                                                 ' is volwassen!'), plaatje)
        rank = ranking_layout()
        return scherm, False, rank_bericht, rank


def padding(woord, lengte):
    """
    Deze functie plakt spaties aan de strings zodat ze verwachte lengte
    hebben.
    :param woord: string om aan te passen
    :param lengte: vewarchtte lengte
    :return:
    """
    return woord + (' ' * (lengte - len(woord)))


def plaatjes_layout(beurt, afval, ongelukkig, naam, honger,
                    bericht, plaatje):
    """
    Deze functie maakt en update string voor het lay out van het spel
    scherm.
    :param beurt: aantal beurten
    :param afval: aantal afval punnten
    :param ongelukkig: aantal geluk punnten
    :param naam: Tamagotchi naam
    :param honger: aantal honger punnten
    :param bericht: string met melding voor het gebruiker
    :param plaatje: lijst van plaatje
    :return: string met updated layout
    """
    space = 20 * '\n'
    naam = padding("Naam:       " + naam, 20)
    beurtje = padding('Leeftijd:   ' + str(beurt), 20)
    afval = padding("Afval:      " + (afval * '*'), 20)
    hongerig = padding("Hongerig:   " + (honger * '*'), 20)
    ongelukkig = padding("Ongelukkig: " + (ongelukkig * ('*')), 20)
    scherm = "{}\n" \
             "{:^70}\n" \
             "{}\n" \
             "{}{}{}\n" \
             "{}{}{}\n" \
             "{}{}{}\n" \
             "{}\n" \
             "{:^69}\n" \
             "{:^69}\n" \
             "{:^79}\n" \
             "{:^69}\n".format(
        space,
        bericht,
        naam,
        beurtje, " " * (60 - (len(beurtje) + len(plaatje[0]))),
        padding(plaatje[0], 20),
        afval, " " * (60 - (len(afval) + len(plaatje[0]))),
        padding(plaatje[1], 20),
        hongerig, " " * (60 - (len(hongerig) + len(plaatje[0]))),
        padding(plaatje[2], 20),
        ongelukkig,
        "1. Geef eten",
        "2. Verschoon",
        "3. Speel een spelletje",
        "4. Afsluiten")

    return scherm


def voeding_lijsten(voeding):
    """
    Deze functie doorzoekt het voeding dictionary aan de hand van de
    waarde van de voeding en voegt gezonde en ongezonde voeding tot
    behorende lijsten.
    :param voeding: voeding dictionary
    :return: lijsten voor gezonde van strings voor ongezonde voeding
    """
    gezond = []
    ongezond = []
    for eten in voeding:
        if voeding[eten] == 'g':
            gezond.append(eten)
        else:
            ongezond.append(eten)
    return gezond, ongezond


def eten_kiezen(voeding, naam):
    """
    Deze functie kiest random gezonde en ongezonde voeding items en
    heeft gebruiker de keuze.
    :param voeding: voeding dictionary
    :param naam: Tamagotchi naam
    :return: string voor input
    """

    gezond, ongezond = voeding_lijsten(voeding)
    opties = "Wat geef je " + naam + " te eten?\n1." + \
             random.choice(gezond) + "\n2." + random.choice(ongezond) + \
             "\n3.Niks.\n\nMaak een keuze:\n"
    return opties


def gezond_eten_geven(afval, ongelukkig, honger):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor gezonde eten. Statusen woorden
    updated afhankelijk van huidige staat.
    :param afval: aantal afval punten
    :param ongelukkig: aantal geluks punten
    :param honger: aantal honger punten
    :return: updatetd status van honger, afval, geluk, string voor
    het melding
    """
    if honger < 13 and afval < 13 and ongelukkig < 13 and honger \
            > 0:
        honger -= 2
        if honger < 0:
            honger = 0
        afval += 1
        ongelukkig = ongelukkig
        return honger, afval, ongelukkig, 'Nomnom'
    elif honger < 13 and afval < 13 and ongelukkig < 13 \
            and honger < 1:
        honger = 0
        ongelukkig += 1
        afval = afval
        return honger, afval, ongelukkig, 'Ik heb geen honger!'


def ongezond_eten_geven(afval, ongelukkig, honger):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor ongezonde eten. Statusen woorden
    updated afhankelijk van huidige staat.
    :param afval: aantal afval punten
    :param ongelukkig: aantal geluks punten
    :param honger: aantal honger punten
    :return: updatetd status van honger, afval, geluk, string voor
    het melding
    """
    if honger < 13 and afval < 13 and ongelukkig < 13 and honger \
            > 0:
        honger -= 1
        if honger < 0:
            honger = 0
        afval += 3
        ongelukkig -= 1
        if ongelukkig < 0:
            ongelukkig = 0
        return honger, afval, ongelukkig, 'Nomnomnom!'
    elif honger < 13 and honger < 1 and afval < 13 and ongelukkig < \
            13:
        honger = 0
        ongelukkig += 1
        afval = afval
        return honger, afval, ongelukkig, 'Ik heb geen honger!'


def geen_eten_geven(afval, ongelukkig, honger):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor geen eten geven. Statusen woorden
    updated afhankelijk van huidige staat.
    :param afval: aantal afval punten
    :param ongelukkig: aantal geluks punten
    :param honger: aantal honger punten
    :return: updatetd status van honger, afval, geluk, string voor
    het melding
    """
    if honger < 13 and afval < 13 and ongelukkig < 13 and honger \
            > 0:
        honger += 1
        afval = afval
        ongelukkig += 1
        return honger, afval, ongelukkig, 'Maar ik heb honger!'

    elif honger < 13 and afval < 13 and ongelukkig < 13 \
            and honger < 1:
        honger += 1
        ongelukkig += 0
        afval = afval
        return honger, afval, ongelukkig, 'Ik krijg hier wel trek ' \
                                          'van!'


def verschonen(afval, ongelukkig, honger):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor verschonen van Tamagotchi. Statusen
    woorden
    updated afhankelijk van huidige staat.
    :param afval: aantal afval punten
    :param ongelukkig: aantal geluks punten
    :param honger: aantal honger punten
    :return: updatetd status van honger, afval, geluk, string voor
    het melding
    """
    if honger < 13 and afval < 13 and ongelukkig < 13 and afval \
            > 0:
        honger += 1
        afval -= 2
        if afval < 0:
            afval = 0
        ongelukkig += 1
        return honger, afval, ongelukkig, 'Fris en fruitig!'
    elif honger < 13 and afval < 13 and ongelukkig < 13 and afval \
            < 1:
        honger += 1
        afval = afval
        ongelukkig += 2
        return honger, afval, ongelukkig, 'Grmpf, het is al schoon!'


def kop_of_munt(km_input, honger, ongelukkig, t_naam, naam):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor spelen met Tamagotchi in 'Kop of
    munt'. Statusen woorden updated afhankelijk van huidige staat.
    :param km_input: keuze van gebruiker voor kop of munt
    :param honger: aantal honger punten
    :param ongelukkig: aantal geluks punten
    :param t_naam: Tamagotchi naam
    :param naam: speler naam
    :return: updatetd status van honger, geluk, string voor het melding
    """
    penny = ['kop', 'munt']
    side = random.choice(penny)
    if penny[int(km_input) - 1] != side:
        honger += 1
        ongelukkig -= 2
        if ongelukkig < 0:
            ongelukkig = 0
        return honger, ongelukkig, 'Uitslag: ' + side.capitalize() + '. ' + \
               t_naam.capitalize() + ' heeft gewonnen!'
    else:
        honger += 1
        ongelukkig += 2
        return honger, ongelukkig, 'Uitslag: ' + side.capitalize() + '. ' + \
               naam.capitalize() + ' heeft gewonnen!'


def steen_schaar_papier(ssp_keuze, honger, geluk, afval):
    """
    Deze functie update eten, honger en geluk statussen in het geval
    van het gebruiker's keuze voor spelen met Tamagotchi in 'Steen,
    schaar of papier'. Statusen woorden updated afhankelijk van huidige
    staat.
    :param ssp_keuze: keuze van gebruiker tussen steen, papier en schaar
    :param honger: aantal honger punten
    :param geluk: aantal geluks punten
    :param afval: aantal afval punten
    :return: updatetd status van honger, afval, geluk, string voor
    het melding
    """
    ssp = ['steen', 'papier', 'schaar']
    tref = random.choice(ssp)
    if ssp[int(ssp_keuze) - 1] == tref:
        return honger, afval, geluk, 'Gelijkspel, allebei ' + tref + '.'
    elif (tref == 'steen' and ssp[int(ssp_keuze) - 1] == 'papier') \
            or (tref == 'schaar' and ssp[int(ssp_keuze) - 1] == 'steen') \
            or (tref == 'papier' and ssp[int(ssp_keuze) - 1] == 'schaar'):

        return honger + 1, afval + 1, geluk + 2, 'Jij wint, ' + ssp[int(
            ssp_keuze) - 1] + ' verslaat ' + tref + '.'
    else:
        geluk -= 2
        if geluk < 1:
            geluk = 0
        return honger + 1, afval + 1, geluk, 'Jij verliest, ' \
                                             '' + tref + ' ' \
                                                         'verslaat ' + \
               ssp[int(ssp_keuze) - 1] + '.'


def punten_tellen(p_beurten, p_totaal_staat):
    """
    Deze functie berekent de score voor de ranking.
    :param p_beurten: aantal beurten
    :param p_totaal_staat: cumulatieve staat
    :return: eindscore
    """
    p_totaal_score = 0
    p_totaal_score += p_totaal_staat
    p_eindscore = (900 - p_totaal_score) * p_beurten
    return p_eindscore


def rankinglijst_maken():
    """
    Deze Functie leest een ranking file tot de lijst.
    :return: ranking lijst
    """
    ranking_file = open('ranking.txt', 'r')
    lijst_ranking = []
    inhoud_bestand = ranking_file.read().splitlines()
    for rij in inhoud_bestand:
        lijst_ranking.append(rij.split(';'))
    ranking_file.close()
    return lijst_ranking


def ranking_vullen(r_leeg_lijst, r_speller_naam,
                   r_taam_naam,
                   r_beurten, r_totaal_staat):
    """
    Deze functie maakt een lijst met nieuwe scores en voegt het aan
    de bestande rankinglijst. Vervolgens sorteert rankinglijst en
    bepaalt of nieuwe scores in de ranking komen.
    :param r_leeg_lijst: rankinglijst van de bestand
    :param r_speller_naam: speler naam
    :param r_taam_naam: Tamagotchi naam
    :param r_beurten: aantal beurten
    :param r_totaal_staat: cumulatieve staat
    :return: updated rankinglijst, string met melding voor de gebruiker
    """
    r_punten = punten_tellen(r_beurten,
                             r_totaal_staat)
    r_datum = datum()
    r_leeg_lijst.append(['', str(r_datum), str(r_speller_naam),
                         str(r_taam_naam),
                         str(r_beurten), str(r_punten)])
    r_leeg_lijst.sort(key=lambda itemrij: int(itemrij[5]),
                      reverse=True)
    positie = 1
    for item, value in enumerate(r_leeg_lijst):
        r_leeg_lijst[item][0] = str(positie)
        positie += 1
    r_lijst = r_leeg_lijst[0:10]
    # lijst_positie, item_positie = positie_vinden(r_lijst, r_punten)
    r_bericht = ''
    # rank_positie = r_lijst[lijst_positie][0]
    if r_punten <= int(r_lijst[9][5]):
        #   rank_positie = r_lijst[lijst_positie][0]
        r_bericht = 'Eindscore: ' + str(r_punten) + '\nHelaas, ' \
                                                    'jouw ' \
                                                    'score is niet hoog ' \
                                                    'genoeg voor de ' \
                                                    'ranglijst.\n\n'

        r_bericht = 'Eindscore: ' + str(r_punten)  # + '\nDaarmee kom je op
        # positie ' + str(rank_positie) + ' in de ranking.\n\n'

    return r_lijst, r_bericht


def positie_vinden(pv_lijst, pv_punten):
    """
    Deze haalt het positie van de speler uit de raninglijst
    :param pv_lijst: updated rankinglijst
    :param pv_punten: gescoorde punten
    :return: lijst index
    """
    for i, lst in enumerate(pv_lijst):
        for j, positie in enumerate(lst):
            if positie == str(pv_punten):
                return i, j


def ranking_wegschrijven(r_ranking, r_kopje):
    """
    Functiebeschrijving: Deze Functie schrijf een rankinglijst tot een
    file.
    :param r_kopje: eerste regel uit het ranking file
    :param r_ranking: lijst met ranking
    """
    file = open('ranking.txt', 'w')

    r_schrijfbaar = []

    for item in r_ranking:
        r_schrijfbaar.append(';'.join(item))

    r_schrijfbaar.insert(0, ';'.join(r_kopje))

    file.write('\n'.join(r_schrijfbaar))
    file.close()


def ranking_layout():
    """
    Functiebeschrijving: Deze Functie opent een ranking file, schrijft het
    file tot de lijst, vervolgens converteert het lijst tot een string in
    aangegeven format.
    :return: string met ranking
    """
    r_ranking = open('ranking.txt', 'r')
    lijst_ranking = []
    inhoud_bestand = r_ranking.read().splitlines()
    for rij in inhoud_bestand:
        lijst_ranking.append(rij.split(';'))
    r_ranking.close()
    print(lijst_ranking)
    teller = 0
    r_ranking_string = ''
    for rij in lijst_ranking:
        r_ranking_string += '{:<10}{:<20}{:<10}{:<10}{:<10}{:<15}\n'.format(
            [rij[0], teller][teller > 0], rij[1], rij[2], rij[3], rij[4],
            rij[5])
        teller += 1
    return r_ranking_string


def main():
    if not file_controleren('voeding.txt')[0]:
        print(file_controleren('voeding.txt')[1])
        exit()

    if not file_controleren('ranking.txt')[0]:
        print(file_controleren('ranking.txt')[1])
        exit()
    if not file_controleren('pet_pictures.txt')[0]:
        print(file_controleren('pet_pictures.txt')[1])
        exit()
    dict_voeding = voeding_bestand_inlezen()
    ranking_lijst = rankinglijst_maken()
    kopje = ranking_lijst[0]
    leeg_ranking = ranking_lijst[1:]
    plaatjes = plaatjes_bestand_inlezen()
    speler_naam = str(input("Wat is je naam? "))
    naam_check = False
    while not naam_check:
        if len(speler_naam) < 1:
            speler_naam = str(input("Wat is je naam? ")).lower()
        elif not speler_naam.isalpha():
            speler_naam = str(input("Wat is je naam? ")).lower()
        else:
            print("Welkom " + speler_naam + "!!\n")
            naam_check = True
    menu_eind = False
    while not menu_eind:
        main_keuze = str(input("Wat wil je doen?\n"
                               "1. Voeding toevoegen\n"
                               "2. Tamagotchi spelen\n"
                               "3. De ranking bekijken\n"
                               "4. Afsluiten\n\nMaak een keuze: \n"))
        if main_keuze.isdigit() and (main_keuze == "1"):
            input_voeding = str(input("\nVoer voedeing in (voorbeeld:"
                                      " wortel, snikers.spitskool, "
                                      "etc.)"
                                      ": "))
            melding, waarde, voeding = input_voeding_controleren(
                input_voeding,
                dict_voeding)
            print(melding)

            voeding_toevoegen(voeding, dict_voeding, waarde)

        elif main_keuze.isdigit() and main_keuze == "2":
            t_naam = str(input('Hoera, er is een nieuwe Tamagotchi '
                               'geboren!\nHmm, hoe zullen we '
                               'hem/haar noemen?\n\nVoer een '
                               'naam in: ')).capitalize()
            naam_check = False
            while not naam_check:
                if len(t_naam) < 1:
                    t_naam = str(input("De naam kan alleen "
                                       "letters bewaren. "
                                       "Voer een naam in: "
                                       "")).capitalize()
                elif not t_naam.isalpha():
                    t_naam = str(input("De naam kan alleen "
                                       "letters bewaren. Voer een "
                                       "naam in: ")).capitalize()
                else:
                    naam_check = True
            beurt = 0
            afval = random.randint(0, 4)
            hongerig = random.randint(0, 4)
            ongelukkig = random.randint(0, 4)
            plaatje = plaatjes[1]
            scherm = plaatjes_layout(beurt, afval, ongelukkig,
                                     t_naam,
                                     hongerig, 'Succes met spelen!', plaatje)
            print(scherm)
            spelen = True
            leeftijd = leeftijden(beurt)
            while spelen:
                in_spel_keuze = str(input("Kies een optie:\n"))

                if in_spel_keuze.isdigit() and in_spel_keuze == '1':
                    beurt += 1
                    stop_eten_menu = False
                    while not stop_eten_menu:
                        eten_keuze = str(input(eten_kiezen(
                            dict_voeding,
                            t_naam)))
                        if eten_keuze.isdigit() and eten_keuze == \
                                '1':
                            hongerig, afval, ongelukkig, bericht = \
                                gezond_eten_geven(afval, ongelukkig,
                                                  hongerig)
                            totaal = hongerig + afval + ongelukkig
                            scherm, spelen, rank_bericht, rank = \
                                plaatje_kiezen(beurt, hongerig, afval,
                                               ongelukkig, plaatjes, totaal,
                                               leeg_ranking, speler_naam,
                                               t_naam, kopje, bericht,
                                               leeftijd)
                            stop_eten_menu = True
                            if spelen:
                                print(scherm)
                            else:
                                print(scherm + '\n' +
                                      rank_bericht + rank + '\n')
                        elif eten_keuze.isdigit() and eten_keuze == \
                                '2':
                            hongerig, afval, ongelukkig, bericht = \
                                ongezond_eten_geven(afval, ongelukkig,
                                                    hongerig)
                            totaal = hongerig + afval + ongelukkig
                            scherm, spelen, rank_bericht, rank = \
                                plaatje_kiezen(beurt, hongerig, afval,
                                               ongelukkig, plaatjes, totaal,
                                               leeg_ranking, speler_naam,
                                               t_naam, kopje, bericht,
                                               leeftijd)
                            stop_eten_menu = True
                            if spelen:
                                print(scherm)
                            else:
                                print(scherm + '\n' +
                                      rank_bericht + rank + '\n')

                        elif eten_keuze.isdigit() and eten_keuze == \
                                '3':
                            hongerig, afval, ongelukkig, bericht = \
                                geen_eten_geven(afval,
                                                ongelukkig, hongerig)
                            totaal = hongerig + afval + ongelukkig
                            scherm, spelen, rank_bericht, rank = \
                                plaatje_kiezen(
                                    beurt,
                                    hongerig, afval, ongelukkig,
                                    plaatjes,
                                    totaal, leeg_ranking, speler_naam,
                                    t_naam, kopje, bericht, leeftijd)
                            stop_eten_menu = True
                            if spelen:
                                print(scherm)
                            else:
                                print(scherm + '\n' + rank_bericht + rank +
                                      '\n')

                        else:
                            print('Kies een nummer tussen 1 en 3.\n')
                            stop_eten_menu = False

                elif in_spel_keuze.isdigit() and in_spel_keuze == '2':
                    beurt += 1
                    hongerig, afval, ongelukkig, bericht = \
                        verschonen(afval,
                                   ongelukkig, hongerig)
                    totaal = hongerig + afval + ongelukkig
                    scherm, spelen, rank_bericht, rank = plaatje_kiezen(
                        beurt,
                        hongerig, afval, ongelukkig, plaatjes,
                        totaal, leeg_ranking, speler_naam,
                        t_naam, kopje, bericht, leeftijd)
                    if spelen:
                        print(scherm)
                    else:
                        print(
                            scherm + '\n' + rank_bericht + rank + '\n')
                elif in_spel_keuze.isdigit() and in_spel_keuze == '3':
                    beurt += 1
                    spelletjes_menu = True
                    while spelletjes_menu:
                        spelletjes_keuze = str(
                            input('Welke spel wil je '
                                  'spelen?\n1. Kop of '
                                  'munt.\n2. Steen, papier, '
                                  'schaar.\n3. Toch maar '
                                  'niet.\n\nMaak een keuze:'))
                        if spelletjes_keuze.isdigit() and \
                                        spelletjes_keuze == '1':
                            wrong_input = True
                            while wrong_input:
                                kop_munt_input = input('{:^70}\n'
                                                       '{:^65}\n'
                                                       '{:^65}\n\n'
                                                       '{}'.format(
                                    'Kop '
                                    'of '
                                    'munt?',
                                    '1. Kop',
                                    '2. Munt',
                                    'Maak een keuze'
                                ))
                                if kop_munt_input == '1' or \
                                                kop_munt_input == '2':
                                    hongerig, ongelukkig, bericht = \
                                        kop_of_munt(
                                            kop_munt_input, hongerig,
                                            ongelukkig,
                                            t_naam, speler_naam)
                                    totaal = hongerig + afval + \
                                             ongelukkig
                                    scherm, spelen, \
                                    rank_bericht, rank = \
                                        plaatje_kiezen(
                                            beurt,
                                            hongerig, afval,
                                            ongelukkig,
                                            plaatjes,
                                            totaal, leeg_ranking,
                                            speler_naam,
                                            t_naam, kopje, bericht, leeftijd)
                                    if spelen:
                                        print(scherm)
                                    else:
                                        print(
                                            scherm + '\n' + rank_bericht +
                                            rank + '\n')
                                    wrong_input = False
                                    spelletjes_menu = False

                                else:
                                    print('Kies een nummer tussen 1 '
                                          'en 2.')
                        elif spelletjes_keuze.isdigit() and \
                                        spelletjes_keuze == '2':
                            spelletjes_menu = False
                            ssp_menu = True
                            while ssp_menu:
                                ssp_keuze = input('{:^70}\n'
                                                  '{:^65}\n'
                                                  '{:^65}\n'
                                                  '{:^65}\n\n'
                                                  '{}'
                                    .format(
                                    'Steen,'
                                    'papier of schaar?',
                                    '1. Steen',
                                    '2. Papier',
                                    '3. Schaar',
                                    'Maak een keuze'
                                ))
                                if ssp_keuze == '1' or ssp_keuze \
                                        == '2' or ssp_keuze == '3':
                                    hongerig, \
                                    afval, \
                                    ongelukkig, \
                                    bericht = steen_schaar_papier(
                                        ssp_keuze, hongerig,
                                        ongelukkig, afval)
                                    totaal = hongerig + afval + \
                                             ongelukkig
                                    print(hongerig)
                                    scherm, spelen, \
                                    rank_bericht, rank = \
                                        plaatje_kiezen(
                                            beurt, hongerig, afval,
                                            ongelukkig, plaatjes,
                                            totaal, leeg_ranking,
                                            speler_naam, t_naam, kopje,
                                            bericht, leeftijd)
                                    if spelen:
                                        print(scherm)
                                    else:
                                        print(
                                            scherm + '\n' + rank_bericht +
                                            rank + '\n')
                                    ssp_menu = False
                                else:
                                    print('Kies een nummer tussen 1 '
                                          'en 3.')
                                    ssp_menu = True
                        elif spelletjes_keuze.isdigit() and \
                                        spelletjes_keuze == '3':
                            hongerig += 1
                            ongelukkig += 2
                            totaal = hongerig + afval + ongelukkig
                            scherm, spelen, rank_bericht, rank = \
                                plaatje_kiezen(
                                    beurt,
                                    hongerig, afval, ongelukkig,
                                    plaatjes,
                                    totaal, leeg_ranking, speler_naam,
                                    t_naam, kopje, 'Jammer.', leeftijd)
                            spelletjes_menu = False
                            if spelen:
                                print(scherm)
                            else:
                                print(scherm + '\n' + rank_bericht + rank +
                                      '\n')
                        else:
                            print('Kies een '
                                  'nummer tussen 1 en '
                                  '3.')

                elif in_spel_keuze.isdigit() and in_spel_keuze == '4':
                    print('Tot volgende keer!')
                    spelen = False
                else:
                    totaal = hongerig + afval + ongelukkig
                    scherm, spelen, rank_bericht, rank = plaatje_kiezen(
                        beurt,
                        hongerig, afval, ongelukkig, plaatjes,
                        totaal, leeg_ranking, speler_naam,
                        t_naam, kopje, ' Kies '
                                       'een nummer tussen 1 en'
                                       ' 4', leeftijd)
                    if spelen:
                        print(scherm)
                    else:
                        print(scherm + '\n' + rank_bericht +
                              rank + '\n')
        elif main_keuze.isdigit() and main_keuze == "3":
            print(ranking_layout())
        elif main_keuze.isdigit() and main_keuze == "4":
            print("Bedankt voor het spelen, tot de voglende keer.")
            menu_eind = True
        else:
            print('Geen geldige optie. Kies een nummer tussen 1 '
                  'en 4\n')

