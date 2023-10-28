import re
import xml.etree.ElementTree as ET
import string
import os
import argparse

parser = argparse.ArgumentParser(description="Program do tworzenia instrukcji dostępu do rejestrów")
parser.add_argument('folder_xml', type=str, help="Folder zawierajacy wszystkie pliki xml")
parser.add_argument('plik_spis', type=str, help="Adres pliku do spisania wszystkich rejestrow")
parser.add_argument('plik_instrukcje', type=str, help="Adres pliku do spisania wszystkich instrukcji")
args = parser.parse_args()
print(args)
print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
folder_wejsciowy = str(args.folder_xml)
plik_spisu = str(args.plik_spis)
plik_instrukcji = str(args.plik_instrukcje)

def zapamietaj_dlugosci_zmiennych(typ_kodowania):
    if kodowanie[:3] == "MCR" or kodowanie[:3] == "MRC" : return [4,3,4,4,3]
    elif kodowanie[:4] == "MCRR" or kodowanie[:4] == "MRRC" : return [4,4,4]
    else :  return [2,3,4,4,3]



def trudna_funkcja(nazwa, atrybuty, instrukcja,wartosc, length):
    for x in range(0,len(atrybuty)):
        if "0b" in atrybuty[x] : atrybuty[x] = atrybuty[x].replace("0b","")
        atrybuty_razem = ''.join(atrybuty)
    print(atrybuty_razem)
    szukana_1_dl = 3
    szukana_2_dl = 2
    index_1 = atrybuty_razem.find(":m[")
    index_2 = atrybuty_razem.find("m[")
    if index_1 < index_2 and index_1 > -1 : 
        index_w = index_1
        dl_w = szukana_1_dl
    elif index_2 > -1 : 
        index_w = index_2
        dl_w = szukana_2_dl
    trzeba_zapisac_bitow = int(atrybuty_razem[index_w + dl_w]) + 1
    #print(instrukcja)
    suma = sum(length)
    if(index_w + trzeba_zapisac_bitow) == suma: na_koncu = ""
    else: na_koncu = atrybuty_razem[-(suma - index_w - trzeba_zapisac_bitow):]
    bity_poczatkowe = atrybuty_razem[:index_w]

    dopisane = str(bin(wartosc))[2:]
    while len(dopisane) < trzeba_zapisac_bitow: dopisane = "0" + dopisane
    match nazwa:
        case "AMEVCNTR0<m>" :
            calosc = bity_poczatkowe + dopisane[0] + "0" + dopisane[1:]
        case "AMEVCNTR1<m>" :
            calosc = bity_poczatkowe + dopisane[0] + "0" + dopisane[1:]
        case "TRCRSCTLR<m>":
            if wartosc < 16 : dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + "00" + dopisane[0]
        case "TRCACVR<m>":
            if wartosc < 8 : dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + "000" + dopisane[0]
        case "TRCACATR<m>":
            if wartosc < 8 : dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + "001" + dopisane[0]
        case "BRBINF<m>_EL1":
            if wartosc < 16 : dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + dopisane[0] + "00"
        case "BRBSRC<m>_EL1":
            if wartosc < 16: dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + dopisane[0] + "01"
        case "BRBTGT<m>_EL1":
            if wartosc < 16: dopisane = "0" + dopisane
            calosc = bity_poczatkowe + dopisane[1:] + dopisane[0] + "10"



        case _: calosc = bity_poczatkowe + dopisane + na_koncu
    
    
    lista_wypelnionych = []
    start = 0

    for x in length:
        part = calosc[start: start + x]
        lista_wypelnionych.append(part)
        start += x



    return lista_wypelnionych



def napisz_adres(parametry,nazwa):
    bufor_parametry = parametry.copy()
    addr = "ADDR=0x"
    if  bufor_parametry[4] == "": 
        bufor_parametry.pop() 
    for x in range(0,len(bufor_parametry)):
        bufor_parametry[x] = bufor_parametry[x].replace("x","1")
        #print(bufor_parametry[x]) 
        z= hex(int(bufor_parametry[x],2))[2:]
        addr = addr + z
    addr = addr + " NAME="+nazwa
    addr += " PAR=#0x"+hex(int(bufor_parametry[0],2))[2:]+","
    addr += "#0x"+hex(int(bufor_parametry[1],2))[2:]+","
    addr += "c"+hex(int(bufor_parametry[2],2))[2:]+","
    addr += "c"+hex(int(bufor_parametry[3],2))[2:]+","
    if len(bufor_parametry) == 5 : addr += "#0x"+hex(int(bufor_parametry[4],2))[2:]+""
    return addr

def zamien_binarne(do_zamiany, wymagana):
    zmienna = str(bin(int(do_zamiany,16)))[2:]
    while len(zmienna) < wymagana : zmienna = "0"+zmienna
    return zmienna


def wypelnij_instrukcje(base_instr, rekordy, czy_m):
    if not czy_m:
        for x in range(0,len(rekordy)):
            rekordy[x] = rekordy[x][2:]


    if base_instr[:4] == "MRC{" or base_instr[:4] == "MCR{":
        bufor = rekordy[0]
        base_instr = base_instr.replace("<coproc>", bufor)
        bufor = rekordy[1]      
        base_instr = base_instr.replace("<opc1>", bufor)
        bufor = rekordy[2]
        base_instr = base_instr.replace("<CRn>", bufor)    
        bufor = rekordy[3]                          
        base_instr = base_instr.replace("<CRm>", bufor)
        bufor = rekordy[4]                        
        base_instr = base_instr.replace("<opc2>", bufor) 
        return base_instr
    elif base_instr[:4] == "VMRS" or base_instr[:4] == "VMSR":
        bufor = rekordy[0]
        base_instr = base_instr.replace("<spec_reg>", bufor)
        return base_instr
    elif base_instr[:4] == "MRRC" or base_instr[:4] == "MCRR":
        bufor = rekordy[0]
        base_instr = base_instr.replace("<coproc>", bufor)
        bufor = rekordy[2]       
        base_instr = base_instr.replace("<opc1>", bufor)
        bufor = rekordy[1]
        base_instr = base_instr.replace("<CRm>", bufor)   
        return base_instr 
    elif base_instr[:4] == "LDC{":
        bufor = rekordy[0]
        base_instr = base_instr.replace("<coproc>", bufor)
        return base_instr
    elif base_instr[:4] == "STC{":
        bufor = rekordy[0]
        base_instr = base_instr.replace("<coproc>", bufor)
        bufor = rekordy[1]
        base_instr = base_instr.replace("<CRd>", bufor)
        return base_instr
    else:
        return base_instr


tree = ET.parse(folder_wejsciowy+ "\\enc_index.xml") 
root = tree.getroot()  
linijka = ""
for sectiongroup in root.iter('sectiongroup'):           
    for section in sectiongroup.iter('section'):        
        for body in section.iter('tbody'):          
            for row in body.iter('row'): 
                bufor_linka = ""
                bufor_nazwy = ""
                linijka = ""
                jestPoprawnaNazwa = False  
                jestPoprawnyLink = False    
                linkPobrany = False   
                for entry in row.iter('entry'):  
                    if not jestPoprawnaNazwa: 
                        if entry.text and not entry.text.isnumeric() and len(entry.text) > 2 and linkPobrany: 
                            bufor_nazwy += entry.text
                            jestPoprawnaNazwa = True
                    for a in entry.iter('a'): 
                            bufor_linka = a.text
                            linkPobrany = True
                            linijka += a.attrib['href'] + "  "
                            if not "<" in a.text: jestPoprawnyLink = True 
                with open(plik_spisu, "a") as plik:
                    if jestPoprawnyLink:
                        if jestPoprawnaNazwa: 
                            linijka = linijka + bufor_nazwy
                            plik.write(linijka +"\n")
                        else:
                            linijka = linijka + bufor_linka
                            plik.write(linijka +"\n")

                    else:
                            linijka = linijka + bufor_linka
                            plik.write(linijka +"\n")



counter = 0

with open(plik_spisu,"r") as plik:
    instrukcja =""
    lista_atrybutow = ["0000"] * 5
    i = 0
    lines = plik.readlines()
    for row in lines:
        link = row.split("  ") 
        folder_wejsciowy = str(args.folder_xml) +"\\" + link[0]
        tree = ET.parse(folder_wejsciowy) 
        root = tree.getroot()
        if not "<" in link[1]:
             for registers in root.iter("registers"):
                for register in registers.iter("register"):
                    for access_mechanisms in register.iter("access_mechanisms"):
                        for access_mechanism in access_mechanisms.iter("access_mechanism"):
                            for encoding in access_mechanism.iter("encoding"):  
                                gotowa = " "
                                i = 0         
                                for access_instruction in encoding.iter("access_instruction"):
                                    instrukcja = access_instruction.text
                                    
                                for enc in encoding.iter("enc"):                            
                                    lista_atrybutow[i] = enc.attrib['v']
                                    i = i + 1
                                gotowa = wypelnij_instrukcje(instrukcja,lista_atrybutow, False)
                                with open(plik_instrukcji,"a") as plik:
                                    if (register.attrib['execution_state'] == "AArch64"):
                                        plik.write(napisz_adres(lista_atrybutow,link[1].strip())+ " : "+gotowa + "\n")     
                                    else : 
                                        plik.write(link[1].strip() + " : "+gotowa + "\n")


        elif "<m>" in link[1]:
            counter +=1
            print(link[1].strip())
            #print(counter)
            zakres_gora = 0
            zakres_dol = 0
            for registers in root.iter("registers"):
                for register in registers.iter("register"):
                    for access_mechanisms in register.iter("access_mechanisms"):
                        for access_mechanism in access_mechanisms.iter("access_mechanism"): 
                            kodowanie = access_mechanism.attrib["accessor"][:5]
                            lista_atrybutow = [""] * 5
                            #print(kodowanie)  
                            dlugosci = zapamietaj_dlugosci_zmiennych(kodowanie)
                            #print(dlugosci)
                            for encoding in access_mechanism.iter("encoding"):
                                i = 0
                                gotowa = ""
                                for acc_array in encoding.iter("acc_array"):
                                    for acc_array_range in acc_array.iter("acc_array_range"):
                                        if acc_array_range.text[-2] == "-": zakres_gora = int(acc_array_range.text[-1])
                                        else: zakres_gora = int(acc_array_range.text[-2:])
                                        zakres_dol = int(acc_array_range.text[0])
                                for access_instruction in encoding.iter("access_instruction"):
                                    instr= access_instruction.text
                                for enc in encoding.iter("enc"):
                                    lista_atrybutow[i] = enc.attrib['v']
                                    i = i + 1
                                for wartosc in range(zakres_dol,zakres_gora+1):
                                    lista_zmiennych = trudna_funkcja(link[1].strip(), lista_atrybutow, instrukcja, wartosc, dlugosci)
                                    nazwa = link[1].replace("<m>",str(wartosc))
                                    instrukcja = instr.replace("<m>",str(wartosc))
                                    gotowa = wypelnij_instrukcje(instrukcja,lista_zmiennych, True)
                                    with open(plik_instrukcji,"a") as plik:
                                        if (register.attrib['execution_state'] == "AArch64"):
                                            
                                            plik.write(napisz_adres(lista_zmiennych,nazwa.strip())+ " : "+gotowa + "\n")     
                                        else : 
                                            plik.write(nazwa.strip() + " : " +gotowa + "\n")
                                #print(instrukcja)
                                #print(lista_atrybutow)
                                #print(link[1])
print(counter)