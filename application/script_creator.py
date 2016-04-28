import numpy as np
import string
import pickle

videos_file = open('application/videos.dict')
videos = pickle.load(videos_file)

tags_file = open('application/tags.dict')
tags = pickle.load(tags_file)

videos_urls_file = open('application/video_urls.dict')
videos_urls = pickle.load(videos_urls_file)

borba_urls_file = open('application/borba_urls.dict')
borba_urls = pickle.load(borba_urls_file)

borba_durations_file = open('application/borba_durations.dict')
borba_durations = pickle.load(borba_durations_file)

borba_ids_file = open('application/borba_ids.dict')
borba_ids = pickle.load(borba_ids_file)

video_durations_file = open('application/video_durations.dict')
video_durations = pickle.load(video_durations_file)

video_ids_file = open('application/video_ids.dict')
video_ids = pickle.load(video_ids_file)

videos_weights_file = open('application/videos_weights.dict')
videos_weights = pickle.load(videos_weights_file)

videos_subs_file = open('application/videos_subs.dict')
videos_subs = pickle.load(videos_subs_file)

# Symbols used for URL slug reation
sym = string.ascii_letters + string.digits[1:]

def create_slug(lista):
    slug = ''
    for num in  lista:
        if num < 61:
            slug += sym[num]
        else:
            slug += '0' + sym[num - 61]
    return slug

def decode_slug(slug):
    lista = []
    a = 0
    for c in slug:
        if c == '0':
           a = 61
           continue
        else:
           lista += [a + sym.index(c)]
           a = 0
    return lista

def seleciona_fechamento(abertura):
    abertura_nome = abertura.split(' ')[0]
    return [ab for ab in tags['Fechamento'] if ab.startswith(abertura_nome)]

def seleciona_proximo(video_atual):
    normalizador = sum(videos_weights[video_atual].values())
    prob = [float(video)/normalizador for video in videos_weights[video_atual].values()]
    proximo_video = np.random.choice(videos_weights[video_atual].keys(), p=prob)
    return proximo_video

def cria_roteiro(numero_maximo = 7, resolution="1280x720"):
    duracao_total = 0

    inicio = {"1280x720": "https://player.vimeo.com/external/159699169.hd.mp4?s=ae62327392ef36f532a69ace0304646099802272&profile_id=113",
               "960x540": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=165",
               "640x360": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=164"}

    finalizacao = {"1280x720": "https://player.vimeo.com/external/159699558.hd.mp4?s=81a7e93edc5a587c29cefe0bce7d7ccb5c2ae4c4&profile_id=113",
                    "960x540": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=165",
                    "640x360": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=164"}

    roteiro = [(inicio[resolution], 'NOSUB')]
    abertura = np.random.choice(tags['Abertura'])

    duracao_total += float(video_durations[video_ids[abertura]])

    roteiro.append((videos_urls[resolution][abertura], videos_subs.get(abertura, 'NOSUB')))

    atual = abertura
    for i in range(numero_maximo):
        proximo = seleciona_proximo(atual)

        duracao_total += float(video_durations[video_ids[proximo]])

        roteiro.append((videos_urls[resolution][proximo], videos_subs.get(proximo, 'NOSUB')))
        atual = proximo

    fechamento = np.random.choice(seleciona_fechamento(abertura))

    duracao_total += float(video_durations[video_ids[fechamento]])

    roteiro.append((videos_urls[resolution][fechamento], videos_subs.get(fechamento, 'NOSUB')))
    roteiro.append((finalizacao[resolution], 'NOSUB'))

    # Adiciona cortes do Borbagato

    numero_borbas = 3 + (numero_maximo - 7) / 2
    indices = range(2, numero_maximo)
    des_indices_borba = np.random.choice(indices, replace=False, size=numero_borbas)
    indices_borba = sorted(des_indices_borba)
    trechos_borba = np.random.choice(borba_urls[resolution].keys(), replace=False, size=numero_borbas)

    for i, indice in enumerate(indices_borba):
        roteiro.insert(indice + i, (borba_urls[resolution][trechos_borba[i]], 'NOSUB'))

        duracao_total += float(borba_durations[borba_ids[trechos_borba[i]]])

    print duracao_total
    minutos = int(duracao_total)/60
    segundos = int(duracao_total)%60
    if segundos != 0:
        print '{}m{}s'.format(minutos, segundos)
    else:
        print '{}m'.format(minutos)

    return roteiro
