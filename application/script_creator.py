import numpy as np
import pickle

videos_file = open('application/videos.dict')
videos = pickle.load(videos_file)

tags_file = open('application/tags.dict')
tags = pickle.load(tags_file)

videos_urls_file = open('application/video_urls.dict')
videos_urls = pickle.load(videos_urls_file)

videos_weights_file = open('application/videos_weights.dict')
videos_weights = pickle.load(videos_weights_file)

videos_subs_file = open('application/videos_subs.dict')
videos_subs = pickle.load(videos_subs_file)

def seleciona_fechamento(abertura):
    abertura_nome = abertura.split(' ')[0]
    return [ab for ab in tags['Fechamento'] if ab.startswith(abertura_nome)]

def seleciona_proximo(video_atual):
    normalizador = sum(videos_weights[video_atual].values())
    prob = [float(video)/normalizador for video in videos_weights[video_atual].values()]
    proximo_video = np.random.choice(videos_weights[video_atual].keys(), p=prob)
    return proximo_video

def cria_roteiro(numero_maximo = 7, resolution="1280x720"):
    inicio = {"1280x720": "https://player.vimeo.com/external/159699169.hd.mp4?s=ae62327392ef36f532a69ace0304646099802272&profile_id=113",
               "960x540": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=165",
               "640x360": "https://player.vimeo.com/external/159699169.sd.mp4?s=002561d1556097cc3c385431c8697d3d82f8b044&profile_id=164"}

    finalizacao = {"1280x720": "https://player.vimeo.com/external/159699558.hd.mp4?s=81a7e93edc5a587c29cefe0bce7d7ccb5c2ae4c4&profile_id=113",
                    "960x540": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=165",
                    "640x360": "https://player.vimeo.com/external/159699558.sd.mp4?s=b56ebe0e08ed2832000e1493293fcddd6f994982&profile_id=164"}

    roteiro = [(inicio[resolution], 'NOSUB')]
    abertura = np.random.choice(tags['Abertura'])
    roteiro.append((videos_urls[resolution][abertura], videos_subs.get(abertura, 'NOSUB')))

    atual = abertura
    for i in range(numero_maximo):
        proximo = seleciona_proximo(atual)
        roteiro.append((videos_urls[resolution][proximo], videos_subs.get(proximo, 'NOSUB')))
        atual = proximo

    fechamento = np.random.choice(seleciona_fechamento(abertura))
    roteiro.append((videos_urls[resolution][fechamento], videos_subs.get(fechamento, 'NOSUB')))
    roteiro.append((finalizacao[resolution], 'NOSUB'))
    return roteiro
