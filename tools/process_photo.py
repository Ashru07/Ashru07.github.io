from pathlib import Path
from rembg import remove
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
in_path = ROOT / 'assets' / 'photo.jpg'
out_png = ROOT / 'assets' / 'photo_processed.png'
out_jpg = ROOT / 'assets' / 'photo_rounded.jpg'

def process():
    if not in_path.exists():
        print('INPUT PHOTO NOT FOUND:', in_path)
        return

    with in_path.open('rb') as i:
        input_bytes = i.read()

    # remove background
    result = remove(input_bytes)

    # save temp png
    temp = ROOT / 'assets' / 'photo_nobg.png'
    temp.write_bytes(result)

    img = Image.open(temp).convert('RGBA')

    # create circular mask
    size = (520, 520)
    img = ImageOps.fit(img, size, centering=(0.5,0.4))
    mask = Image.new('L', size, 0)
    draw = Image.new('L', size, 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(mask)
    d.ellipse((0,0,size[0],size[1]), fill=255)

    # apply mask to make circle
    circular = Image.new('RGBA', size, (255,255,255,0))
    circular.paste(img, (0,0), mask=mask)

    # create soft background and shadow
    bg = Image.new('RGBA', (size[0]+40, size[1]+40), (15,17,36,255))
    shadow = Image.new('RGBA', bg.size, (0,0,0,0))
    sh = Image.new('RGBA', size, (0,0,0,180))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    shadow.paste(sh, (20,20), sh)
    bg = Image.alpha_composite(bg, shadow)

    # paste circular on bg
    bg.paste(circular, (20,20), circular)

    # save processed PNG (transparent background) and flattened JPG
    out_png.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_png)

    # also save a flattened jpg for browsers that may not render PNG shadow well
    rgb = Image.new('RGB', bg.size, (15,17,36))
    rgb.paste(bg, mask=bg.split()[3])
    rgb.save(out_jpg, quality=90)

    print('WROTE', out_png, out_jpg)

if __name__ == '__main__':
    process()
