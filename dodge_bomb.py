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


def houkou():
    """
    各移動方向に応じたこうかとんの画像を辞書で返す関数
    戻り値：
    kk_img:方向と対応するこうかとんの画像を辞書として返す
    """
    kk_img = pg.image.load("fig/3.png")
    kk_imgs = {
        (5, 0): pg.transform.rotozoom(kk_img, 180, 1.0),   # 右
        (5, -5): pg.transform.rotozoom(kk_img, 0, 1.0),  # 右上
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0), # 左
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0), # 左上
        (0, 5): pg.transform.rotozoom(kk_img, 90, 1.0),  # 下
        (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0),  # 上
        (5, 5): pg.transform.rotozoom(kk_img, 0, 1.0),  # 右下
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0), # 左下
    }
    return kk_imgs



def bomb():
    """
    爆弾の拡大画像リストと加速度リストを作成する関数
    戻り値：
    bb_img : サイズに応じた爆弾Surface
    bb_accs : 加速度のリスト
    """
    bb_imgs = []  # 爆弾画像のリスト
    bb_accs = [a for a in range(1, 11)]  # 加速度のリスト

    for r in range(1, 11):  # 爆弾のサイズを1段階ごとに大きくする
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # サイズに応じた爆弾Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 赤い爆弾を描く
        bb_imgs.append(bb_img)  # リストに追加

    return bb_imgs, bb_accs






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

    # 各方向に応じたこうかとんの画像を取得
    kk_imgs = houkou()
    kk_img = kk_imgs[(5, 0)]  # 最初の向きは右
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = bomb()  # bomb関数から爆弾画像と加速度を取得
    bb_rct = bb_imgs[0].get_rect()  # 最初の爆弾サイズのRectを設定
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 初期の爆弾速度

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

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なった時
            game_over(screen, fonto, txt, go_kk_rct, go_kk)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横、縦移動量
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横
                sum_mv[1] += tpl[1]  # 縦

        # 移動量がある場合、対応する方向のこうかとん画像に変更
        if sum_mv != [0, 0]:
            movement = (sum_mv[0], sum_mv[1])
            kk_img = kk_imgs.get(movement, kk_img)  # 辞書から画像を取得（デフォルトは現在の画像）

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外に出ない
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # tmrに基づいて適切な爆弾画像と加速度を選択
        idx = min(tmr // 500, 9)  # インデックスの上限は9（10段階）
        bb_img = bb_imgs[idx]  # 爆弾の拡大版を取得
        bb_rct = bb_img.get_rect(center=bb_rct.center)  # 拡大後のRectを取得

        avx = vx * bb_accs[idx]  # 加速値に基づいて速度を調整
        avy = vy * bb_accs[idx]

        bb_rct.move_ip(avx, avy)  # 爆弾の移動

        yoko, tate = check_bound(bb_rct)  # 爆弾が画面端にぶつかったら反射
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)  # 爆弾を描画
        screen.blit(kk_img, kk_rct)  # こうかとんを描画
        pg.display.update()
        tmr += 1  # タイマーの更新
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

