import os
import random 
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0), 
    }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def game_over(screen, fonto, txt, go_kk_rct, go_kk): 
    """
    Game Overの画面を表示する関数
    引数:
    screen: ゲーム画面
    fonto: フォントオブジェクト
    txt: "Game Over"の文字画像
    go_kk_rct: こうかとんのRectオブジェクト
    go_kk: 泣いているこうかとんの画像
    """
    black_out = pg.Surface(screen.get_size())
    black_out.fill((0, 0, 0))
    black_out.set_alpha(200)

    screen.blit(black_out, (0, 0))
    screen.blit(txt, [WIDTH/2 - txt.get_width()/2,HEIGHT/2])

    go_kk_rct.center = WIDTH/2 - 200, HEIGHT/2 + 25
    screen.blit(go_kk, go_kk_rct)
    go_kk_rct.center = WIDTH/2 + 200, HEIGHT/2 + 25
    screen.blit(go_kk, go_kk_rct)

    pg.display.update()
    time.sleep(5) #5
    return
    


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん　または　獏ファンのRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue　画面外たらFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #爆弾
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5 #爆弾の速度

    clock = pg.time.Clock()
    tmr = 0

    fonto = pg.font.Font(None, 80)  # フォントオブジェクト
    txt = fonto.render("Game Over", True, (255, 255, 255))  # "Game Over"の文字画像
    go_kk = pg.image.load("fig/8.png")  # 泣いているこうかとんの画像
    go_kk_rct = go_kk.get_rect()  # こうかとんのRectオブジェクト
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):#こうかとんと爆弾が重なった時
            game_over(screen, fonto, txt, go_kk_rct, go_kk)
            return
            #return #ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] #横、縦
        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] #横
                sum_mv[1] += tpl[1] #縦
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#画面外に出ない
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)

        yoko, tate = check_bound(bb_rct) #爆弾が反射
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

