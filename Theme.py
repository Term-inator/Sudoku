class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    white_alpha = (255, 255, 255, 200)
    grey = (128, 128, 128)
    grey_alpha = (128, 128, 128, 200)
    light_grey_alpha = (225, 225, 225, 200)
    reddish_blue_alpha = (65, 105, 225, 100)
    transparent = (0, 0, 0, 0)

    sun_flower = (241, 196, 15)
    sun_flower_alpha = (241, 196, 15, 100)

    black_pearl = (30, 39, 46)
    blue_night_alpha = (53, 59, 72, 200)

    chi_gong = (214, 48, 49)
    chi_gong_alpha = (255, 0, 0, 200)
    alizarin_alpha = (231, 76, 60, 200)

    aurora_green = (120, 224, 143)
    aurora_green_alpha = (120, 224, 143, 200)
    green_sea = (22, 160, 133)
    green_sea_alpha = (22, 160, 133, 200)
    ufo_green = (46, 213, 115)
    ufo_green_alpha = (46, 213, 115, 200)

    green_darner_tail = (72, 219, 251)
    green_darner_tail_alpha = (116, 185, 255, 200)
    merchant_marine_blue = (6, 82, 221)
    merchant_marine_blue_alpha = (6, 82, 221, 200)
    joust_blue_alpha = (84, 160, 255, 200)
    saturated_sky_alpha = (83, 82, 237, 200)

    beekeeper = (246, 229, 141)
    beekeeper_alpha = (246, 229, 141, 200)
    puffins_bill = (238, 90, 36)
    puffins_bill_alpha = (238, 90, 36, 200)
    radiant_yellow_alpha = (247, 159, 31, 200)
    carrot_alpha = (230, 126, 34, 100)


class Theme:
    winter = {
        "name": "寒冬",
        "primary": Color.__dict__["white"],
        "secondary": Color.__dict__["light_grey_alpha"],
        "emphasize": Color.__dict__["reddish_blue_alpha"],
        "line": Color.__dict__["black"],
        "number": Color.__dict__["black"],
        "font": Color.__dict__["grey"],
        "wrong": Color.__dict__["chi_gong"],
        "normal": {
            "bubble": Color.__dict__["white_alpha"],
            "button": Color.__dict__["white_alpha"],
            "border": Color.__dict__["grey_alpha"],
            "font": Color.__dict__["grey_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["white"],
            "button": Color.__dict__["white"],
            "border": Color.__dict__["grey"],
            "font": Color.__dict__["grey"]
        },
        "hover": {
            "bubble": Color.__dict__["white"],
            "button": Color.__dict__["white"],
            "border": Color.__dict__["grey"],
            "font": Color.__dict__["black"]
        },
        "click": {
            "bubble": Color.__dict__["white"],
            "button": Color.__dict__["reddish_blue_alpha"],
            "border": Color.__dict__["grey"],
            "font": Color.__dict__["black"]
        }
    }

    dark = {
        "name": "暗黑",
        "primary": Color.__dict__["black_pearl"],
        "secondary": Color.__dict__["blue_night_alpha"],
        "emphasize": Color.__dict__["sun_flower"],
        "line": Color.__dict__["white"],
        "number": Color.__dict__["white"],
        "font": Color.__dict__["white"],
        "wrong": Color.__dict__["chi_gong"],
        "normal": {
            "bubble": Color.__dict__["black_pearl"],
            "button": Color.__dict__["black_pearl"],
            "border": Color.__dict__["sun_flower_alpha"],
            "font": Color.__dict__["white_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["black_pearl"],
            "button": Color.__dict__["black_pearl"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["white"]
        },
        "hover": {
            "bubble": Color.__dict__["black_pearl"],
            "button": Color.__dict__["black_pearl"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["white"]
        },
        "click": {
            "bubble": Color.__dict__["black_pearl"],
            "button": Color.__dict__["sun_flower"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["white"]
        }
    }

    new_year = {
        "name": "新年",
        "primary": Color.__dict__["chi_gong"],
        "secondary": Color.__dict__["alizarin_alpha"],
        "emphasize": Color.__dict__["sun_flower_alpha"],
        "line": Color.__dict__["sun_flower"],
        "number": Color.__dict__["black"],
        "font": Color.__dict__["black"],
        "wrong": Color.__dict__["white"],
        "normal": {
            "bubble": Color.__dict__["chi_gong_alpha"],
            "button": Color.__dict__["chi_gong_alpha"],
            "border": Color.__dict__["sun_flower_alpha"],
            "font": Color.__dict__["grey_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["chi_gong"],
            "button": Color.__dict__["chi_gong"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["black"]
        },
        "hover": {
            "bubble": Color.__dict__["chi_gong"],
            "button": Color.__dict__["chi_gong"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["black"]
        },
        "click": {
            "bubble": Color.__dict__["chi_gong"],
            "button": Color.__dict__["sun_flower_alpha"],
            "border": Color.__dict__["sun_flower"],
            "font": Color.__dict__["black"]
        }
    }

    spring = {
        "name": "暖春",
        "primary": Color.__dict__["aurora_green"],
        "secondary": Color.__dict__["ufo_green_alpha"],
        "emphasize": Color.__dict__["sun_flower_alpha"],
        "line": Color.__dict__["green_sea"],
        "number": Color.__dict__["black"],
        "font": Color.__dict__["black"],
        "wrong": Color.__dict__["chi_gong"],
        "normal": {
            "bubble": Color.__dict__["aurora_green_alpha"],
            "button": Color.__dict__["aurora_green_alpha"],
            "border": Color.__dict__["green_sea_alpha"],
            "font": Color.__dict__["grey_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["aurora_green"],
            "button": Color.__dict__["aurora_green"],
            "border": Color.__dict__["green_sea"],
            "font": Color.__dict__["black"]
        },
        "hover": {
            "bubble": Color.__dict__["aurora_green"],
            "button": Color.__dict__["aurora_green"],
            "border": Color.__dict__["green_sea"],
            "font": Color.__dict__["black"]
        },
        "click": {
            "bubble": Color.__dict__["aurora_green"],
            "button": Color.__dict__["sun_flower_alpha"],
            "border": Color.__dict__["green_sea"],
            "font": Color.__dict__["black"]
        }
    }

    summer = {
        "name": "夏雨",
        "primary": Color.__dict__["green_darner_tail"],
        "secondary": Color.__dict__["joust_blue_alpha"],
        "emphasize": Color.__dict__["saturated_sky_alpha"],
        "line": Color.__dict__["green_sea"],
        "number": Color.__dict__["black"],
        "font": Color.__dict__["black"],
        "wrong": Color.__dict__["chi_gong"],
        "normal": {
            "bubble": Color.__dict__["green_darner_tail_alpha"],
            "button": Color.__dict__["green_darner_tail_alpha"],
            "border": Color.__dict__["merchant_marine_blue_alpha"],
            "font": Color.__dict__["grey_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["green_darner_tail"],
            "button": Color.__dict__["green_darner_tail"],
            "border": Color.__dict__["merchant_marine_blue"],
            "font": Color.__dict__["black"]
        },
        "hover": {
            "bubble": Color.__dict__["green_darner_tail"],
            "button": Color.__dict__["green_darner_tail"],
            "border": Color.__dict__["merchant_marine_blue"],
            "font": Color.__dict__["black"]
        },
        "click": {
            "bubble": Color.__dict__["green_darner_tail"],
            "button": Color.__dict__["saturated_sky_alpha"],
            "border": Color.__dict__["merchant_marine_blue"],
            "font": Color.__dict__["black"]
        }
    }

    autumn = {
        "name": "丰秋",
        "primary": Color.__dict__["beekeeper"],
        "secondary": Color.__dict__["radiant_yellow_alpha"],
        "emphasize": Color.__dict__["carrot_alpha"],
        "line": Color.__dict__["puffins_bill"],
        "number": Color.__dict__["black"],
        "font": Color.__dict__["black"],
        "wrong": Color.__dict__["chi_gong"],
        "normal": {
            "bubble": Color.__dict__["beekeeper_alpha"],
            "button": Color.__dict__["beekeeper_alpha"],
            "border": Color.__dict__["puffins_bill_alpha"],
            "font": Color.__dict__["grey_alpha"]
        },
        "hover_on_parent": {
            "bubble": Color.__dict__["beekeeper_alpha"],
            "button": Color.__dict__["beekeeper_alpha"],
            "border": Color.__dict__["puffins_bill"],
            "font": Color.__dict__["black"]
        },
        "hover": {
            "bubble": Color.__dict__["beekeeper"],
            "button": Color.__dict__["beekeeper"],
            "border": Color.__dict__["puffins_bill"],
            "font": Color.__dict__["black"]
        },
        "click": {
            "bubble": Color.__dict__["beekeeper"],
            "button": Color.__dict__["carrot_alpha"],
            "border": Color.__dict__["puffins_bill"],
            "font": Color.__dict__["black"]
        }
    }


theme = Theme()
theme_list = [theme.winter, theme.dark, theme.new_year, theme.spring, theme.summer, theme.autumn]
