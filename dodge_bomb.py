import os
import sys
import random
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:

    bb_gmov = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bb_gmov, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bb_gmov.set_alpha(200) 
    
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GAME OVER", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    bb_gmov.blit(txt, txt_rect)
    kk_gameover_img = pg.image.load("fig/8.png") 
    kk_gameover_rct1 = kk_gameover_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    kk_gameover_rct2 = kk_gameover_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    
    bb_gmov.blit(kk_gameover_img, kk_gameover_rct1)
    bb_gmov.blit(kk_gameover_img, kk_gameover_rct2) 
    
    screen.blit(bb_gmov, [0, 0])
    pg.display.update()
    time.sleep(5)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとん画像の準備
    # 基本の画像（右向き）をロード
    kk_img = pg.image.load("fig/3.png")
    #左右反転させて「右向き」を基準にする
    kk_img_0 = pg.transform.flip(kk_img, True, False)
    
    # 8方向の画像を辞書で定義する
    # キーは横移動量, 縦移動量、値はrotozoomしたSurface
    kk_imgs = {
        (0, 0):   pg.transform.rotozoom(kk_img_0, 0, 0.9),    # 静止
        (+5, 0):  pg.transform.rotozoom(kk_img_0, 0, 0.9),    # 右
        (+5, -5): pg.transform.rotozoom(kk_img_0, 45, 0.9),   # 右上
        (0, -5):  pg.transform.rotozoom(kk_img_0, 90, 0.9),   # 上
        (+5, +5): pg.transform.rotozoom(kk_img_0, -45, 0.9),  # 右下
        (0, +5):  pg.transform.rotozoom(kk_img_0, -90, 0.9),  # 下
        # --- 左側シリーズ（右用を回転させてから反転させる） ---
        (-5, 0):  pg.transform.flip(pg.transform.rotozoom(kk_img_0, 0, 0.9), True, False),   # 左
        (-5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img_0, 45, 0.9), True, False),  # 左上
        (-5, +5): pg.transform.flip(pg.transform.rotozoom(kk_img_0, -45, 0.9), True, False), # 左下
    }


    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)

    kk_img = kk_imgs[(0, 0)] 
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の拡大・加速用のリスト作成
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    

    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        # 当たり判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # 1. 背景の描画（一番最初）
        screen.blit(bg_img, [0, 0]) 

        # 2. こうかとんの移動
        key_lst = pg.key.get_pressed()
        idou = [0, 0]
        for key, move in DELTA.items():
            if key_lst[key]:
                idou[0] += move[0]
                idou[1] += move[1]
        
        kk_img = kk_imgs[tuple(idou)]

        kk_rct.move_ip(idou[0], idou[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-idou[0], -idou[1])
        screen.blit(kk_img, kk_rct)

        # 3. 爆弾の拡大・加速
        idx = min(tmr // 500, 9) # 10秒(500フレーム)ごとに段階アップ
        curr_bb_img = bb_imgs[idx]
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        
        # サイズが変わるのでRectを更新（中心を維持）
        old_center = bb_rct.center
        bb_rct = curr_bb_img.get_rect()
        bb_rct.center = old_center
        
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: vx *= -1
        if not tate: vy *= -1

        screen.blit(curr_bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()