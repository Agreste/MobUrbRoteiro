import string

from flask import *
import pandas as pd
import numpy as np
from sqlalchemy import and_

from . import *
from .default_settings import _basedir

all_videos = db.session.query(models.Video).all()
videos = {v.name: v for v in all_videos if not 'BORBA' in v.name and v.name not in ['ABERTURA', 'FECHAMENTO'] and v.position != 'f'}
borbas = {b.name: b for b in all_videos if 'BORBA' in b.name}
aberturas = {a.name: a for a in db.session.query(models.Video).filter(models.Video.position == 'a').all()}
fechamentos = {f.name: f for f in [db.session.query(models.Video).\
                   filter(and_(models.Video.name.contains(a.name.split(' ')[0]), models.Video.position == 'f')).\
                   one() for a in aberturas.values()]}

videos_weights = {}
for video_name_A, video_tags_A in videos.items():
    videos_weights[video_name_A] = {}
    for video_name_B, video_tags_B in videos.items():
        if video_name_B != video_name_A:
            common_tags_num = len(set([t.id for t in videos[video_name_A].tags]).\
                                intersection(set([t.id for t in videos[video_name_B].tags])))
            if common_tags_num > 0:
                videos_weights[video_name_A][video_name_B] = common_tags_num

def random_abertura_fechamento():
    a = np.random.choice(aberturas.values())
    f = [f for f in fechamentos.values() if a.name.split(' ')[0] in f.name][0]
    return (a,f)

def seleciona_proximo(video_atual, already_played):
    normalizador = sum(videos_weights[video_atual.name].values())
    prob = [float(video)/normalizador for video in videos_weights[video_atual.name].values()]
    while True:
        proximo_video = np.random.choice(videos_weights[video_atual.name].keys(), p=prob)
        if proximo_video not in already_played:
            break
    return videos[proximo_video]

# Symbols used for URL slug reation
sym = string.ascii_letters + string.digits[1:]

inicio = {"1280x720": "https://player.vimeo.com/external/159699169.hd.mp4?s=ae62327392ef36f532a69ace0304646099802272&profile_id=113",
          "960x540": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=165",
          "640x360": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=164"}

finalizacao = {"1280x720": "https://player.vimeo.com/external/159699558.hd.mp4?s=81a7e93edc5a587c29cefe0bce7d7ccb5c2ae4c4&profile_id=113",
               "960x540": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=165",
               "640x360": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=164"}

def create_slug(lista):
    slug = ''
    for video in  lista:
        if video['id'] > 0:
            if video['id'] < 61:
                slug += sym[video['id']]
            else:
                slug += '0' + sym[video['id'] - 61]
    return slug

def decode_slug(slug, resolution="1280x720"):
    lista = []
    a = 0

    roteiro = {}
    roteiro['duration'] = 0
    roteiro['slug'] = slug
    roteiro['sequence'] = [{'url': inicio[resolution], 'sub': 'NOSUB', 'id': -1}]

    for c in slug:
        if c == '0':
           a = 61
           continue
        else:
           lista += [a + sym.index(c)]
           a = 0

    for id in lista:
        video = db.session.query(models.Video).get(id)
        roteiro['duration'] += video.duration
        roteiro['sequence'].append(video.json(resolution))

    roteiro['sequence'].append({'url': finalizacao[resolution], 'sub': 'NOSUB', 'id': -1})

    return roteiro

def cria_roteiro(numero_maximo = 7, resolution="1280x720"):
    roteiro = {'duration': 0, 'sequence': []}
    duracao_total = 0

    roteiro['sequence'] = [{'url': inicio[resolution], 'sub': 'NOSUB', 'id': -1}]
    abertura, fechamento = random_abertura_fechamento()

    already_played = [abertura.name, fechamento.name]
    duracao_total += abertura.duration

    roteiro['sequence'].append(abertura.json(resolution))

    atual = abertura
    for i in range(numero_maximo):
        proximo = seleciona_proximo(atual, already_played)
        already_played += [proximo.name]

        duracao_total += proximo.duration

        roteiro['sequence'].append(proximo.json(resolution))
        atual = proximo

    duracao_total += fechamento.duration

    roteiro['sequence'].append(fechamento.json(resolution))
    roteiro['sequence'].append({'url': finalizacao[resolution], 'sub': 'NOSUB', 'id': -1})

    # Adiciona cortes do Borbagato

    numero_borbas = 3 + (numero_maximo - 7) / 2
    indices = range(2, numero_maximo)
    des_indices_borba = np.random.choice(indices, replace=False, size=numero_borbas)
    indices_borba = sorted(des_indices_borba)
    trechos_borba = np.random.choice(borbas.keys(), replace=False, size=numero_borbas)

    for i, indice in enumerate(indices_borba):
        roteiro['sequence'].insert(indice + i, borbas[trechos_borba[i]].json(resolution))

        duracao_total += float(borbas[trechos_borba[i]].duration)

    roteiro['duration'] = duracao_total
    minutos = int(duracao_total)/60
    segundos = int(duracao_total)%60
    if segundos != 0:
        print '{}m{}s'.format(minutos, segundos)
    else:
        print '{}m'.format(minutos)

    roteiro['slug'] = create_slug(roteiro['sequence'])

    return roteiro

