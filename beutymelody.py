import math
import time
from tkinter import filedialog, messagebox
import torch
from torch.cuda.amp import autocast
from diffusers import StableDiffusionPipeline,DPMSolverSDEScheduler,DPMSolverMultistepScheduler
from diffusers import StableDiffusionXLImg2ImgPipeline
import os
from PIL import Image, ImageOps,ImageTk
from compel import Compel
import tkinter as tk
from tkinter import Canvas, Scale,ttk
from googletrans import Translator
import random
import datetime
import time 
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
import pygame
from diffusers import StableDiffusionInpaintPipeline,DPMSolverMultistepScheduler,DPMSolverSDEScheduler,AutoPipelineForInpainting,DiffusionPipeline, UNet2DConditionModel,StableDiffusionPipeline
from diffusers import AutoPipelineForText2Image
import sys
from cryptography.fernet import Fernet
#arrays
azione=""
outfit=""
location=""
capelli=""
occhi=""
inquadratura=""

SFONDO= None
IMMAGINENASCOSTA= None

Totalconits=0
CointsLivel=0

#arrays
cucina = [
    "cucina design moderno",
    "cucina toni chiari del marmo e della ceramica",
    "cucina di lusso Dotata di elettrodomestici all'avanguardia",
    "cucina  eleganza e raffinatezza,lampadario in cristallo che pende sopra l'isola di cucina illumina la stanza, creando un'atmosfera accogliente e invitante",
    "cucina dove il lusso incontra la praticità"
    ]
sala_da_pranzo = [
    "Eleganza e comfort in sala da pranzo",
    "Sala da pranzo lussuosa con vista panoramica",
    "Sala da pranzo perfetta per cene eleganti",
    "Sala da pranzo lussuosa per cene indimenticabili",
    "Sala da pranzo elegante e accogliente"
    ]

camera_da_letto = [
    "Camera da letto accogliente e moderna",
    "Camera da letto confortevole e stilistica",
    "Camera da letto tranquilla e luminosa",
    "Camera da letto lussuosa per ospiti",
    "Camera da letto elegante e personale"
    ]

bagno = [
    "Bagno lussuoso per relax",
    "Bagno funzionale con vista panoramica",
    "Bagno tranquillo per un'esperienza spa",
    "Bagno elegante e rilassante",
    "Bagno lussuoso e confortevole"
    ]

salotto = [
    "Salotto confortevole ed elegante",
    "Salotto lussuoso e accogliente",
    "Salotto perfetto per intrattenere",
    "Salotto lussuoso per cene indimenticabili",
    "Salotto elegante e confortevole"
    ]

mansarda = [
    "Mansarda confortevole ed elegante",
    "Mansarda lussuosa e accogliente",
    "Mansarda perfetta per intrattenere",
    "Mansarda lussuosa per cene indimenticabili",
    "Mansarda elegante e confortevole"
    ]

esterno_piscina = [
    "Esterno lussuoso con piscina scintillante",
    "Esterno lussuoso con prato verde e piscina",
    "Esterno perfetto per il sole estivo",
    "Esterno lussuoso per una giornata al sole",
    "Esterno elegante e confortevole con piscina"
]

college_americano = [
    "Campus del college americano pieno di vita",
    "Aula del college americano per menti brillanti",
    "College americano per scoperta e innovazione",
    "Campus del college americano di storia e tradizione",
    "College americano che esprime eccellenza e ambizione"
]

ufficio = [
    "Ufficio moderno e luminoso",
    "Ufficio confortevole e produttivo",
    "Ufficio per collaborazione e innovazione",
    "Ufficio efficiente e stilistico",
    "Ufficio elegante e funzionale"
    ]

fastfood = [
    "Benvenuto in Burger Queen",
    "Entra in Fried Chicken Palace",
    "Scopri Pizza Planet",
    "Visita Taco Terra",
    "Esplora Sushi Speed"
    ]

capelli = ['biondi lisci', 'castano chiaro lisci', 'lunghi biondi', 'biondi ondulati', 'castano chiari  con mesh bionde', 'biondi con coda', 'ramati con cerchietto', 'biondi con treccie', 'castano chiaro raccolti', 'biondi con chignon']
occhi = ['verde smeraldo', 'azzurro verde', 'verde', 'verde mare', 'verde acqua', 'azzurro cielo', 'verde oliva', 'azzurro ghiaccio']
# Definisci i tuoi array di azioni
azioni_bagno = ['lei si lava il viso', 'lei fa la doccia', 'lei si insapona nella doccia']
azioni_bagno_NSFW = ['lei si lava il viso', 'lei fa la doccia', 'lei si insapona nella doccia','seduta sulla lavatrice a gambe aperte','seduta sul wc a gambe aperte']

azioni_cucina = ['lei è seduta sul tavolo in cucina e fa colazione', 'lei fa colazione con una tazza di cereali', 'lei beve una tazza di caffè']
azioni_cucina_NSFW = ['lei è seduta sul tavolo in cucina e fa colazione', 'lei fa colazione con una tazza di cereali', 'lei beve una tazza di caffè',
                      'lei è seduta sulla cucina a gambe aperte','lei è seduta sul tavolo a gambe aperte',
                      'lei è seduta su una sedia in cucina a gambe aperte','lei è in ginocchio sul tavolo','lei è seduta sul tavolo con le gambe sollevate e spalancate']
azioni_sala_da_pranzo = ['lei è seduta a tavola e pranza con delle uova', 'lei è seduta a tavola e pranza con un bistecca', 'lei è seduta a tavola e beve un succo di arancia']
azioni_sala_da_pranzo_NSFW = ['lei è seduta a tavola e pranza con delle uova', 'lei è seduta a tavola e pranza con un bistecca', 'lei è seduta a tavola e beve un succo di arancia',
                            'lei è seduta sul tavolo in sala da pranzo con le gambe aperte','lei è sdraiata sul tavolo in sala da pranzo con  a gambe aperte',
                            'lei è seduta su una sedia in sala da pranzo con gambe aperte','lei è in ginocchio sul tavolo in sala da pranzo','lei è seduta sul tavolo con le gambe sollevate e spalancate']

azioni_salotto = ['lei è seduta sul divano e guarda un film su netflix', 'lei è seduta sul divano e guarda un film', 'lei è seduta sul divano e mangia un pacchetto di patatine']
azioni_salotto_NSFW = ['lei è seduta sul divano e guarda un film su netflix', 'lei è seduta sul divano e guarda un film', 'lei è seduta sul divano e mangia un pacchetto di patatine',
                       'lei è seduta sul divano con le gambe aperte','lei è sdraiata sul divano con le gambe sollevate e aperte','lei è sul divano in posa dog']

azioni_esterno_piscina = ['lei nuota in piscina', 'lei è a bordo piscina', 'lei nuota sott''acqua in piscina']
azioni_esterno_piscina_NSFW = ['lei nuota in piscina', 'lei è a bordo piscina', 'lei nuota sott''acqua in piscina',
                               'lei è seduta a bordo piscina con le gambe aperte',
                               'lei è sdraiata a bordo piscina con le gambe sollevate e aperte']
azioni_mansarda = ['lei è seduta ad un tavolino in manzarda e beve un cocktail', 'lei è in piedi sulla mansarda e beve un succo di arancia', 'lei è seduta sulla mansarda']
azioni_mansarda_NSFW= ['lei è seduta ad un tavolino in manzarda e beve un cocktail', 'lei è in piedi sulla mansarda e beve un succo di arancia', 'lei è seduta sulla mansarda',
                       'lei è seduta sulla mansarda a gambe aperte','lei è seduta su una sedia a gambe aperte','lei è sdraiata sulla mansarda con le gambe aperte e sollevate']

azioni_fastfood = ['lei è seduta ad un tavolo di un fastfood e mangia un hotdog', 'lei è seduta in un tavolo in pizzeria e mangia una pizza', 'lei è seduta ad un tavolo del kebab e mangia un panino di kebab']
azioni_fastfood_NSFW = ['lei è seduta ad un tavolo di un fastfood e mangia un hotdog', 'lei è seduta in un tavolo in pizzeria e mangia una pizza', 'lei è seduta ad un tavolo del kebab e mangia un panino di kebab',
                   'lei è seduta su un tavolo di un fastfood a gambe aperte','lei è seduta su una sedia di un fastfood a gambe aperte','lei è seduta su un tavolo di un fastfood a gambe aperte e sollevate',
                   'lei è seduta su un tavolo di un pizzeria a gambe aperte','lei è seduta su una sedia di un pizzeria a gambe aperte','lei è seduta su un tavolo di un pizzeria a gambe aperte e sollevate',
                   'lei è seduta su un tavolo di un kebab a gambe aperte','lei è seduta su una sedia di un kebab a gambe aperte','lei è seduta su un tavolo di un kebab a gambe aperte e sollevate']

azioni_camera_da_letto = ['lei dorme rannicchiata sul matrimoniale in camera da letto', 'lei dorme nel letto matrimoniale in camera da letto a pancia in giù', 'lei dorme in camera da letto nel letto matrimoniale, sotto le coperte']
azioni_camera_da_letto_NSFW = ['lei dorme rannicchiata sul matrimoniale in camera da letto', 'lei dorme nel letto matrimoniale in camera da letto a pancia in giù', 'lei dorme in camera da letto nel letto matrimoniale, sotto le coperte',
                               'lei è seduta sul letto matrimoniale a gambe aperte','lei è seduta sul letto matrimoniale a gambe aperte e sollevate in area','lei è distesa sul letto matrimoniale','lei è in posa dog sul letto matrimoniale',
                               'lei è sul letto matrimoniale in posa candella con le gambe sollevate in area']

azioni_ufficio = ['lei sta lavorando al computer', 'lei sta partecipando a una riunione', 'lei sta scrivendo un report']
azioni_ufficio_NSFW = ['lei sta lavorando al computer', 'lei sta partecipando a una riunione', 'lei sta scrivendo un report','lei è seduta su una sedia d''ufficio con le gambe aperte',
                       'lei è seduta sulla scrivania con le gambe aperte','lei è seduta su una scrivania con le gambe aperte e sollevate in area']
azioni_college = ['lei sta assistendo a una lezione', 'lei sta studiando in biblioteca', 'lei sta facendo un esperimento in laboratorio',
                     'lei sta lavorando su un progetto di gruppo',
                     'lei sta leggendo un libro sotto un albero nel campus',
                     'lei sta facendo una pausa caffè al bar del college',
                     'lei sta partecipando a un club o a un''attività extracurricolare',
                     'lei sta facendo jogging nel campus',
                     'lei sta pranzando con gli amici nella mensa del college']

azioni_college_NSFW = ['lei sta assistendo a una lezione', 
                     'lei sta studiando in biblioteca', 
                     'lei sta facendo un esperimento in laboratorio',
                     'lei sta lavorando su un progetto di gruppo',
                     'lei sta leggendo un libro sotto un albero nel campus',
                     'lei sta facendo una pausa caffè al bar del college',
                     'lei sta partecipando a un club o a un''attività extracurricolare',
                     'lei sta facendo jogging nel campus',
                     'lei sta pranzando con gli amici nella mensa del college',
                     
                     'lei è seduta su un banco di scuola con le gambe aperte', 
                     'lei è su una scala in bibbiotega con le gambe spalancate', 
                     'lei è sdraiata un tavolo di laboratorio con le gambe spalancate in area',
                     'lei è nuda in mezzo ad un gruppo di studenti',
                     'lei lei legge un libbro seduta sotto un albero del campus ,con le gambe aperte',
                     'lei sta davanti alla macchina del caffè ,in piedi, e beve un caffè totalmente nuda',
                     'lei è seduta su un tavolo di un club con le gambe spalancate in area',
                     'lei sta facendo jogging nuda nel campus',
                     'lei è sdraiata sul tavolo della mensa del college, mentre i suoi amici mangiano su di lei',
                     'lei è seduta sul tavolo della mensa del college mentre i suoi amici le mangiano affianco ']

# Definisci i tuoi array di outfit
outfit_bagno = ['accappatoio', 'tuta da bagno', 'asciugamano']
outfit_cucina = ['pigiami', 'tuta', 'maglietta e pantaloni','vestaglia da notte','lingerie']
outfit_sala_da_pranzo = ['abito casual', 'jeans e maglietta', 'gonna e camicetta']
outfit_salotto = ['tuta', 'pigiami', 'shorts e canotta']
outfit_esterno_piscina = ['costume da bagno', 'pareo', 'shorts e top']
outfit_mansarda = ['vestito elegante', 'gonna lunga e top', 'pantaloni eleganti e camicetta','costume da bagno']
outfit_fastfood = ['jeans e maglietta', 'gonna e top', 'abito casual']
outfit_camera_da_letto = ['pigiami', 'babydoll', 'tuta','intimo bianco','lingerie','vestaglia da notte']
outfit_ufficio = ['tailleur', 'abito formale', 'gonna e camicetta']
outfit_college = ['jeans e maglietta', 'gonna e top', 'abito casual']
outfit_nsfw=['totalmente nuda','totalmente nuda con scarpe con tacco','totalmente nuda con collana']



inquadratura=['mezzo busto','figura completa','corpo intero','3/4']
pube= ['pube rasato','pube con una striscia di peli','pube peloso']


giorno_corrente=0
ora_corrente=0

def generateprompt():
        global azione,outfit,location,capelli,occhi,inquadratura,cucina, sala_da_pranzo, camera_da_letto, bagno, salotto, mansarda, esterno_piscina, college_americano, ufficio, fastfood
        global capelli, occhi
        global azioni_bagno, azioni_cucina, azioni_sala_da_pranzo, azioni_salotto, azioni_esterno_piscina, azioni_mansarda, azioni_fastfood, azioni_camera_da_letto, azioni_ufficio, azioni_universita
        global outfit_bagno, outfit_cucina, outfit_sala_da_pranzo, outfit_salotto, outfit_esterno_piscina, outfit_mansarda, outfit_fastfood, outfit_camera_da_letto, outfit_ufficio,outfit_college
        global giorno_corrente,ora_corrente,pube,combonfsw,CointsLivel,intimi
        # Ottieni il giorno corrente
        giorno_corrente = datetime.datetime.now().weekday()
        # Ottieni l'ora corrente
        ora_corrente = datetime.datetime.now().hour
        # Estrai un prompt a caso in base all'ora e ai giorni settimanali 
        print(f"giorno {giorno_corrente} ora: {ora_corrente}")
        if giorno_corrente == 5 or giorno_corrente == 6:
            print("sabato o domenica")
            # E' DOMENICA O SABATO GIRNI DI RIPOSO ALLORA: 
            # doccia
            if 11<= ora_corrente<= 12:
                location = random.choice(bagno)
                if combonfsw.get()=='attiva NSFW':
                   azione = random.choice(azioni_bagno_NSFW)
                   outfit = random.choice(outfit_nsfw)
                else:            
                    azione = random.choice(azioni_bagno)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_bagno)
            elif 12<= ora_corrente <= 13:
                #colazione
                location = random.choice(cucina)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_cucina_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_cucina)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_cucina)
                #pranzo sala da pranzo
            elif 13<= ora_corrente <= 14:
                location = random.choice(sala_da_pranzo)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_sala_da_pranzo_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_sala_da_pranzo)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_sala_da_pranzo)
                #tv
            elif 14<= ora_corrente <= 15:
                location = random.choice(salotto)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_salotto_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_salotto)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_salotto)
                #piscina
            elif 15<= ora_corrente <= 17:
                location = random.choice(esterno_piscina)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_esterno_piscina_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_esterno_piscina)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_esterno_piscina)
                #apericena
            elif 17<= ora_corrente<= 18:
                location = random.choice(mansarda)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_mansarda_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_mansarda)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_mansarda)
                # cena fuori
            elif 18<= ora_corrente<= 20:
                location = random.choice(fastfood)
                if combonfsw.get()=='attiva NSFW':
                   azione = random.choice(azioni_fastfood_NSFW)
                   outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_fastfood)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_fastfood)
            #streaming film tv
            elif 20<= ora_corrente<= 22:
                    location = random.choice(salotto)
                    if combonfsw.get()=='attiva NSFW':
                        azione = random.choice(azioni_salotto_NSFW)
                        outfit = random.choice(outfit_nsfw)
                    else:         
                        azione = random.choice(azioni_salotto)
                        if CointsLivel>= 5000 and CointsLivel < 10000:
                            outfit = random.choice(intimi)
                        elif CointsLivel>= 10000:
                            outfit = random.choice(outfit_nsfw)
                        else:
                            outfit = random.choice(outfit_salotto)
            # dormire
            elif ora_corrente >= 22 or ora_corrente <= 6:
                print ("fascia oraria")
                location = random.choice(camera_da_letto)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_camera_da_letto_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_camera_da_letto)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_camera_da_letto)
        else:
            print("non domenica o sabato")
            # NON è DOMENICA O SABATO GIRNI DI RIPOSO ALLORA: 
            if 7<= ora_corrente <= 8:
                #colazione
                location = random.choice(cucina)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_cucina_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_cucina)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_cucina)
                #lavoro
            elif 8<= ora_corrente <= 13:
                location = random.choice(ufficio)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_ufficio_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_ufficio)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_ufficio)
                #universiata
            elif 13<= ora_corrente <= 19:
                location = random.choice(college_americano)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_college_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_college)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_college)
            elif 19<= ora_corrente <= 20:
                #cena a casa
                location = random.choice(cucina)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_cucina_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_cucina)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_cucina)
                #film tv in salotto
            elif 20<= ora_corrente<= 22:
                location = random.choice(salotto)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_salotto_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_salotto)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_salotto)
                #dorme
            elif ora_corrente >= 22 or ora_corrente <= 6:
                print ("fascia oraria")
                location = random.choice(camera_da_letto)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_camera_da_letto_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_camera_da_letto)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_camera_da_letto)
                #bagno doccia
            elif 6<= ora_corrente<= 7:
                location = random.choice(bagno)
                if combonfsw.get()=='attiva NSFW':
                    azione = random.choice(azioni_bagno_NSFW)
                    outfit = random.choice(outfit_nsfw)
                else:         
                    azione = random.choice(azioni_bagno)
                    if CointsLivel>= 5000 and CointsLivel < 10000:
                        outfit = random.choice(intimi)
                    elif CointsLivel>= 10000:
                        outfit = random.choice(outfit_nsfw)
                    else:
                        outfit = random.choice(outfit_bagno)

tradu = Translator()
cfg=None
steps= None
photo= []
livel=1

model_id = "SG161222/Realistic_Vision_V6.0_B1_noVAE"
refinemodel= "stabilityai/stable-diffusion-xl-refiner-1.0"
tokenizer='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'



prompt =""
#prompt = "(photorealism:1.9),(1girl:1.9),(solo:1.9),(half-length shot:1.8),(a 17-year-old girl:1.9),(angelic face:1.8),American:1.9),(natural pink complexion:1. 8),(long blond hair:1.9),(emerald green eyes:1.9),(full lips:1.7),(sitting on a bench,wearing a casual T-shirt:1.9)"
negative= "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck"

def traduci(Testo_ita):
    testo_inglese = tradu.translate(Testo_ita, src='it', dest='en').text
    return testo_inglese


locationstr = [
    "Victorian Halliwell Manor exterior, San Francisco, night, fog, 'Charmed' TV series",
    "Attic of Halliwell Manor, Book of Shadows on pedestal, sunlight through stained glass windows",
    "Halliwell Manor living room, antique furniture, fireplace, family photos",
    "P3 nightclub interior, stage with live band, crowded dance floor, neon lights",
    "Halliwell Manor kitchen, herbs hanging, potion ingredients on shelves, sunlit",
    "San Francisco street view with Halliwell Manor, cable car passing by",
    "Magic School grand hall, floating books, mystical artifacts, students practicing spells",
    "Underworld cavern, dark and foreboding, fire pits, demon gathering",
    "Halliwell Manor conservatory, wicker furniture, plants, crystal chandelier",
    "Golden Gate Bridge at sunset, magical aura, 'Charmed' style",
    "Piper's restaurant Quake, bustling dining room, 90s decor",
    "Phoebe's newspaper office at The Bay Mirror, cubicles, busy journalists",
    "Halliwell Manor basement, creepy ambiance, washing machine, cardboard boxes",
    "Whitelighter realm, cloudy ethereal space, glowing figures in robes",
    "Prue's auction house workplace, antiques, paintings, elegant interior",
    "San Francisco police station, Darryl's desk, case files on 'unsolved' magical crimes",
    "Halliwell Manor driveway, Piper's Jeep and Prue's BMW parked",
    "Chinese herb shop, cluttered shelves, mystical ingredients, 'Charmed' universe",
    "Demonic market in a dark alley, potion vendors, magical weapons stalls",
    "Halliwell Manor backyard, herb garden, swing, BBQ area, string lights"
]
hphoebe=['hair blonde','brown hair']

outfitphoebe = [
    "Phoebe Halliwell, crop top, low-rise jeans, chunky belt, 90s style",
    "Leather jacket, fitted tank top, dark skinny jeans, ankle boots, edgy look",
    "Boho chic maxi dress, layered necklaces, sandals, flowing hair",
    "Halter neck top, flared pants, platform shoes, 70s inspired outfit",
    "Midriff-baring blouse, mini skirt, knee-high boots, 90s party look",
    "Casual sweater, leggings, sneakers, messy bun hairstyle",
    "Spaghetti strap dress, strappy heels, delicate jewelry, date night outfit",
    "Fitted blazer, silk camisole, tailored trousers, professional Phoebe look",
    "Colorful paisley print top, bell-bottom jeans, headband, hippie style",
    "Sleeveless turtleneck, leather miniskirt, ankle boots, 60s mod inspired",
    "Off-shoulder peasant blouse, denim shorts, gladiator sandals, bohemian summer look",
    "Cropped cardigan, high-waisted pants, kitten heels, retro-inspired outfit",
    "Sheer blouse, camisole underneath, wide-leg trousers, statement necklace",
    "Tight-fitting sweater, plaid mini skirt, knee socks, schoolgirl-inspired look",
    "Sequin top, leather pants, stilettos, glamorous night out ensemble",
    "Denim jacket, graphic tee, ripped jeans, combat boots, grunge style",
    "Wrap dress, wedge sandals, hoop earrings, breezy casual look",
    "Corset top, wide-leg jeans, chunky shoes, Y2K fashion",
    "Tie-front crop top, high-waisted shorts, espadrilles, summer festival outfit",
    "Slip dress, oversized cardigan, ankle boots, 90s layered look"
]
outfitpiper = [
    "Button-up blouse, high-waisted jeans, ankle boots, practical style",
    "Sleeveless turtleneck, tailored pants, loafers, professional look",
    "Cropped cardigan, floral midi skirt, kitten heels, feminine outfit",
    "Leather jacket, fitted t-shirt, bootcut jeans, edgy casual",
    "Wrap dress, wedge sandals, minimal jewelry, elegant simplicity",
    "Halter top, wide-leg trousers, strappy heels, night out ensemble",
    "Cozy sweater, leggings, ugg boots, comfortable home attire",
    "Denim jacket, graphic tee, cargo pants, relaxed weekend look",
    "Blazer, silk camisole, pencil skirt, business chic",
    "Off-shoulder top, capri pants, espadrilles, summer style",
    "Turtleneck sweater, plaid midi skirt, knee-high boots, autumn fashion",
    "Sleeveless blouse, culottes, block heels, trendy work outfit",
    "Peasant top, maxi skirt, gladiator sandals, boho-inspired look",
    "Fitted sweater, corduroy pants, ankle boots, cozy casual",
    "Sheath dress, pumps, pearl necklace, sophisticated event wear",
    "Utility jumpsuit, sneakers, bandana, practical yet stylish",
    "Silk pajama set, fluffy slippers, hair in a messy bun, loungewear",
    "Crisp white shirt, black trousers, stilettos, classic monochrome",
    "Crop top, high-waisted shorts, wedge sneakers, youthful summer look",
    "Turtleneck bodysuit, leather skirt, ankle boots, sleek evening attire"
]

outfitprue = [
    "Black turtleneck, leather pants, stiletto boots, sleek all-black ensemble",
    "Power suit, crisp white shirt, pointed heels, corporate chic",
    "Slip dress, oversized blazer, strappy sandals, 90s minimalism",
    "Fitted sweater, pencil skirt, pumps, sophisticated work outfit",
    "Halter top, wide-leg trousers, platform sandals, retro-inspired look",
    "Leather jacket, band tee, ripped jeans, edgy rocker style",
    "Wrap blouse, tailored shorts, loafers, polished casual",
    "Bodycon dress, denim jacket, ankle boots, night out attire",
    "Silk camisole, high-waisted pants, mules, elegant simplicity",
    "Turtleneck sweater dress, over-the-knee boots, statement earrings",
    "Crop top, high-waisted jeans, chunky sneakers, 90s street style",
    "Sleeveless turtleneck, midi skirt, kitten heels, vintage-inspired",
    "Off-shoulder top, leather mini skirt, stilettos, daring evening look",
    "Oversized sweater, leggings, combat boots, grunge-chic outfit",
    "Blazer dress, sheer tights, pointed-toe pumps, power dressing",
    "Satin slip top, mom jeans, strappy heels, effortless cool",
    "Turtleneck bodysuit, palazzo pants, wedges, 70s-inspired ensemble",
    "Cropped cardigan, A-line skirt, mary janes, preppy style",
    "Sheer blouse, high-waisted trousers, loafers, androgynous chic",
    "Fitted vest, wide-leg jeans, block heels, modern take on 90s fashion"
]

outfitpaige = [
    "Cropped tank top, low-rise jeans, chunky belt, early 2000s style",
    "Bohemian maxi dress, layered necklaces, gladiator sandals",
    "Leather jacket, band tee, ripped skinny jeans, rocker chic",
    "Halter neck top, flared pants, platform shoes, retro-inspired",
    "Off-shoulder peasant blouse, denim shorts, ankle boots, boho casual",
    "Colorful printed mini dress, oversized hoop earrings, strappy heels",
    "Graphic tee, cargo pants, sneakers, edgy street style",
    "Corset top, wide-leg jeans, stilettos, going-out look",
    "Crop hoodie, high-waisted leggings, chunky sneakers, athleisure",
    "Slip dress, denim jacket, combat boots, grunge-inspired outfit",
    "Tie-front crop top, high-waisted shorts, platform sandals, festival vibes",
    "Sequin tank top, leather pants, pointed boots, glam rock style",
    "Mesh long-sleeve top, mini skirt, knee-high boots, Y2K fashion",
    "Backless halter top, low-rise jeans, kitten heels, early 2000s party look",
    "Asymmetrical one-shoulder top, printed pants, wedge sandals",
    "Tube top, cargo skirt, chunky flip flops, summer casual",
    "Sheer overlay dress, bodysuit, ankle strap heels, daring evening wear",
    "Crop cardigan, high-waisted flared jeans, platform sneakers, retro casual",
    "Lace-up front top, mini skirt, over-the-knee boots, edgy night out",
    "Tie-dye shirt, denim cutoffs, slip-on vans, laid-back bohemian"
]

outfitbillie = [
    "Crop top, low-rise cargo pants, chunky sneakers, Y2K street style",
    "Leather bustier, skinny jeans, studded boots, edgy night out look",
    "Mesh long sleeve top, mini skirt, platform boots, cyber-inspired outfit",
    "Graphic baby tee, baggy jeans, chunky jewelry, 2000s throwback",
    "Halter neck jumpsuit, strappy heels, oversized hoops, sleek party attire",
    "Tie-front crop top, low-rise flared jeans, pointed mules, retro-modern mix",
    "Off-shoulder sweater, leather mini skirt, combat boots, grunge-chic",
    "Bandana top, distressed denim shorts, high-top sneakers, festival ready",
    "Corset-style tank, wide-leg pants, platform sandals, trendy evening wear",
    "Cropped hoodie, high-waisted track pants, chunky trainers, sporty-casual",
    "Metallic tube top, low-slung jeans, kitten heels, millennium party vibe",
    "Sheer overlay dress, bodysuit, ankle strap heels, daring night out",
    "Asymmetrical one-shoulder top, cargo skirt, strappy sandals, edgy-feminine",
    "Fishnet top, high-waisted shorts, lace-up boots, punk-inspired look",
    "Butterfly print crop top, low-rise miniskirt, flip flops, Y2K summer style",
    "Velour tracksuit, crop top, chunky gold chain, 2000s loungewear",
    "Lace-up front top, leather pants, stiletto boots, rock-chic ensemble",
    "Rhinestone-embellished tank, denim mini skirt, platform flip flops, glam casual",
    "Mesh long-sleeved crop top, cargo pants, chunky belt, futuristic street style",
    "Tie-dye baby tee, low-rise bootcut jeans, sneaker wedges, retro-casual fusion"
]
azionephoebe = [
    "Phoebe levitating to dodge a demon's attack, mid-air kick",
    "Writing a spell in the Book of Shadows, determined expression",
    "Having a premonition, eyes closed, hands on temples",
    "Throwing a potion vial at a demon, fierce stance",
    "Practicing martial arts in the manor's backyard, high kick",
    "Meditating on a yoga mat, surrounded by candles",
    "Riding her bicycle through San Francisco streets, hair flowing",
    "Typing her advice column at the Bay Mirror, focused at computer",
    "Casting a spell with her sisters, hands linked in circle",
    "Reading tarot cards, mystical aura around her",
    "Comforting a crying Paige, sisterly hug",
    "Flirting with a handsome stranger at P3, coy smile",
    "Researching demons in old books, surrounded by stacks of tomes",
    "Celebrating a vanquish with her sisters, high-fiving",
    "Sneaking into a demon lair, stealthy posture",
    "Giving relationship advice to Piper, gesturing expressively",
    "Using empathy power, hand on heart, eyes glowing",
    "Arguing with Cole, hands on hips, defiant pose",
    "Consoling an innocent, compassionate expression",
    "Dancing carefree at P3, arms in the air, big smile"
]

azionepiper = [
    "Freezing a demon mid-attack, hands outstretched",
    "Mixing a potion in the kitchen, focused expression",
    "Blowing up a demon with a flick of her hands, determined look",
    "Managing P3 nightclub, clipboard in hand, giving orders",
    "Cooking a family dinner, stirring a pot with a wooden spoon",
    "Holding baby Wyatt, protective stance",
    "Arguing with Leo, hands on hips, frustrated expression",
    "Consoling a crying Phoebe, sisterly hug",
    "Writing a spell in the Book of Shadows, brow furrowed in concentration",
    "Molecular combustion on multiple demons, action pose",
    "Balancing a tray of drinks at Quake, waitress uniform",
    "Time freezing the entire street, panicked expression",
    "Mediating between her sisters, calming gesture",
    "Driving her Jeep, determined look on face",
    "Tending to the herb garden, peaceful expression",
    "Practicing her freezing power on falling objects",
    "Giving a pep talk to her sisters before a big battle",
    "Rocking out on stage at P3, microphone in hand",
    "Changing a diaper with magical assistance, looking frazzled",
    "Leading a Wiccan ceremony, arms raised, eyes closed"
]

azioneprue = [
    "Using telekinesis to throw a demon across the room, intense focus",
    "Astral projecting, ethereal form appearing elsewhere",
    "Squinting eyes to move object precisely, concentration evident",
    "Examining an artifact at Buckland's auction house, professional demeanor",
    "Levitating to avoid demon attack, mid-air defensive pose",
    "Flinging multiple objects at once with telekinesis, powerful stance",
    "Researching in old books, surrounded by stacks of tomes",
    "Taking charge in a demon fight, giving orders to sisters",
    "Using telekinesis to clean the manor, multitasking",
    "Astral projecting to spy on a suspect, stealthy pose",
    "Martial arts training in the backyard, high kick",
    "Confronting Andy about magic, serious expression",
    "Comforting a crying Piper, protective big sister mode",
    "Photography session, camera in hand, artistic focus",
    "Casting a spell with her sisters, hands linked",
    "Telekinetically slamming the Book of Shadows shut, frustrated",
    "Dodging energy ball with a gymnastic move, athletic pose",
    "Leading a stake-out, binoculars in hand, determined look",
    "Using telekinesis in a creative way to solve a problem",
    "Standing protectively in front of her sisters, fierce expression"
]

azionepaige = [
    "Orbing out to escape danger, blue lights swirling",
    "Calling for an object, hand outstretched, object materializing",
    "Healing a wounded innocent, hands glowing",
    "Scrying for a lost witch, crystal spinning over a map",
    "Throwing a potion vial with precision, fierce expression",
    "Orbing a demon's energy ball back at them, triumphant smile",
    "Casting a spell solo, confident stance",
    "Shape-shifting into another form, mid-transformation",
    "Levitating during whitelighter training, concentrate look",
    "Comforting a charge, compassionate expression",
    "Arguing with the Elders, defiant pose",
    "Glamouring her appearance, magical shimmer effect",
    "Sensing for her charges, eyes closed in focus",
    "Telekinetic orbing multiple objects at once, strained expression",
    "Creating a magical forcefield, protective stance",
    "Orbing with a passenger, holding onto them tightly",
    "Using empathy power to connect with a charge, emotional moment",
    "Combining powers with her sisters, linked hands glowing",
    "Confronting her evil past life, determined expression",
    "Balancing magic and social work, juggling magical items and case files"
]

azionebillie = [
    "Projecting a scenario, hands framing an imaginary scene",
    "Using telekinesis to deflect an attack, defensive stance",
    "Practicing projection power, surrounded by shifting reality",
    "Fighting demons with martial arts, high kick",
    "Creating an illusion, mischievous smile",
    "Researching in magic school, surrounded by floating books",
    "Projecting herself to another location, fading effect",
    "Using enhanced agility to dodge attacks, acrobatic pose",
    "Casting a spell with the Charmed Ones, part of the circle",
    "Training her powers with Phoebe, focused expression",
    "Confronting her sister Christy, conflicted emotions",
    "Projecting her desires accidentally, chaotic scene around her",
    "Using telekinesis to multitask, various objects floating",
    "Infiltrating the demon world undercover, stealthy pose",
    "Combining her power with the Charmed Ones, energy building",
    "Reflecting on her past, looking at old photos, pensive",
    "Protecting an innocent with a projected shield, determined look",
    "Engaging in magical combat, action pose mid-fight",
    "Bonding with Wyatt and Chris, playful aunt mode",
    "Realizing the extent of her powers, awe-struck expression"
]
hpaige = [
    "Long straight black hair",
    "Shoulder-length red hair, side-swept bangs",
    "Wavy auburn hair, middle part",
    "Short spiky red hair",
    "Long dark brown hair with subtle highlights",
    "Medium-length copper hair, tousled waves",
    "Straight dark red hair, blunt cut",
    "Long layered black hair with red undertones",
    "Messy updo, deep auburn color",
    "Sleek bob, intense red color",
    "Long wavy hair, dark brown with reddish tint",
    "Pixie cut, bright red",
    "Shoulder-length black hair with choppy layers",
    "Long straight hair, dark red ombre",
    "Messy bun, copper red color",
    "Loose curls, rich auburn shade",
    "Straight hair with side bangs, dark brown",
    "Textured lob, vibrant red",
    "Half-up half-down style, black hair",
    "Braided crown, deep red color"
]

azionistregheNSFW=['(gambe aperte:1.9)','(sdaiata a gambe aperte:1.9)']

pussyclose_up="""(((show vaginal, wet,cumdrip,pussy ,close-up, anus, uncensored, pussy juice,breasts, Realistic skin texture,pale skin, dripping,urethra, 
legs up, clitoris, masterpiece, best quality,realistic,photo realistic,photography, highly detailed, sharp focus,trending on artstation,studio photo, intricate details, highly detailed)))"""

intimi = [
"Reggiseno in pizzo",
"Slip brasiliani",
"Body in seta",
"Perizoma in raso",
"Sottoveste in satin",
"Culotte in microfibra",
"Babydoll in pizzo",
"Giarrettiera in pizzo",
"Canotta in cotone",
"Brasiliana in pizzo",
"Sottoveste a balconcino",
"Tanga in raso",
"Corpetto in pizzo",
"Culotte a vita alta",
"Sottoveste a balconcino",
"Brasiliana in microfibra",
"Body in tulle",
"Slip in pizzo",
"Sottoveste in raso",
"Tanga in microfibra",
"Reggiseno push-up in pizzo",
"Reggiseno a balconcino in raso",
"Reggiseno a fascia in cotone",
"Reggiseno a triangolo in seta",
"Reggiseno a ferretto in microfibra",
"Reggiseno a balconcino in tulle",
"Reggiseno a sostegno in pizzo",
"Reggiseno a fascia in raso",
"Reggiseno a triangolo in cotone",
"Reggiseno a ferretto in seta",
"Perizoma in pizzo",
"Perizoma in raso",
"Perizoma in microfibra",
"Perizoma in tulle",
"Perizoma in seta",
"Perizoma in cotone",
"Perizoma in pizzo e raso",
"Perizoma in microfibra e tulle",
"Perizoma in seta e cotone",
"Perizoma in pizzo e seta",
"Costume da mare a balconcino",
"Costume da mare a ferretto",
"Costume da mare a triangolo",
"Costume da mare a push-up",
"Costume da mare a sostegno",
"Costume da mare a fascia",
"Costume da mare a pizzo",
"Costume da mare a raso",
"Costume da mare a microfibra",
"Costume da mare a tulle",
"Costume da mare a seta",
"Costume da mare a cotone",
"Costume da mare a pizzo e raso",
"Costume da mare a microfibra e tulle",
"Costume da mare a seta e cotone",
"Costume da mare a pizzo e seta",
"Costume da mare a raso e microfibra",
"Costume da mare a tulle e seta",
"Costume da mare a pizzo e microfibra",
"Costume da mare a raso e tulle",
"Costume da mare a seta e microfibra"
]

lora= False
selviso=""
import shutil
bondage= ".\\model\\bondage\\bondage-v11-ep105.safetensors"
diffusionXLbase10= "stabilityai/stable-diffusion-xl-base-1.0"
StableDiffusion15= "runwayml/stable-diffusion-v1-5"
Realistic_Vision_V60_B1_noVAE="SG161222/Realistic_Vision_V6.0_B1_noVAE" #ok
NSFW= "UnfilteredAI/NSFW-gen-v2"
pipe=None
from diffusers import StableDiffusionXLPipeline
bondagearrays=[
    "front full,dress pantyhose heels brastrap lace otm classicdamsel hbae sitting rupperarm rupperchest rlowerchest rwaist rknees rankles rthighs chair blindfold, cleavegag, coloredrope damselindistress <lyco:bondage-v11-p20:0.7>, Cottonwood,Endangered redwood Cyberpunk Rarefied,Isolated aesthetic",
    "naked woman bound between two poles spread legs vagina nipples face afraid,barn <lyco:bondage-v11-p20:0.7>, Elder Techy Comfortable,Monochromatic cinematic,aesthetic",
    "front medium kneeling blonde dress tapegag classicdamsel sitting floor (wol rope tied uwe) cleavage downblouse damselindistress sad <lyco:bondage-v11-p20:0.7>, Gigantic cinematic,grandiose",
    "metal collar (ballgag:1.1), ebony woman front dark hair breasts corset<lyco:bondage-v11-p20:0.7>, Techno-organic Luxurious masterpiece,aesthetic",
    "green rope wol tied side profile naked woman kneeling breasts blonde hair <lyco:bondage-v11-p20:0.7>, Lime Impressive Ian McQue masterpiece",
    "hogtie front full rope tied bondage nipples breasts ballgag harness pantyhose laying on floor shoulder <lyco:bondage-v11-p20:0.7>, Fir Futurama epic",
    "green latex catsuit front full sitting heels redhead face <lyco:bondage-v11-p20:0.7>, Larch Loish intricate,cinematic",
    "side top , brastrap jeans shirt outdoors tapegag hfad rwrists rankles ziptie rope tied cleavage downblouse damselindistress sad <lyco:bondage-v11-p20:0.7>, Pecan,Jack pine Alien-like Exquisite,Incredible masterpiece",  
    "fancysteel (chastitybelt:1.1) front medium naked woman, tiara standing metal collar (oue:1.1) <lyco:bondage-v11-p20:0.5>, Blissful",  
    "front  medium skirt shirt schoolgirl pigtails studio ballgag classicdamsel hfab standing rshoulder rupperchest rlowerchest rwaist hardpoint brownrope <lyco:bondage-v11-p20:0.7>, Elder Augmented Reality Disorienting,Moody intricate",  
    "ballgag close harness , <lyco:bondage-v11-p20:0.7>, Modernistic grandiose <lora:LowRA:0.7>, hasselblad, film still, skin pores, 4K",
    "gasmask front close visor shoulders braids <lyco:bondage-v11-p20:0.7>, European beech Spectacular Andrew Bosley cinematic,aesthetic", 
    "red latex hood front close lipstick eyes bokeh blonde <lyco:bondage-v11-p20:0.7>, Sci-fi Glimmering epic,aesthetic", 
    "sketch, monochrome, ugly, blurry, boring, cropped, child, worst, drawing",
    "rope tied bondage shibari woman sitting on floor heels front full uwe breasts nipples ballgag harness, boxtie, frogtie <lyco:bondage-v11-p20:0.7>, Banana Techno-organic Maciej Kuciara grandiose,detailed", 
]
def Streghe():
    global selez_stregha,prompt,hphoebe,locationstr,hphoebe,outfitphoebe,outfitpiper,outfitpaige,outfitprue,outfitbillie,azionephoebe,azionebillie
    global azionepiper,azionepaige,azioneprue,pube,testo,testonegative,pipe,steps,cfg,outfit_nsfw,comblist,lora,selviso,pussyclose_up,CointsLivel,intimi
    global bondage,StableDiffusion2,diffusionXLbase10,Realistic_Vision_V60_B1_noVAE,NSFW,comboModelgen,pipe,combonfsw,CointsLivel,bondagearrays,testo
    #['bondage','diffuserXL','diffuser2.1','realistic vision v6','nsfw']
    # Crea un nuovo scheduler
    if (comboModelgen.get() == 'bondage') or (combonfsw.get() == "attiva NSFW" and CointsLivel == 5000):
        pipe =StableDiffusionPipeline.from_single_file(bondage, torch_dtype=torch.float16)
    elif comboModelgen.get()=='diffuserXL':
        pipe = AutoPipelineForText2Image.from_pretrained(diffusionXLbase10, torch_dtype=torch.float16)
    elif comboModelgen.get()=='diffuser1.5':
        pipe = AutoPipelineForText2Image.from_pretrained(StableDiffusion15, torch_dtype=torch.float16)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    elif comboModelgen.get()=='realistic vision v6':
        pipe = AutoPipelineForText2Image.from_pretrained(Realistic_Vision_V60_B1_noVAE, torch_dtype=torch.float16) #ok
    elif comboModelgen.get()=='nsfw':
        pipe = AutoPipelineForText2Image.from_pretrained(NSFW, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.safety_checker = None
    pipe.requires_safety_checker = False
    print("streghe")
    comblist=None
    prompt=""
    #phoebe
    if selez_stregha.get()=="Phoebe":
        if testo.get("1.0", "end-1c").strip()=='':
            if combonfsw.get()== "attiva NSFW":
                if CointsLivel>= 5000 and CointsLivel<10000:
                    prompt= f"1girl, solo,A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},brown eyes,{random.choice(bondagearrays)},{pussyclose_up}<lora:4lyss4m:1.0>"
                else:    
                    comblist= azionephoebe+azionistregheNSFW
                    prompt= f"""(totalmente nuda:1.9),{random.choice(locationstr)},A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},
brown eyes,lips,traditional media,red shirt,realistic,soft lighting,{random.choice(outfit_nsfw)},{pube},{random.choice(comblist)}
professional Photography, Photorealistic, detailed, RAW, analog, sharp focus, 8k, HD, high quality, masterpiece,{pussyclose_up}<lora:4lyss4m:1.0>"""
            else:
                #cointis livel
                if CointsLivel>= 5000 and CointsLivel < 10000:
                    print("Outfit INTIMO")
                    prompt= f"""{random.choice(locationstr)},A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},
brown eyes,lips,traditional media,red shirt,realistic,soft lighting,{random.choice(intimi)},{random.choice(azionephoebe)}
professional Photography, Photorealistic, detailed, RAW, analog, sharp focus, 8k, HD, high quality,masterpiece,<lora:4lyss4m:1.0>"""
                elif CointsLivel>= 10000:
                    comblist= azionepiper+azionistregheNSFW
                    prompt= f"""(totalmente nuda:1.9),{random.choice(locationstr)},A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},
brown eyes,lips,traditional media,red shirt,realistic,soft lighting,{random.choice(outfit_nsfw)},{pube},{random.choice(comblist)}
professional Photography, Photorealistic, detailed, RAW, analog, sharp focus, 8k, HD, high quality, masterpiece,{pussyclose_up}<lora:4lyss4m:1.0>"""
                else:
                    if comboModelgen.get()== 'bondage':
                        prompt= f"""1girl, solo,A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},
brown eyes,{random.choice(bondagearrays)},{pussyclose_up}<lora:4lyss4m:1.0>"""
                    else:
                        prompt= f"""{random.choice(locationstr)},A beautiful 4lyss4m woman,1girl,solo,long hair,looking at viewer,smile,{random.choice(hphoebe)},
brown eyes,lips,traditional media,red shirt,realistic,soft lighting,{random.choice(outfitphoebe)},{random.choice(azionephoebe)}
professional Photography, Photorealistic, detailed, RAW, analog, sharp focus, 8k, HD, high quality,masterpiece,<lora:4lyss4m:1.0>"""
        else:
            prompt= traduci(testo.get("1.0", "end-1c").strip())  
            prompt= "4lyss4m woman,1girl,"+prompt+"<lora:4lyss4m:1.0>"
            print(f"personale prompt: {prompt}")
            
        if lora== False:
            pipe.load_lora_weights(".\\Lora\\4lyss4m.safetensors", weight_name="4lyss4m.safetensors", adapter_name="4lyss4m")
            lora== True
        selviso= os.path.join(".\\faces_streghe\\phoebe",random.choice([viso for viso in os.listdir(".\\faces_streghe\\phoebe")])) 
        
    #piper
    elif selez_stregha.get()=="Piper":
        if testo.get("1.0", "end-1c").strip()=='':
            if combonfsw.get()== "attiva NSFW":
                if CointsLivel>= 5000 and CointsLivel< 10000:
                    prompt=f"1girl, solo,h011ym4ri3c0mb5, full body, brown hair, brown eyes, {random.choice(bondagearrays)}, {pube},lips, {random.choice(locationstr)}, looking at viewer, upper body, morning, bright, {pussyclose_up}<lora:Holly_Marie_Combs_PMv1_Lora:1.3>"
                else:
                    comblist= azionepiper+azionistregheNSFW
                    prompt=f"""(totalmente nuda:1.9),(RAW, analogue, Nikon Z 14mm ultra-wide angle lens, award-winning glamour photograph, ((best quality)), ((masterpiece)), ((realistic)), skin pores, subsurface scattering, 
radiant light rays, high-res, detailed facial features, high detail, sharp focus, smooth, aesthetic, extremely detailed, (extremely detailed eyes, extremely detailed iris), extremely detailed hair, 
extremely detailed skin, extremely detailed clothes, octane render, photorealistic, realistic, post-processing, max detail, realistic shadows, roughness, natural skin texture, real life, ultra-realistic, 
photorealism, photography, 8k UHD, photography, hdr, intricate, elegant, highly detailed, sharp focus, stunning, beautiful, gorgeous), (photorealistic), (realistic), h011ym4ri3c0mb5, full body, brown hair, 
brown eyes, {random.choice(outfit_nsfw)}, {pube},lips, {random.choice(locationstr)}, {random.choice(comblist)}, looking at viewer, upper body, morning, bright, {pussyclose_up}<lora:Holly_Marie_Combs_PMv1_Lora:1.3>"""
            else:
                if CointsLivel>= 5000 and CointsLivel < 10000:
                    print("Outfit INTIMO")
                    prompt=f"""(RAW, analogue, Nikon Z 14mm ultra-wide angle lens, award-winning glamour photograph, ((best quality)), ((masterpiece)), ((realistic)), skin pores, subsurface scattering, 
radiant light rays, high-res, detailed facial features, high detail, sharp focus, smooth, aesthetic, extremely detailed, (extremely detailed eyes, extremely detailed iris), extremely detailed hair, 
extremely detailed skin, extremely detailed clothes, octane render, photorealistic, realistic, post-processing, max detail, realistic shadows, roughness, natural skin texture, real life, ultra-realistic, 
photorealism, photography, 8k UHD, photography, hdr, intricate, elegant, highly detailed, sharp focus, stunning, beautiful, gorgeous), (photorealistic), (realistic), h011ym4ri3c0mb5, full body, brown hair, 
brown eyes, {random.choice(intimi)}, lips, {random.choice(locationstr)}, {random.choice(azionepiper)}, looking at viewer, upper body, morning, bright, <lora:Holly_Marie_Combs_PMv1_Lora:1.3>"""
                elif CointsLivel>=10000:
                    comblist= azionepiper+azionistregheNSFW
                    prompt=f"""(totalmente nuda:1.9),(RAW, analogue, Nikon Z 14mm ultra-wide angle lens, award-winning glamour photograph, ((best quality)), ((masterpiece)), ((realistic)), skin pores, subsurface scattering, 
radiant light rays, high-res, detailed facial features, high detail, sharp focus, smooth, aesthetic, extremely detailed, (extremely detailed eyes, extremely detailed iris), extremely detailed hair, 
extremely detailed skin, extremely detailed clothes, octane render, photorealistic, realistic, post-processing, max detail, realistic shadows, roughness, natural skin texture, real life, ultra-realistic, 
photorealism, photography, 8k UHD, photography, hdr, intricate, elegant, highly detailed, sharp focus, stunning, beautiful, gorgeous), (photorealistic), (realistic), h011ym4ri3c0mb5, full body, brown hair, 
brown eyes, {random.choice(outfit_nsfw)}, {pube},lips, {random.choice(locationstr)}, {random.choice(comblist)}, looking at viewer, upper body, morning, bright, {pussyclose_up}<lora:Holly_Marie_Combs_PMv1_Lora:1.3>"""
                else:
                    if comboModelgen.get()== 'bondage':
                        prompt=f"""1girl, solo,h011ym4ri3c0mb5, full body, brown hair, brown eyes, {random.choice(bondagearrays)}, {pube},lips, {random.choice(locationstr)}, looking at viewer, upper body, morning, bright, {pussyclose_up}<lora:Holly_Marie_Combs_PMv1_Lora:1.3>"""
                    else: 
                        prompt=f"""(RAW, analogue, Nikon Z 14mm ultra-wide angle lens, award-winning glamour photograph, ((best quality)), ((masterpiece)), ((realistic)), skin pores, subsurface scattering, 
radiant light rays, high-res, detailed facial features, high detail, sharp focus, smooth, aesthetic, extremely detailed, (extremely detailed eyes, extremely detailed iris), extremely detailed hair, 
extremely detailed skin, extremely detailed clothes, octane render, photorealistic, realistic, post-processing, max detail, realistic shadows, roughness, natural skin texture, real life, ultra-realistic, 
photorealism, photography, 8k UHD, photography, hdr, intricate, elegant, highly detailed, sharp focus, stunning, beautiful, gorgeous), (photorealistic), (realistic), h011ym4ri3c0mb5, full body, brown hair, 
brown eyes, {random.choice(outfitpiper)}, lips, {random.choice(locationstr)}, {random.choice(azionepiper)}, looking at viewer, upper body, morning, bright, <lora:Holly_Marie_Combs_PMv1_Lora:1.3>"""
        else:
            prompt= traduci(testo.get("1.0", "end-1c").strip())
            prompt= "1girl, solo,h011ym4ri3c0mb5,"+prompt+"<lora:Holly_Marie_Combs_PMv1_Lora:1.3>"
            print(f"personale prompt: {prompt}")
        if lora== False:
           pipe.load_lora_weights(".\\Lora\\Holly_Marie_Combs_PMv1_Lora.safetensors", weight_name="Holly_Marie_Combs_PMv1_Lora.safetensors", adapter_name="Holly_Marie_Combs_PMv1_Lora")
           lora=True
        selviso= os.path.join(".\\faces_streghe\\piper",random.choice([viso for viso in os.listdir(".\\faces_streghe\\piper")])) 
    #prue
    elif selez_stregha.get()=="Prue":
        if testo.get("1.0", "end-1c").strip()=='': 
            if combonfsw.get()== "attiva NSFW":
                if CointsLivel>= 5000 and CointsLivel<10000:
                    prompt = f"""1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(bondagearrays)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:Sh4nn3nD:1.0>"""
                else:
                    comblist= azioneprue+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube}, {random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality,{pussyclose_up}<lora:Sh4nn3nD:1.0>"""
            else:
                if CointsLivel>= 5000 and CointsLivel < 10000:
                    print("Outfit INTIMO")
                    prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(intimi)}, {random.choice(azioneprue)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:Sh4nn3nD:1.0>"""
                elif  CointsLivel>=10000:
                    comblist= azioneprue+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube}, {random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality,{pussyclose_up}<lora:Sh4nn3nD:1.0>"""
                else:
                    if comboModelgen.get()== 'bondage':
                        prompt = f"""1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(bondagearrays)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:Sh4nn3nD:1.0>"""
                    else:   
                        prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((Sh4nn3nD))), 27 years old, long black hair, green eyes, 
detailed facial features, {random.choice(outfitprue)}, {random.choice(azioneprue)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:Sh4nn3nD:1.0>"""
        else:
            prompt= traduci(testo.get("1.0", "end-1c").strip())
            prompt= "1girl,solo,(((Sh4nn3nD))),"+prompt+"<lora:Sh4nn3nD:1.0>"
            print(f"personale prompt: {prompt}")
            
        if lora== False:
            pipe.load_lora_weights(".\\Lora\\PrueHalliwell.safetensors", weight_name="PrueHalliwell.safetensors", adapter_name="PrueHalliwell")
            lora= True
        selviso= os.path.join(".\\faces_streghe\\prue",random.choice([viso for viso in os.listdir(".\\faces_streghe\\prue")])) 
    #Paige
    elif selez_stregha.get()=="Paige":
        if testo.get("1.0", "end-1c").strip()=='':
            if combonfsw.get()== "attiva NSFW":
                if CointsLivel>=5000 and CointsLivel< 10000:
                    prompt = f"""1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(bondagearrays)},professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:R0s3McG:1.0>"""
                else:
                    comblist= azionepaige+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube},{random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality,{pussyclose_up}<lora:R0s3McG:1.0>"""
            else:
                if CointsLivel>=5000 and CointsLivel < 10000:
                    print("Outfit INTIMO")
                    prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(intimi)}, {random.choice(azionepaige)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:R0s3McG:1.0>"""
                elif CointsLivel>= 10000:
                    comblist= azionepaige+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube},{random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality,{pussyclose_up}<lora:R0s3McG:1.0>"""
                else:
                    if comboModelgen.get()== 'bondage':
                        prompt = f"""1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(bondagearrays)},professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:R0s3McG:1.0>"""
                    else:
                        prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((R0s3McG))), 25 years old, {random.choice(hpaige)}, brown eyes, 
detailed facial features, {random.choice(outfitpaige)}, {random.choice(azionepaige)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, 
high quality<lora:R0s3McG:1.0>"""
        else:
            prompt= traduci(testo.get("1.0", "end-1c").strip())
            prompt= "1girl,solo,(((R0s3McG))),"+prompt+"<lora:R0s3McG:1.0>"
            print(f"personale prompt: {prompt}")
        if lora== False:
            pipe.load_lora_weights(".\\Lora\\PaigeMatthews.safetensors", weight_name="PaigeMatthews.safetensors", adapter_name="PaigeMatthews")
            lora=True
        selviso= os.path.join(".\\faces_streghe\\paige",random.choice([viso for viso in os.listdir(".\\faces_streghe\\paige")])) 
    #billie
    elif selez_stregha.get()=="Billie":
        if testo.get("1.0", "end-1c").strip()=='':
            if combonfsw.get()== "attiva NSFW":
                if CointsLivel>=5000 and CointsLivel< 10000:
                    prompt = f"1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, detailed facial features,{random.choice(bondagearrays)} {pube}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality,{pussyclose_up}<lora:K4l3yCu0c0:1.0>"
                else:
                    comblist= azionebillie+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube}, {random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality,{pussyclose_up}<lora:K4l3yCu0c0:1.0>"""
            else:
                if CointsLivel>= 5000 and CointsLivel < 10000:
                    print("Outfit INTIMO")
                    prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, 
detailed facial features, {random.choice(intimi)}, {random.choice(azionebillie)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality<lora:K4l3yCu0c0:1.0>"""
                elif CointsLivel>= 10000:
                    comblist= azionebillie+azionistregheNSFW
                    prompt = f"""(totalmente nuda:1.9),(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, 
detailed facial features, {random.choice(outfit_nsfw)},{pube}, {random.choice(comblist)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality,{pussyclose_up}<lora:K4l3yCu0c0:1.0>"""
                else:
                    if comboModelgen.get()=='bondage':
                        prompt = f"1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, detailed facial features,{random.choice(bondagearrays)} {pube}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality,{pussyclose_up}<lora:K4l3yCu0c0:1.0>"
                    else:
                        prompt = f"""(RAW, analogue, award-winning photograph), ((best quality)), ((masterpiece)), ((realistic)), 1girl, solo, (((K4l3yCu0c0))), 18 years old, long blonde hair, light green eyes, 
detailed facial features, {random.choice(outfitbillie)}, {random.choice(azionebillie)}, {random.choice(locationstr)}, professional Photography, Photorealistic, detailed, sharp focus, 8k, HD, high quality<lora:K4l3yCu0c0:1.0>"""
        else:
             prompt= traduci(testo.get("1.0", "end-1c").strip())   
             prompt= "1girl,solo,(((K4l3yCu0c0))),"+ prompt+"<lora:K4l3yCu0c0:1.0>"
             print(f"personale prompt: {prompt}")
             
        if lora== False:
            pipe.load_lora_weights(".\\Lora\\k4l3yc.safetensors", weight_name="k4l3yc.safetensors", adapter_name="k4l3yc")
            lora=True
        selviso= os.path.join(".\\faces_streghe\\billie",random.choice([viso for viso in os.listdir(".\\faces_streghe\\billie")])) 
        
    compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
    if testo.get("1.0", "end-1c").strip()=='':
        conditioning = compel(traduci(prompt))
    else:
        conditioning = compel(traduci(testo.get("1.0", "end-1c")))
    negative_conditioning = compel(traduci(testonegative.get("1.0", "end-1c")))
    [conditioning, negative_conditioning] = compel.pad_conditioning_tensors_to_same_length([conditioning, negative_conditioning])
    if combonfsw== "attiva NSFW":
            pipe.safety_checker = None
            pipe.requires_safety_checker = False
    with autocast(), torch.inference_mode():
        image = pipe(prompt_embeds=conditioning, negative_propmt_embeds=negative_conditioning,width=960,height=720,num_inference_steps=int(50),guidance_scale=float(7)).images[0]
        image.save("imghidden.jpg")
        
        #reface_Actor
        if os.path.exists(".\\swapseed\\generato.jpg"):
            os.remove(".\\swapseed\\generato.jpg")
        shutil.copyfile(".\\imghidden.jpg",".\\swapseed\\generato.jpg")
        if os.path.exists(".\\swapseed\\volto.jpg"):
            os.remove(".\\swapseed\\volto.jpg")
        shutil.copyfile(selviso,".\\swapseed\\volto.jpg")
        os.chdir("swapseed")
        os.system("python main.py")
        time.sleep(1)
        imaggen = Image.open(".\\generatedimagewithface.png")
        imaggen.thumbnail((960,720))
        imaggen.save("..\\imghidden.jpg")
        os.chdir("..")
        #shutil.move(".\\swapseed\\generatedimagewithface.png",".\\imghidden.jpg")
        
        
        
        
        
        
modelXL= "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
difInp="runwayml/stable-diffusion-inpainting"
modelrealistvision6inp= "stablediffusionapi/realistic-vision-v6.0-b1-inpaint"
f222nsfwinpaintingsd= ".\\model\\f22_nsfw\\f222-nsfw-inpainting.ckpt"

Imgload= None
dirload=None
ik=0
arrayphotos= []
#selectModelInp= ttk.Combobox(frameInpaint,values=['Stable Diffuser XL1.0 Inpainting','Stable Diffusion Inpainting','Realistic Vision V6B1 Inpaint','f222 nsfw Inpainting'],font=customFont)
def inpainting():
    global Imgload,dirload,model_id,difInp,modelrealistvision6inp,f222nsfwinpaintingsd,arrayphotos,ik,selectModelInp
    print("inpainting")
    if Imgload!= None:
        inputfoto= Imgload
    elif dirload!= None:
        inputfoto= os.path.join(dirload, arrayphotos[ik])
        ik=ik+1
    if os.path.exists(inputfoto):
        shutil.copyfile(inputfoto,".\\huggingface-cloth-segmentation\\input.jpg") 
    os.chdir('huggingface-cloth-segmentation')
    os.system("python process.py --image input.jpg")
    os.chdir("..")
    # Apri l'immagine
    img = Image.open(".\\huggingface-cloth-segmentation\\output\\cloth_seg\\final_seg.png")
    # Converti l'immagine in RGB
    img = img.convert("RGB")
    # Ottieni le dimensioni dell'immagine
    width, height = img.size
    # Crea una nuova immagine con le stesse dimensioni
    new_img = Image.new("RGB", (width, height))
    # Scansiona ogni pixel dell'immagine
    for x in range(width):
        for y in range(height):
            # Ottieni il colore del pixel corrente
            r, g, b = img.getpixel((x, y))
            # Se il colore non è nero, rendilo bianco
            if (r, g, b) != (0, 0, 0):
                new_img.putpixel((x, y), (255, 255, 255))
            else:
                new_img.putpixel((x, y), (0, 0, 0))
    # Salva la nuova immagine
    new_img.save("mask.png")    
    # Crea un kernel di dimensioni 10x10 pieno di 1
    kernel = np.ones((10,10),np.uint8)
    # Converti l'immagine PIL in un array numpy
    new_img_np = np.array(new_img)
    # Espande la maschera bianca esternamente di 10 pixel
    mask_dilated = cv2.dilate(new_img_np, kernel, iterations = 1)
    # Salva la nuova immagine
    cv2.imwrite("maskext.jpg", mask_dilated)

    #inpainting
    prompttxt= "A girl, (completely naked:1.9), (naked breasts:1.9), (aroused nipples:1.9), (((shows wet pussy)),((pussy, uncensored)), ((pussy juice))clitoris:1.9)."
    def add_padding(img, expected_size):
        delta_width = expected_size[0] - img.size[0]
        delta_height = expected_size[1] - img.size[1]
        padding = (delta_width//2, delta_height//2, delta_width-(delta_width//2), delta_height-(delta_height//2))
        return ImageOps.expand(img, padding)
    # Apri l'immagine di input e ridimensionala
    inpImage = Image.open(inputfoto)
    inpImage.thumbnail((960, 720))
    inpImage = add_padding(inpImage, (960, 720))
    # Apri la maschera e ridimensionala
    maskinp = Image.open('maskext.jpg')
    maskinp.thumbnail((960, 720))
    maskinp = add_padding(maskinp, (960, 720))
    if selectModelInp.get()== 'Stable Diffuser XL1.0 Inpainting':
        pipe = AutoPipelineForInpainting.from_pretrained(modelXL,use_safetensors=True,torch_dtype=torch.float16) 
        pipe.scheduler = DPMSolverSDEScheduler.from_config(pipe.scheduler.config) 
        pipe.safety_checker = None
        pipe.requires_safety_checker = False
        pipe.to('cuda')
        w,h= inpImage.size
        imageinp = pipe(prompt=prompttxt, image=inpImage, mask_image=maskinp,width=w,height=h,num_inference_steps=int(20), guidance_scale=float(8.0),strength= float(0.95),eta= float(1.0)).images[0]
        imageinp.save("imghidden.jpg")
        #stable diffuser
    elif selectModelInp.get()== 'Stable Diffusion Inpainting':
            pipe = StableDiffusionInpaintPipeline.from_pretrained(difInp,revision="fp16",
            torch_dtype=torch.float16,) 
            pipe.scheduler = DPMSolverSDEScheduler.from_config(pipe.scheduler.config) 
            pipe.safety_checker = None
            pipe.requires_safety_checker = False
            pipe.to('cuda')
            w,h= inpImage.size
            imageinp = pipe(prompt=prompttxt, image=inpImage, mask_image=maskinp,width=w,height=h,num_inference_steps=int(20), guidance_scale=float(8.0),strength= float(0.99),eta= float(1.0)).images[0]
            imageinp.save("imghidden.jpg")
    #realistic
    elif selectModelInp.get()=='Realistic Vision V6B1 Inpaint':
            pipe = AutoPipelineForInpainting.from_pretrained(modelrealistvision6inp,use_safetensors=True,torch_dtype=torch.float16) 
            pipe.scheduler = DPMSolverSDEScheduler.from_config(pipe.scheduler.config) 
            pipe.safety_checker = None
            pipe.requires_safety_checker = False
            pipe.to('cuda')
            w,h= inpImage.size
            imageinp = pipe(prompt=prompttxt, image=inpImage, mask_image=maskinp,width=w,height=h,num_inference_steps=int(20), guidance_scale=float(8.0),strength= float(0.99),eta= float(1.0)).images[0]
            imageinp.save("imghidden.jpg")
    elif selectModelInp.get()=='f222 nsfw Inpainting':
            pipe = StableDiffusionInpaintPipeline.from_single_file(f222nsfwinpaintingsd,use_safetensors=True,torch_dtype=torch.float16) 
            pipe.scheduler = DPMSolverSDEScheduler.from_config(pipe.scheduler.config) 
            pipe.safety_checker = None
            pipe.requires_safety_checker = False
            pipe.to('cuda')
            w,h= inpImage.size
            imageinp = pipe(prompt=prompttxt, image=inpImage, mask_image=maskinp,width=w,height=h,num_inference_steps=int(20), guidance_scale=float(8.0),strength= float(0.99),eta= float(1.0)).images[0]
            imageinp.save("imghidden.jpg")
            
        

def genera_image():
    global cfg, steps, testo, testonegative, frame, photo, prompt, azione, outfit, location, capelli, occhi, inquadratura, cucina, sala_da_pranzo, camera_da_letto, bagno, salotto, mansarda, esterno_piscina, college_americano, ufficio, fastfood
    global capelli, occhi, combonfsw, selez_stregha, selviso, Imgload, dirload, comboModelgen, CointsLivel, bondagearrays
    global bondage, StableDiffusion2, diffusionXLbase10, Realistic_Vision_V60_B1_noVAE, NSFW, pipe, pube, pussyclose_up

    if (comboModelgen.get() == 'bondage') or (combonfsw.get() == "attiva NSFW" and CointsLivel == 5000):
        pipe = StableDiffusionPipeline.from_single_file(bondage, torch_dtype=torch.float16)
    elif comboModelgen.get() == 'diffuserXL':
        pipe = AutoPipelineForText2Image.from_pretrained(diffusionXLbase10, torch_dtype=torch.float16)
    elif comboModelgen.get() == 'diffuser1.5':
        pipe = AutoPipelineForText2Image.from_pretrained(StableDiffusion15, torch_dtype=torch.float16)
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    elif comboModelgen.get() == 'realistic vision v6':
        pipe = AutoPipelineForText2Image.from_pretrained(Realistic_Vision_V60_B1_noVAE, torch_dtype=torch.float16)
    elif comboModelgen.get() == 'nsfw':
        pipe = AutoPipelineForText2Image.from_pretrained(NSFW, torch_dtype=torch.float16)

    pipe.to("cuda")
    pipe.safety_checker = None
    pipe.requires_safety_checker = False

    if Imgload is not None or dirload is not None:
        print("inpainting")
        inpainting()
    elif selez_stregha.get() not in ['+ Melody', 'Personalizzato']:
        Streghe()
    else:
        prompt_text = testo.get("1.0", "end-1c").strip()
        
        if prompt_text == '':
            if selez_stregha.get() == '+ Melody':
                generateprompt()
                time.sleep(2)
                if combonfsw.get() == 'attiva NSFW':
                    if 5000 <= CointsLivel < 10000:
                        prompt = f"(fotorealismo:1.9),(1girl:1.9),(solo:1.9),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(terza di seno:1.8),(capezzoli eccitati:1.8),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),{random.choice(bondagearrays)},({random.choice(pube)}:1.8),(buco del culo:1.8),{pussyclose_up}"
                    else:   
                        if azione in ['lei fa la doccia', 'lei si insapona nella doccia']:
                            prompt = f"(fotorealismo:1.9),(location:{location}:1.9),(totalmente nuda:1.9),(1girl:1.9),(solo:1.9),(inquadratura{random.choice(inquadratura)}:1.8),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(terza di seno:1.8),(capezzoli eccitati:1.8),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),(lei è totalmente nuda:1.9),({azione}:1.9),({random.choice(pube)}:1.8),(buco del culo:1.8),{pussyclose_up}"
                        else:
                            prompt = f"(fotorealismo:1.9),(location:{location}:1.9),(totalmente nuda:1.9),(1girl:1.9),(solo:1.9),({random.choice(inquadratura)}:1.8),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(terza di seno:1.8),(capezzoli eccitati:1.8),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),({outfit}:1.9),({azione}:1.9),({random.choice(pube)}:1.8),(buco del culo:1.8)"
                else:  
                    if comboModelgen.get() == 'bondage':
                        prompt = f"(fotorealismo:1.9),(1girl:1.9),(solo:1.9),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(terza di seno:1.8),(capezzoli eccitati:1.8),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),{random.choice(bondagearrays)},({random.choice(pube)}:1.8),(buco del culo:1.8),{pussyclose_up}"
                        print("BONDAGE")
                    else:
                        if azione in ['lei fa la doccia', 'lei si insapona nella doccia']:
                            print(f"AZIONE MELODY {azione}")
                            prompt = f"(fotorealismo:1.9),(location:{location}:1.9),(1girl:1.9),(solo:1.9),(inquadratura {random.choice(inquadratura)}:1.8),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(terza di seno:1.8),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),({azione},lei è totalmente nuda:1.9),{pussyclose_up}"
                        else:
                            print(f"AZIONE MELODY {azione}")
                            prompt = f"(fotorealismo:1.9),(location:{location}:1.9),(1girl:1.9),(solo:1.9),({random.choice(inquadratura)}:1.8),(una ragazza di 17 anni:1.9),(viso angelico:1.8),(americana:1.9),(capelli {random.choice(capelli)}:1.9),(occhi {random.choice(occhi)}:1.9),(labbra carnose:1.7),({azione},indossa {outfit}:1.9)"
            elif selez_stregha.get() == 'Personalizzato':
                messagebox.showinfo("Attenzione", "Inserisci Un prompt")
                return  # Usa 'return' invece di 'esc_funzione'
        else:
            prompt = prompt_text

        negative_prompt = testonegative.get("1.0", "end-1c")
        
        print(prompt)

        if comboModelgen.get() == 'diffuserXL':
            encoded_output = pipe.encode_prompt(
            prompt=traduci(prompt),
            negative_prompt=traduci(negative_prompt),
            device=pipe.device,
            num_images_per_prompt=1,
            do_classifier_free_guidance=True
        )
            if isinstance(encoded_output, tuple) and len(encoded_output) == 2:
                prompt_embeds, pooled_prompt_embeds = encoded_output
            elif isinstance(encoded_output, dict):
                prompt_embeds = encoded_output.get('prompt_embeds')
                pooled_prompt_embeds = encoded_output.get('pooled_prompt_embeds')
            else:
                raise ValueError("Unexpected output format from encode_prompt")
        else:
            compel = Compel(tokenizer=pipe.tokenizer, text_encoder=pipe.text_encoder)
            conditioning = compel(traduci(prompt))
            negative_conditioning = compel(traduci(negative_prompt))
            [conditioning, negative_conditioning] = compel.pad_conditioning_tensors_to_same_length([conditioning, negative_conditioning])

        if combonfsw.get() == "attiva NSFW":
            pipe.safety_checker = None
            pipe.requires_safety_checker = False

        with autocast(), torch.inference_mode():
            if comboModelgen.get() == 'diffuserXL':
                image = pipe(
                    prompt_embeds=prompt_embeds,
                    pooled_prompt_embeds=pooled_prompt_embeds,
                    width=960,
                    height=720,
                    num_inference_steps=int(steps.get()),
                    guidance_scale=float(cfg.get()) 
                ).images[0]
            else:
                image = pipe(
                    prompt_embeds=conditioning, 
                    negative_prompt_embeds=negative_conditioning,
                    width=960,
                    height=720,
                    num_inference_steps=int(steps.get()),
                    guidance_scale=float(cfg.get())
                ).images[0]

        image.save("imghidden.jpg")
                
            
        #reface_Actor
        selviso= os.path.join(".\\faces_streghe\\melody",random.choice([viso for viso in os.listdir(".\\faces_streghe\\melody")])) 
        if os.path.exists(".\\swapseed\\generato.jpg"):
            os.remove(".\\swapseed\\generato.jpg")
        shutil.copyfile(".\\imghidden.jpg",".\\swapseed\\generato.jpg")
        if os.path.exists(".\\swapseed\\volto.jpg"):
            os.remove(".\\swapseed\\volto.jpg")
        shutil.copyfile(selviso,".\\swapseed\\volto.jpg")
        os.chdir("swapseed")
        os.system("python main.py")
        time.sleep(1)
        imaggen = Image.open(".\\generatedimagewithface.png")
        imaggen.thumbnail((960,720))
        imaggen.save("..\\imghidden.jpg")
        os.chdir("..")
        #shutil.move(".\\swapseed\\generatedimagewithface.png",".\\imghidden.jpg")
        

demonepath= ".\\animazionidemon\\belthazor\\belthazor00.png"
demonepath2= ".\\animazionidemon\\grimlock\\grimlock00.png"
demonepath3= ".\\animazionidemon\\hakate\\hekate00.png"
demonepath4= ".\\animazionidemon\\javna\\javna00.png"
demonepath5= ".\\animazionidemon\\wig\\wig00.png"

belthazorimage = None  # Aggiungi questa linea
grimlock=None
hakate=None
javna=None
wing= None

velocitay=random.randrange(0,720)
velocitax=random.randrange(0,960)
velocitay2=random.randrange(0,720)
velocitax2=random.randrange(0,960)
velocitay3=random.randrange(0,720)
velocitax3=random.randrange(0,960)
velocitay4=random.randrange(0,720)
velocitax4=random.randrange(0,960)
velocitay5=random.randrange(0,720)
velocitax5=random.randrange(0,960)
ymarcia=1
xmarcia=1
ymarcia2=1
xmarcia2=1
ymarcia3=1
xmarcia3=1
ymarcia4=1
xmarcia4=1
ymarcia5=1
xmarcia5=1
limitey=int(720)
limitex=int(960)
rdirezione=10
rdirezione2=10
rdirezione3=10
rdirezione4=10
rdirezione5=10
speed=10
# Aggiungi questa linea all'inizio del tuo codice
ultimo_aggiornamento = time.time()
tkimage=[]

pointsselect= []
seleziona= False
rettangolo_temp = None
goldsframes=[]
gold=None
k=0
colpo=False



windows = tk.Tk()
windows.attributes('-fullscreen', True)  # Avvia la finestra in modalità schermo intero
for i in range(0,51):
    if i< 10:
         gold= Image.open(f".\\gold\\particulare\\pg_0000{i}.png").convert('RGBA')
    else:
        gold= Image.open(f".\\gold\\particulare\\pg_000{i}.png").convert('RGBA')
    gold= gold.resize((100,100),Image.LANCZOS)
    gold = ImageTk.PhotoImage(gold)  # Converti l'oggetto PIL Image in PhotoImage
    goldsframes.append(gold) 


def disegnaselezione(even):
    global frame,seleziona,rettangolo_temp,gold,k,goldsframes,IMMAGINENASCOSTA,SFONDO,velocitax,velocitax2,velocitax3,velocitax4,velocitax5,velocitay,velocitay2,velocitay3,velocitay4,velocitay5,VITA,labvita,labvita,VitaBar,colpo,pixels_svelati,immagintrasp,tkimage,windows,pointsselect
    global livel,grimlock,hakate,javna,wing,ymarcia2,velocitax2,xmarcia2,rdirezione2,velocitay2,ymarcia3,velocitax3,xmarcia3,rdirezione3,velocitay3,ymarcia4,velocitax4,xmarcia4,rdirezione4,velocitay4,rdirezione4,ymarcia5,velocitax5,xmarcia5,rdirezione5,velocitay5,rdirezione5
    global CointsLivel,Totalconits,totprogrconits_level,labconits
    try:
        
        if VITA<= 0:
            pygame.init()

            # Carica il video
            clip = VideoFileClip('.\\gameover.mp4')

            # Crea una finestra della dimensione del video
            pygame.display.set_mode((clip.size[0], clip.size[1]))

            # Riproduci il video
            clip.preview()

            pygame.quit()

            print("ricomincio livello")
            # game over
            #reset variabili
            VITA= 100
            CointsLivel=0
            tkimage=[]
            pointsselect= []
            pixels_svelati=[]
            seleziona= False
            rettangolo_temp = None
            colpo=False
            immagintrasp= Image.new('RGBA', (960,720), (0, 0, 0, 0))
            labvita.config(text=f"Vita: {VITA}", font="Imperial",foreground= "red")
            VitaBar.configure(value=VITA)  # Usa 'configure' invece di 'set'
            windows.update_idletasks()
            #genera nuova immagine castello
            generacastelli()
            SFONDO= Image.open("castello.png")
            IMMAGINENASCOSTA= Image.open('imghidden.jpg')
            try:
                # Cancella il canvas
                frame.delete('all')

                # Crea la nuova immagine

                tkimage.append(ImageTk.PhotoImage(SFONDO))
                
                # Ora aggiungi l'immagine al canvas
                frame.create_image((960 // 2, 720 // 2), image=tkimage[-1])
                frame.update()
                # Forza un aggiornamento dell'interfaccia utente
                windows.update_idletasks()

            except Exception as error:
                print(f"errore: {error}")
            print(f"direzione: {velocitax},{velocitay}")
    except Exception as  errorg:
        print(f"error game over {errorg}")
    # Controlla se è passato almeno 1 secondo dall'ultimo contatto
    if abs(even.x - velocitax) <= 2 or abs(even.y - velocitay) <= 2 or abs(even.x - velocitax2) <= 2 or abs(even.y - velocitay2) <= 2 or abs(even.x - velocitax3) <= 2 or abs(even.y - velocitay3) <= 2 or abs(even.x - velocitax4) <= 2 or abs(even.y - velocitay4) <= 2 or abs(even.x - velocitax5) <= 2 or abs(even.y - velocitay5) <= 2:
            # Calcola la quantità di vita da sottrarre
        if livel< 20:
            vita_da_sottrarre =int(math.ceil(1 * math.log(livel + 1)))
        elif livel>= 20 and  livel < 30:
            vita_da_sottrarre =int(math.ceil(2 * math.log(livel + 1)))
        elif livel>= 30 and  livel < 40:
                vita_da_sottrarre =int(math.ceil(3 * math.log(livel + 1)))
        elif livel>= 40 and  livel < 50:
                vita_da_sottrarre =int(math.ceil(4 * math.log(livel + 1)))
        elif livel>= 50 and  livel < 60:
                vita_da_sottrarre =int(math.ceil(5 * math.log(livel + 1)))
        elif livel>= 60 and  livel < 70:
                vita_da_sottrarre =int(math.ceil(6 * math.log(livel + 1)))
        elif livel>= 70 and  livel <80:
            vita_da_sottrarre =int(math.ceil(7 * math.log(livel + 1)))
        elif livel>= 80 and  livel < 90:
                vita_da_sottrarre =int(math.ceil(8 * math.log(livel + 1)))
        elif livel>= 90 and  livel < 100:
                vita_da_sottrarre =int(math.ceil(9 * math.log(livel + 1)))
        elif livel== 100:  
                vita_da_sottrarre =int(math.ceil(10 * math.log(livel + 1)))
             

        if VITA > 0 and colpo == False:
            VITA = max(VITA - vita_da_sottrarre, 0)
            print(f"vita: {VITA}")
            labvita.config(text=f"Vita: {VITA}", font="Imperial",foreground= "red")
            VitaBar.configure(value=VITA)  # Usa 'configure' invece di 'set'
            windows.update_idletasks()
            # Aggiorna l'ultimo contatto al tempo corrente
            colpo= True    
    else:
        colpo=False
       
    if seleziona == True:
        print("selezione")
        # point             x=[0],y=[1] 
        pointsselect.append((even.x, even.y))
        print(f"POINT SELECT: {pointsselect}")
        if len(pointsselect) >= 2:
            x1, y1 = pointsselect[0]
            x2, y2 = pointsselect[-1]
            box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            sum_points = sum(sum(point) for point in pointsselect)
            CointsLivel += int(math.log(sum_points))
            if CointsLivel > 10000:
                CointsLivel = 10000
            totprogrconits_level['value'] = CointsLivel
            totprogrconits_level.update()
            totprogrconits['value'] = Totalconits  # Qui ho corretto l'errore
            totprogrconits.update()
            labconits.config(text=f"Total coins: {Totalconits} Coins Level: {CointsLivel}", style="Gold.TLabel")
            labconits.update()
            
            # Cancella il rettangolo temporaneo precedente
            if rettangolo_temp:
                frame.delete(rettangolo_temp)
                
            # Crea un nuovo rettangolo temporaneo
            rettangolo_temp = frame.create_rectangle(*box, outline='gold', width=3)
            frame.create_image((even.x,even.y), image=goldsframes[k])  # Specifica il parametro 'image'
            if k< 50:
                k=k+1
            else:
                k=0

            
            

def attivadisegno(even):
    global seleziona
    seleziona= True
    print("disegno")
pixels_svelati=[]

# Carica la chiave da un file
def load_key():
    return open("secret.key", "rb").read()

# Decripta il file
def decrypt_file(encrypted_file_path, key):
    fernet = Fernet(key)
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(encrypted_file_path.replace(".encrypted", ""), "wb") as decrypted_file:
        decrypted_file.write(decrypted)
        
 

VITA= 100
# Inizializza un'immagine trasparente
immagintrasp = Image.new('RGBA', (960,720), (0, 0, 0, 0))
def resetpoints(even):
    global pointsselect,seleziona,rettangolo_temp,IMMAGINENASCOSTA,SFONDO,belthazorimage,velocitax,velocitay,immagintrasp,VITA,colpo,speed,immagintrasp,frame,tkimage,pixels_svelati,livel,labLivel
    global grimlock,hakate,javna,wing,ymarcia2,velocitax2,xmarcia2,rdirezione2,velocitay2,ymarcia3,velocitax3,xmarcia3,rdirezione3,velocitay3,ymarcia4,velocitax4,xmarcia4,rdirezione4,velocitay4,rdirezione4,ymarcia5,velocitax5,xmarcia5,rdirezione5,velocitay5,rdirezione5
    global CointsLivel,Totalconits
    print("resetta punti")
    seleziona=False
    # Crea un rettangolo permanente quando rilasci il pulsante del mouse
    if len(pointsselect) >= 2:
        frame.create_rectangle(pointsselect[0][0],pointsselect[0][1],pointsselect[-1][0],pointsselect[-1][1],outline='gold' ,width=3)
        # quando viene rilasciato il pulsante 1 copia i pixel del immagine nascosta che ha le stesse dimenzioni del immagine sfondo, sul immagine sfindo in modo da creare effetto da rivelare immagine celata dietro lo sfondo 
        x1, y1 = pointsselect[0]
        x2, y2 = pointsselect[-1]
        box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
         # Ritaglia la porzione di IMMAGINENASCOSTA che corrisponde al box
        IMMAGINENASCOSTA_cropped = IMMAGINENASCOSTA.crop(box)
        pixels_svelati.append((IMMAGINENASCOSTA_cropped, box))
        immagintrasp.paste(IMMAGINENASCOSTA_cropped, box)
        # cv2.imshow('Image', np.array(immagintrasp))
        if np.all(np.array(immagintrasp)[:,:,3] != 0) and VITA > 0:
            print("VITTORIA")
            if livel == 100:
                file = ".//Charmed_Inedity_interviste_720[ITA].mp4.encrypted"
                if os.path.exists(file):
                    key = load_key()
                    decrypt_file(file, key)
                    print("File decriptato con successo.")
                    time.sleep(1)
                    decrypted_file = "Charmed_Inedity_interviste_720[ITA].mp4.encrypted".replace('.encrypted','')
                    if os.path.exists(decrypted_file):
                       os.startfile(decrypted_file)
                       sys.exit()
                        
                else:
                    print("Errore: file non trovato")
                    sys.exit()
                
            else:
                Totalconits += CointsLivel
                if Totalconits > 1000000:
                    Totalconits = 1000000
                pygame.init()
                # Carica il video
                clip = VideoFileClip('.\\winner.mp4')
                # Crea una finestra della dimensione del video
                pygame.display.set_mode((clip.size[0], clip.size[1]))
                # Riproduci il video
                clip.preview()
                pygame.quit()
                print("continuo")
                # next Livel
                livel= livel+1
                labLivel.config(text=f"Livello {livel}", font="Impac", fg="blue")
                labLivel.update()
                print(f"livel {livel}")
                #reset variabili
                VITA= 100
                CointsLivel=0
                tkimage=[]
                pointsselect= []
                pixels_svelati=[]
                seleziona= False
                rettangolo_temp = None
                colpo=False
                immagintrasp= Image.new('RGBA', (960,720), (0, 0, 0, 0))
                labvita.config(text=f"Vita: {VITA}", font="Imperial",foreground= "red")
                VitaBar.configure(value=VITA)  # Usa 'configure' invece di 'set'
                windows.update_idletasks()
                # genera nuova immagine nascosta
                genera_image()
                #genera nuova immagine castello
                generacastelli()
                #aumenta velocita mostri
                if speed< 1000: 
                    speed= speed*2
                if speed> 1000:
                    speed=1000
                SFONDO= Image.open("castello.png")
                IMMAGINENASCOSTA= Image.open('imghidden.jpg')
                try:
                    # Cancella il canvas
                    frame.delete('all')

                    # Crea la nuova immagine

                    tkimage.append(ImageTk.PhotoImage(SFONDO))
                    
                    # Ora aggiungi l'immagine al canvas
                    frame.create_image((960 // 2, 720 // 2), image=tkimage[-1])
                    frame.update()
                    # Forza un aggiornamento dell'interfaccia utente
                    windows.update_idletasks()

                except Exception as error:
                    print(f"errore: {error}")
                print(f"direzione: {velocitax},{velocitay}")
            
            
        pointsselect=[]
        rettangolo_temp = None
        # poi copia immagine demone sopra a tutto e aggiorna la canvas
        try:
            # Cancella il canvas
            frame.delete('all')
            # Incolla tutte le aree rivelate su SFONDO
            
            SFONDO.paste(immagintrasp, (0.0))
            # Incolla l'immagine
            SFONDO.paste(belthazorimage, (velocitax, velocitay), belthazorimage)
            SFONDO.paste(grimlock, (velocitax2, velocitay2), grimlock)
            SFONDO.paste(hakate,(velocitax3, velocitay3), hakate)
            SFONDO.paste(javna, (velocitax4, velocitay4), javna)
            SFONDO.paste(wing, (velocitax5, velocitay5), wing)
            tkimage.append(ImageTk.PhotoImage(SFONDO))
            # Crea l'immagine nel centro del canvas
            frame.create_image((960//2, 720//2), image=tkimage[-1])
            
        except Exception as error:
            print(f"errore: {error}")

        print(f"direzione: {velocitax},{velocitay}")
        frame.update()

    
    
    
    
    
def gioca():
    global demonepath, velocitay, limitex,limitey,frame, belthazorimage,ymarcia,velocitax,xmarcia,rdirezione,ultimo_aggiornamento
    global SFONDO,IMMAGINENASCOSTA,frame,speed,pixels_svelati,VITA,labvita,VitaBar
    global grimlock,hakate,javna,wing,ymarcia2,velocitax2,xmarcia2,rdirezione2,velocitay2,ymarcia3,velocitax3,xmarcia3,rdirezione3,velocitay3,ymarcia4,velocitax4,xmarcia4,rdirezione4,velocitay4,rdirezione4,ymarcia5,velocitax5,xmarcia5,rdirezione5,velocitay5,rdirezione5

    SFONDO= Image.open("castello.png")
    IMMAGINENASCOSTA= Image.open('imghidden.jpg')
    
    
    labvita.config(text=f"Vita: {VITA}", font="Imperial",foreground= "red")
    VitaBar.configure(value=VITA)  # Usa 'configure' invece di 'set'
    windows.update_idletasks()
    
    
    # Aggiorna rdirezione solo se sono passati 10 secondi
    if time.time() - ultimo_aggiornamento >= 10:
        rdirezione = random.randrange(0, 100)
        rdirezione2 = random.randrange(0, 100)
        rdirezione3 = random.randrange(0, 100)
        rdirezione4 = random.randrange(0, 100)
        rdirezione5 = random.randrange(0, 100)
        ultimo_aggiornamento = time.time()
    
    print("gioca")
    belthazorimage = Image.open(demonepath).convert('RGBA')
    grimlock=Image.open(demonepath2).convert('RGBA')
    hakate=Image.open(demonepath3).convert('RGBA')
    javna=Image.open(demonepath4).convert('RGBA')
    wing= Image.open(demonepath5).convert('RGBA')
    
    #demone1
    #divisibile  per 5 con resto 0
    if rdirezione % 5==0:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if ymarcia==1 and velocitay<limitey:
            velocitay=velocitay+speed
        else:
            ymarcia=0
        if ymarcia==0 and velocitay>0:
            velocitay=velocitay-speed
        else:
            ymarcia=1 
    else:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if xmarcia==1 and velocitax<limitex:
            velocitax=velocitax+speed
        else:
            xmarcia=0
        if xmarcia==0 and velocitax>0:
            velocitax=velocitax-speed
        else:
            xmarcia=1
    #demone2
    #divisibile  per 5 con resto 0
    if rdirezione2 % 5==0:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if ymarcia2==1 and velocitay2<limitey:
            velocitay2=velocitay2+speed
        else:
            ymarcia2=0
        if ymarcia2==0 and velocitay2>0:
            velocitay2=velocitay2-speed
        else:
            ymarcia2=1 
    else:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if xmarcia2==1 and velocitax2<limitex:
            velocitax2=velocitax2+speed
        else:
            xmarcia2=0
        if xmarcia2==0 and velocitax2>0:
            velocitax2=velocitax2-speed
        else:
            xmarcia2=1 
    #demone3
    #divisibile  per 5 con resto 0
    if rdirezione3 % 5==0:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if ymarcia3==1 and velocitay3<limitey:
            velocitay3=velocitay3+speed
        else:
            ymarcia3=0
        if ymarcia3==0 and velocitay3>0:
            velocitay3=velocitay3-speed
        else:
            ymarcia3=1 
    else:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if xmarcia3==1 and velocitax3<limitex:
            velocitax3=velocitax3+speed
        else:
            xmarcia3=0
        if xmarcia3==0 and velocitax3>0:
            velocitax3=velocitax3-speed
        else:
            xmarcia3=1 
    #demone4
    #divisibile  per 5 con resto 0
    if rdirezione4 % 5==0:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if ymarcia4==1 and velocitay4<limitey:
            velocitay4=velocitay4+speed
        else:
            ymarcia4=0
        if ymarcia4==0 and velocitay4>0:
            velocitay4=velocitay4-speed
        else:
            ymarcia4=1 
    else:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if xmarcia4==1 and velocitax4<limitex:
            velocitax4=velocitax4+speed
        else:
            xmarcia4=0
        if xmarcia4==0 and velocitax4>0:
            velocitax4=velocitax4-speed
        else:
            xmarcia4=1 
    #demone5
    #divisibile  per 5 con resto 0
    if rdirezione5 % 5==0:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if ymarcia5==1 and velocitay5<limitey:
            velocitay5=velocitay5+speed
        else:
            ymarcia5=0
        if ymarcia5==0 and velocitay5>0:
            velocitay5=velocitay5-speed
        else:
            ymarcia5=1 
    else:
        # Inverti la direzione se il mostro ha raggiunto il bordo del canvas
        if xmarcia5==1 and velocitax5<limitex:
            velocitax5=velocitax5+speed
        else:
            xmarcia5=0
        if xmarcia5==0 and velocitax5>0:
            velocitax5=velocitax5-speed
        else:
            xmarcia5=1 
    try:
        # Cancella il canvas
        frame.delete('all')
       
        # Incolla l'immagine
        for img, box in pixels_svelati:
                SFONDO.paste(img, box)
        SFONDO.paste(belthazorimage, (velocitax, velocitay), belthazorimage)
        SFONDO.paste(grimlock, (velocitax2, velocitay2), grimlock)
        SFONDO.paste(hakate,(velocitax3, velocitay3), hakate)
        SFONDO.paste(javna, (velocitax4, velocitay4), javna)
        SFONDO.paste(wing, (velocitax5, velocitay5), wing)
        tkimage.append(ImageTk.PhotoImage(SFONDO))
        # Crea l'immagine nel centro del canvas
        frame.create_image((960//2, 720//2), image=tkimage[-1])
        
    except Exception as error:
        print(f"errore: {error}")
    
    print(f"direzione: {velocitax},{velocitay}")
    frame.update()

   #attiva selezione
    windows.bind('<Button-1>',attivadisegno)
    windows.bind('<ButtonRelease-1>',resetpoints)
    #rileva movimento mouse
    windows.bind('<Motion>', disegnaselezione)
    # Ripeti la funzione dopo 20 millisecondi
    windows.after(10, gioca)
    
    
# Crea un dizionario di stili di castelli
stile_castelli = ["medieval", "antique", "nineteenth-century", "Roman", "Gothic", "Renaissance", "Baroque", "Rococo", "neoclassical", "Victorian", "Edwardian", "art nouveau", "art deco", "modernist", "brutalist", "postmodern", "deconstructivist", "futurist", "minimalist", "high-tech"]
def generacastelli():
    global stile_castelli,negative
    selctcastello= random.choice(stile_castelli)
    nfinestre = random.randint(5, 20)
    ntorri = random.randint(5, 20)
    
    
    # Genera un'immagine di un castello
    promptcast =f"((close frontal shot)),a {selctcastello} castle with {nfinestre} windows and {ntorri} towers frontal view,((open windows)),((large windows))"
    result = pipe(promptcast, negative_prompt=negative, width=960, height=720, num_inference_steps=30, guidance_scale=7.5)
    imagecast = result.images[0]
    # Salva l'immagine
    imagecast.save(f"castello.png")
    
def inizializzagioco():
    global SFONDO,IMMAGINENASCOSTA,frame
    print("inizializza gioco")   
    genera_image()
    generacastelli()
    SFONDO= Image.open("castello.png")
    IMMAGINENASCOSTA= Image.open('.\\imghidden.jpg')
    gioca()
    
    

def visualizzaimaginegenerata():
    global frame,photo
    
    genera_image()
    # Carica l'immagine con PIL e convertila in RGB
    image = Image.open(".\\imghidden.jpg").convert("RGB")

    # Crea un PhotoImage da un'immagine PIL
    photo.append(ImageTk.PhotoImage(image))

    # Aggiungi l'immagine al canvas
    frame.create_image(0, 0, image=photo[-1], anchor="nw")
    frame.update()

from tkinter import font as tkFont 
    
customFont = tkFont.Font(family='Achafexp', size=12)
framecoltrol= tk.Frame(windows)
framecoltrol.grid(row=0,column=0)

labLivel = tk.Label(framecoltrol,text=f"Livello {livel}", font=customFont, fg="blue")
labLivel.grid(row=0, column=1)    
style = ttk.Style()
style.configure('my.TCombobox', font=customFont, foreground="green")

comboModelgen= ttk.Combobox(framecoltrol,values=['bondage','diffuserXL','diffuser1.5','realistic vision v6','nsfw'], style='my.TCombobox',font=customFont)
comboModelgen.grid(row=1,column=1)
comboModelgen.set('diffuser1.5')



combonfsw= ttk.Combobox(framecoltrol,value= ['attiva NSFW','disattiva NSFW'],font=customFont)
combonfsw.grid(row=2,column=1)
combonfsw.set('disattiva NSFW')
styleOR = ttk.Style(framecoltrol)
styleOR.configure("Orange.TLabel", foreground="orange")
labper = ttk.Label(framecoltrol, text="Seleziona Personaggio", font=customFont, style="Orange.TLabel")
labper.grid(row=3, column=1)
selez_stregha= ttk.Combobox(framecoltrol,values=['Phoebe','Piper','Prue','Paige','Billie','+ Melody','Personalizzato'], font=customFont)
selez_stregha.grid(row=3,column=1)
selez_stregha.set('Paige')



stylebot = ttk.Style()
stylebot.configure('my.TButton', font=('Helvetica', 12), foreground='blue')

frameInpaint= tk.Frame(windows)
frameInpaint.grid(row=0,column=4)

photol=[]
def imageload():
    global Imgload,photol,frame
    print("load image")
    filetypes = [('JPEG Files', '*.jpg'), ('PNG Files', '*.png')]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        frame.delete('all')
        # Assign the file path to Imgload
        Imgload = filepath
        print(f"Image loaded: {Imgload}")
        shutil.copyfile(Imgload, ".\\imghidden.jpg")
        imgl = Image.open(".\\imghidden.jpg")
        imgl.thumbnail((960,720))
        photol.append(ImageTk.PhotoImage(imgl))
        # Get canvas width and height
        canvas_width = frame.winfo_width()
        canvas_height = frame.winfo_height()
        # Calculate center coordinates
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        # Create image at center
        frame.create_image(center_x, center_y, image=photol[-1], anchor='center')
    else:
        print("No image selected")
        # If no image is selected, set Imgload to None
        Imgload = None


bottonimg = ttk.Button(frameInpaint, text="Carica immagine", style='my.TButton', command=imageload)
bottonimg.grid(row=0, column=0, padx=10)

def selectdir():
    global dirload,photol,frame,arrayphotos
    print("dir")
    dirload = filedialog.askdirectory()
    if dirload:  # If a directory was selected
        frame.delete('all')
        print(f"Selected directory: {dirload}")
        # Get a list of all files in the directory
        files = os.listdir(dirload)
        # Filter the list to include only .jpg and .png files
        arrayphotos = [file for file in files if file.endswith(('.jpg', '.png'))]
        if arrayphotos:  # If there are any images
            shutil.copyfile(os.path.join(dirload, arrayphotos[0]), ".\\imghidden.jpg")
            # Open, resize, and display the first image
            img = Image.open(".\\imghidden.jpg")
            img.thumbnail((960,720))
            photol.append(ImageTk.PhotoImage(img))
            # Get canvas width and height
            canvas_width = frame.winfo_width()
            canvas_height = frame.winfo_height()
            # Calculate center coordinates
            center_x = canvas_width // 2
            center_y = canvas_height // 2
            # Create image at center
            frame.create_image(center_x, center_y, image=photol[-1], anchor='center')
        else:
            print("No images found in the selected directory")
    else:  # If no directory was selected
        print("No directory selected")
        
bottondir= ttk.Button(frameInpaint,text="seleziona Cartella",style='my.TButton',command=selectdir)
bottondir.grid(row=0,column=1)

def clear():
    global Imgload,dirload,frame
    print("clear")
    frame.delete('all')
    Imgload= None
    dirload= None
    print(f"Cancell: {Imgload},{dirload}")
    
delselect = tk.Button(frameInpaint, text="clear select",font=customFont,foreground='magenta',command=clear)
delselect.grid(row=0, column=2,padx=10)

labmod= tk.Label(frameInpaint, text="Seleziona modello Inpaint", font=('Achafexp', 12), foreground='dark blue')
labmod.grid(row=1,column=0)



selectModelInp= ttk.Combobox(frameInpaint,values=['Stable Diffuser XL1.0 Inpainting','Stable Diffusion Inpainting','Realistic Vision V6B1 Inpaint','f222 nsfw Inpainting'],font=customFont)
selectModelInp.grid(row=2,column=0)
selectModelInp.set('Stable Diffuser XL1.0 Inpainting')

#Strength  Eta

lastren_eta= tk.Label(frameInpaint, text="Strength", font=('Achafexp', 12), foreground='green')
lastren_eta.grid(row=3,column=0)
lastren_eta2= tk.Label(frameInpaint, text="Eta", font=('Achafexp', 12), foreground='green')
lastren_eta2.grid(row=3,column=1)

# Crea le variabili di controllo
stren_val = tk.StringVar(value='0.95')  # Imposta il valore iniziale a '0.95'
eta_val = tk.StringVar(value='1.0')  # Imposta il valore iniziale a '1.0'

# Crea le scale e associa le variabili di controllo
stren = ttk.Scale(frameInpaint, from_=0.0, to=1.0, value=0.99, command=lambda s: stren_val.set('%0.2f' % float(s)))
stren.grid(row=4, column=0)

eta = ttk.Scale(frameInpaint, from_=0.0, to=1.0, value=0.99, command=lambda e: eta_val.set('%0.2f' % float(e)))
eta.grid(row=4, column=1)

# Crea le etichette che mostrano i valori delle variabili di controllo
stren_label = tk.Label(frameInpaint, textvariable=stren_val)
stren_label.grid(row=5, column=0)

eta_label = tk.Label(frameInpaint, textvariable=eta_val)
eta_label.grid(row=5, column=1)

# Riduci il padding intorno al canvas
frame = Canvas(windows, width=960, height=720, bg="pink")
frame.grid(row=0, column=2, columnspan=2, padx=100)

labtesto = tk.Label(windows, text="Prompt positivo", font=customFont)
labtesto.grid(row=1, column=2, padx=10)

testo = tk.Text(windows, width=60, height=5, font=customFont)
testo.grid(row=2, column=2, padx=10)

cfg = Scale(windows, from_=1.0, to=100.0, orient="horizontal", resolution=0.1, label="cfg", font=customFont)
cfg.grid(row=3, column=2, padx=10)
cfg.set(float(12.6))

labtesto2 = tk.Label(windows, text="Prompt negativo", font=customFont)
labtesto2.grid(row=1, column=3)

testonegative = tk.Text(windows, width=60, height=5, font=customFont)
testonegative.grid(row=2, column=3)
testonegative.insert("1.0",negative)

steps = Scale(windows, from_=1, to=150, orient="horizontal", label="steps", font=customFont)
steps.grid(row=3, column=3)
steps.set(int(51))

buttongenera= tk.Button(windows,text="Genera Image",font=customFont,command=visualizzaimaginegenerata)
buttongenera.grid(row=4, column=2)

buttonGioca= tk.Button(windows,text="Gioca", font=customFont,command= inizializzagioco)
buttonGioca.grid(row=4, column=3)

style = ttk.Style()
style.configure("red.Horizontal.TProgressbar", troughcolor='red')  # Cambia 'background' in 'troughcolor'

labvita = ttk.Label(windows,text="Vita: 100", foreground= "red", font=customFont)
labvita.grid(row=6, column=2,padx=5)
VitaBar = ttk.Progressbar(windows,maximum=100, value=100, style="red.Horizontal.TProgressbar", length=500)
VitaBar.grid(row=7, column=2)




def exit():
    windows.destroy()
buttonesc= tk.Button(windows,text= "Esci Dal Gioco",  fg= "#8B0000", font=customFont,command=exit)
buttonesc.grid(row=8,column=4,padx=5)

framecoints= tk.Frame(windows)
framecoints.grid(row=9,column=2)

# Creazione dello stile per l'etichetta
stylegold = ttk.Style()
stylegold.configure("Gold.TLabel", foreground="gold", font=("Helvetica", 12))

# Creazione dell'etichetta
labconits = ttk.Label(framecoints, text=f"Total coins: {Totalconits} Coins Level: {CointsLivel}", style="Gold.TLabel")
labconits.grid(row=0,column=0,padx=5)

# Creazione dello stile per la barra di avanzamento
stylegold.configure("red.Horizontal.TProgressbar", foreground="gold", background="yellow")

# Creazione della barra di avanzamento per i total coins
totprogrconits = ttk.Progressbar(framecoints, maximum=1000000, value=0, style="gold.Horizontal.TProgressbar", length=300)
totprogrconits.grid(row=1, column=0,padx=5)

# Creazione della barra di avanzamento per il coins level
totprogrconits_level = ttk.Progressbar(framecoints, maximum=10000, value=0, style="gold.Horizontal.TProgressbar", length=200)
totprogrconits_level.grid(row=1, column=1)


windows.mainloop()



     