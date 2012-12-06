import Image

def make_box(element):
    x = element.location['x']
    y = element.location['y']
    height = element.size['height']
    width = element.size['width']
    box = (x,y, x+width, y+height)
    return box

def encode_html(fname):
    data_uri = open(fname, 'rb').read().encode('base64').replace('\n','')
    img_tag = '<img src="data:image/png;base64,%s">' % data_uri
    return img_tag


def make_html_img(element, wb):
    box = make_box(element)
    fname = "ss.png"
    wb.save_screenshot(fname)
    im = Image.open(fname)
    im = im.crop(box)
    im.save(fname)
    return encode_html(fname)



