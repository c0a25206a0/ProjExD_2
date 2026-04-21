import os
import sys
import random
import pygame as pg



WIDTH, HEIGHT = 1100, 650

#辞書deltaの定義

DELTA = {
    pg.K_UP: (0, -5),  
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20)) #爆弾用の空のSurfaceを作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0,)) #円の周りの黒い領域を透明化

    bb_rct = bb_img.get_rect() #爆弾rectを作る
    bb_rct.centerx = random.randint(0,WIDTH) #爆弾の初期横座標を設定
    bb_rct.centery = random.randint(0, HEIGHT)#爆弾の初期縦座標を設定 

    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()

        idou = [0, 0]

        for key, move in DELTA.items():
            if key_lst[key]:
                idou[0] += move[0]
                idou[1] += move[1]

        kk_rct.move_ip(idou[0], idou[1])
        
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)

        screen.blit(bb_img, bb_rct) #爆弾を表示

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
