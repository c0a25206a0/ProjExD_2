import os
import sys
import random
import time
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

    def check_bound(rct: pg.Rect) -> tuple[bool, bool]:

        """
        
        引数で与えられたRectが画面内外であるかを判定する関数
        引数：こうかとんRectか爆弾Rect
        戻り値：横方向、縦方向
        画面内ならTrue、画面外ならFalse

        """

        width, height = True, True

        if rct.left < 0 or WIDTH < rct.right:
            width = False
        if rct.top < 0 or HEIGHT < rct.bottom:
            height = False
        
        return width, height
    
    #ゲームオーバー画面の処理

    def gameover(screen: pg.Surface) -> None:
        # 1. 黒い矩形を描画するための空のSurfaceを作り，黒い矩形を描画する
        bb_gmov = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(bb_gmov, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

        # 2. 1のSurfaceの透明度を設定する
        bb_gmov.set_alpha(200) 

        # 3. 白文字でGame Overと書かれたフォントSurfaceを作り，1のSurfaceにblitする
        fonto = pg.font.Font(None, 80)
        txt = fonto.render("GAME OVER", True, (255, 255, 255))
        txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        bb_gmov.blit(txt, txt_rect) # txtをblitし忘れていたのを修正

        # 4. こうかとん画像をロードし，こうかとんSurfaceを作り，1のSurfaceにblitする
        kk_gameover_img = pg.image.load("fig/8.png") 
        kk_gameover_rct1 = kk_gameover_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
        kk_gameover_rct2 = kk_gameover_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))

        bb_gmov.blit(kk_gameover_img, kk_gameover_rct1)
        bb_gmov.blit(kk_gameover_img, kk_gameover_rct2) 

        # 5. 1のSurfaceをscreen Surfaceにblitする
        screen.blit(bb_gmov, [0, 0])

        # 6. pg.display.update()したら，time.sleep(5)する
        pg.display.update()
        time.sleep(5)

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            

        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突
            gameover(screen)
            return #当たった時のゲームを終わらせる処理
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()

        idou = [0, 0]

        for key, move in DELTA.items():
            if key_lst[key]:
                idou[0] += move[0]
                idou[1] += move[1]

        kk_rct.move_ip(idou[0], idou[1])

        if check_bound(kk_rct) != (True, True): #画面外なら
            kk_rct.move_ip(-idou[0], -idou[1])
        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)

        width, height = check_bound(bb_rct)
        if not width:
            vx *= -1
        if not height:
            vy *= -1

        screen.blit(bb_img, bb_rct) #爆弾を表示

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
