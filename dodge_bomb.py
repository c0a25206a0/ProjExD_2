import os
import sys
import random
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0)}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内外であるかを判定する関数
    戻り値：横方向、縦方向（画面内ならTrue、画面外ならFalse）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    """
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

def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    org(爆弾)からdst(こうかとん)へ向かう速度ベクトルを計算する関数
    引数 current_xy: 現在の速度(vx, vy)
    """
    diff_x = dst.centerx - org.centerx
    diff_y = dst.centery - org.centery
    
    # 距離を計算（三平方の定理）
    norm = (diff_x**2 + diff_y**2) ** 0.5
    
    if norm != 0:
        # 現在の「速さ（ベクトルの長さ）」を計算
        speed = (current_xy[0]**2 + current_xy[1]**2) ** 0.5
        # 単位ベクトル（長さ1）に速さを掛けて、新しい(vx, vy)を作る
        new_vx = (diff_x / norm) * speed
        new_vy = (diff_y / norm) * speed
        return new_vx, new_vy
    
    return current_xy

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # --- こうかとん画像の準備 ---
    kk_img = pg.image.load("fig/3.png")
    # 左右反転させて「右向き」を基準にする
    kk_img_0 = pg.transform.flip(kk_img, True, False)
    
    # 8方向の画像を辞書で定義する
    kk_imgs = {
        (0, 0):   pg.transform.rotozoom(kk_img_0, 0, 0.9),    # 静止
        (+5, 0):  pg.transform.rotozoom(kk_img_0, 0, 0.9),    # 右
        (+5, -5): pg.transform.rotozoom(kk_img_0, 45, 0.9),   # 右上
        (0, -5):  pg.transform.rotozoom(kk_img_0, 90, 0.9),   # 上
        (+5, +5): pg.transform.rotozoom(kk_img_0, -45, 0.9),  # 右下
        (0, +5):  pg.transform.rotozoom(kk_img_0, -90, 0.9),  # 下
        (-5, 0):  pg.transform.flip(pg.transform.rotozoom(kk_img_0, 0, 0.9), True, False),   # 左
        (-5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img_0, 45, 0.9), True, False),  # 左上
        (-5, +5): pg.transform.flip(pg.transform.rotozoom(kk_img_0, -45, 0.9), True, False), # 左下
    }

    kk_img = kk_imgs[(0, 0)] 
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # --- 爆弾の拡大・加速用のリスト作成 ---
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    
    # 爆弾の初期速度
    vx, vy = 5.0, 5.0
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        # --- 当たり判定 ---
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # 1. 背景の描画
        screen.blit(bg_img, [0, 0]) 

        # 2. こうかとんの移動と画像切り替え
        key_lst = pg.key.get_pressed()
        idou = [0, 0]
        for key, move in DELTA.items():
            if key_lst[key]:
                idou[0] += move[0]
                idou[1] += move[1]
        
        kk_img = kk_imgs[tuple(idou)]
        kk_rct.move_ip(idou[0], idou[1])
        
        # こうかとんが画面外に出ないようにする
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-idou[0], -idou[1])
            
        screen.blit(kk_img, kk_rct)

        # 3. 爆弾の拡大・加速と周期的な追従
        idx = min(tmr // 500, 9) # 10秒(500フレーム)ごとに段階アップ
        curr_bb_img = bb_imgs[idx]
        
        # 100フレーム（約2秒）に1回だけ方向を再計算する
        if tmr % 100 == 0:
            vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        
        # 計算した(vx, vy)に、時間の経過による加速倍率をかける
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        
        # サイズが変わるのでRectを更新（中心を維持）
        old_center = bb_rct.center
        bb_rct = curr_bb_img.get_rect()
        bb_rct.center = old_center
        
        # 移動実行
        bb_rct.move_ip(avx, avy)

        # 追従しない間は壁にぶつかるので、跳ね返り処理を行う
        yoko, tate = check_bound(bb_rct)
        if not yoko: 
            vx *= -1
        if not tate: 
            vy *= -1

        screen.blit(curr_bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()