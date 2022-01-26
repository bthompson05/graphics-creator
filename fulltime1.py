from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from cropimagesquare import CropSquareImages

class FullTimeOption1:

    def __init__(self, image, logo_l, logo_r, score, half, base, compliment):
        self.image = image
        self.logo_l = logo_l
        self.logo_r = logo_r
        self.home_score = 0
        self.away_score = 0
        self.score = score
        self.half = half
        self.canvas = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
        self.base = base
        self.compliment = compliment


    def set_scores(self):
        try:
            list_form = self.score.split("-")
            self.home_score = list_form[0]
            self.away_score = list_form[1]
        except:
            print("An error has occurred.")

    def add_background_image(self):
        im = CropSquareImages(self.image).main_func()
        im = im.resize((1080, 1080))
        self.canvas.paste(im)

    def add_overlay(self):
        # change colours for main color (bottom)

        # open the image into memory
        main = Image.open("assets/baseplate.png")
        # loop through each item in the image array
        for w in range(main.width):
            for h in range(main.height):
                # gets RGBA values of the pixel selected
                tup = main.getpixel((w, h))
                # sets to requested color if pixel is not transparent
                if tup[3] > 50:
                    main.putpixel((w, h), self.base)
                # passes the pixel if it is not transparent
                else:
                    pass

        # opens the accent image into memory
        accent = Image.open("assets/accent.png")
        # loops through each item in the image array
        for w in range(main.width):
            for h in range(main.height):
                tup = accent.getpixel((w, h))
                # misses out the pixel if it is transparent
                if tup[3] < 200:
                    pass
                # sets the color of visible pixels to the requested one
                else:
                    accent.putpixel((w, h), self.compliment)
        # combines the accent image with the bas image
        main.paste(accent, (0, 1), accent)
        # opens the text overlay into memory
        overlay = Image.open("assets/overlay.png")
        # applies the overlay to the base image
        combination = Image.alpha_composite(main, overlay)

        mask = Image.open("assets/masklogos.png")
        for w in range(mask.width):
            for h in range(mask.height):
                tup = mask.getpixel((w, h))
                if tup == (255, 255, 255, 255):
                    combination.putpixel((w, h), (255, 255, 255, 0))

        shadows = Image.open("assets/logo_shadows.png")
        combination = Image.alpha_composite(combination, shadows)
        self.canvas.paste(combination, (0,0), combination)

    def add_logos(self):

        l = Image.open(self.logo_l)
        l = l.resize((339, 339))
        r = Image.open(self.logo_r)
        r = r.resize((339, 339))

        # creating logos
        base = Image.new(mode="RGBA", size=(1080, 1080), color=(255, 255, 255, 255))
        base.paste(l, (205, 735), l)
        base.paste(r, (534, 735), r)
        # creating mask
        mask = Image.open('./assets/masklogos.png').convert('L')

        # applying the mask to the images
        self.canvas = Image.composite(base, self.canvas, mask)

    def add_scores(self):

        scores_boxes = Image.open("./assets/scoreboxes.png")
        for w in range(scores_boxes.width):
            for h in range(scores_boxes.height):
                tup = scores_boxes.getpixel((w, h))
                if tup[3] > 200:
                    scores_boxes.putpixel((w, h), self.base)
                else:
                    pass
        enhancer = ImageEnhance.Brightness(scores_boxes)
        scores_boxes = enhancer.enhance(0.65)
        self.canvas.paste(scores_boxes, (0, 0), scores_boxes)

        font = ImageFont.truetype("./assets/bebas.ttf", 115)

        # establishing draw object
        img_draw = ImageDraw.Draw(self.canvas)
        img_draw.text((350, 715), str(self.home_score), fill='white', font=font)
        img_draw.text((682, 715), str(self.away_score), fill='white', font=font)

    def add_timings(self):
        if self.half == "ht":
            over = Image.open("./assets/half_time_overlay.png")
            self.canvas.paste(over, (0, 0), over)
        else:
            over = Image.open("./assets/full_time_overlay.png")
            self.canvas.paste(over, (0, 0), over)

    def create_graphic(self):
        self.set_scores()
        self.add_background_image()
        self.add_overlay()
        self.add_logos()
        self.add_scores()
        self.add_timings()
        self.canvas.show()



a = FullTimeOption1("./assets/bg.jfif", "./assets/WBA.png", "./assets/Millwall.png", "1-2", "ft", (0, 0, 70, 255), (255, 255, 255, 255))
a.create_graphic()

# create web scraping module


