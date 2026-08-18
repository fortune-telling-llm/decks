from stellar_base import *
from stellar_minor import MINOR
from stellar_major import MAJORS
from stellar_render import slug, render

def cards():
    idx=1
    for suit in ('Wands','Cups','Swords','Pentacles'):
        for rank,core,scene in MINOR[suit]:
            idx += 1 if not (suit=='Wands' and rank=='Ace') else 0
            if suit=='Wands' and rank=='Ace':
                continue
            title=f'{rank} of {suit}'
            yield idx,title,'Minor Arcana',suit,RANK_NUMBER[rank],core,scene
        if suit!='Wands':
            pass
    for i,title,core,scene in MAJORS:
        yield i,title,'Major Arcana',None,str(i-57) if i>57 else '0',core,scene

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for index,title,arcana,suit,formal,core,scene in cards():
        path=OUT/f'{index}-{slug(title)}.md'
        path.write_text(render(index,title,arcana,suit,formal,core,scene),encoding='utf-8')
    files=sorted(OUT.glob('[0-9]*.md'),key=lambda p:int(p.name.split('-',1)[0]))
    assert len(files)==78, len(files)
    assert [int(p.name.split('-',1)[0]) for p in files]==list(range(1,79))
    required=['## Card metadata','## Literal visual description','## Core meaning','### Upright keywords','### Reversed / shadow keywords','## Symbol-by-symbol interpretation','## Divinatory interpretation by question type','## Intentions','## Feelings','## Actions / likely next move','## Advice','## Outcome','## Yes / no','## Timing','## Health / wellbeing readings','## Spread interactions','## Image-led reading examples','## Fortune-teller cautions','## One-sentence essence']
    titles=[]
    for p in files:
        text=p.read_text(encoding='utf-8')
        titles.append(text.splitlines()[0])
        for heading in required:
            assert heading in text,(p,heading)
        assert len(text)>9000,(p,len(text))
        assert not re.search(r'placeholder|lorem ipsum|(^|[^A-Z])TBD([^A-Z]|$)|(^|[^A-Z])TODO([^A-Z]|$)',text,re.I),p
    assert len(set(titles))==78
    assert (OUT/'1-ace-of-wands.md').is_file()
    assert (OUT/'78-the-world.md').is_file()
    assert (OUT/'DECK-INFO.md').is_file()
    print('Validated 78 continuous Stellar Mosaic Tarot descriptions.')

if __name__=='__main__':
    main()
