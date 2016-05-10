from flask import *
import pandas as pd

from application import *
from application.default_settings import _basedir

roteiro = pd.read_excel('Roteiro_Mob_Urb_16_05_04.xlsx')
roteiro = roteiro.fillna('')
videos_info = pd.read_csv('../video_all_info.csv', quotechar='"')
videos_info = videos_info.fillna('')

db.create_all()
db.session.commit()

for vi, v in videos_info.iterrows():
    # Insere video
    new_video = models.Video()
    new_video.name = v['name'].decode('utf8')
    new_video.duration = v['duration']
    new_video.vimeo_id = v['id']
    new_video.high_def = v['highres']
    new_video.standard_def_small = v['sd_small']
    new_video.standard_def_big = v['sd_big']
    new_video.position = v['borda']

    db.session.add(new_video)
    db.session.commit()
    
    # Insere legenda
    new_sub = models.Subtitle()
    new_sub.language = "pt"
    new_sub.filename = v['sub']
    new_sub.video_id = new_video.id
    
    db.session.add(new_sub)
    db.session.commit()

    roteiro_video = roteiro[roteiro['name'] == new_video.name]
    if not roteiro_video.empty:
        tags = [s for s in roteiro_video.iloc[0,8:].values if s]
        for tag in tags:
            search_tag = db.session.query(models.Tag).filter(models.Tag.value == tag).all()
            if not search_tag:
                new_tag = models.Tag()
                new_tag.value = tag
                db.session.add(new_tag)
                db.session.commit()
                t = new_tag
            else:
                t = search_tag[0]
            new_video.tags.append(t)
            db.session.add(new_video)
            db.session.commit()

