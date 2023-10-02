import random
def random_memes():
    Photo = ["0.png", "1.png"] #сюда закинем картинки,вообще если знаешь способ лучше то его сделаем, я просто не особо с этим морочился
    memes = random.choice(Photo)
    f = open("memes/" + memes, 'rb')
    return "memes/" + memes