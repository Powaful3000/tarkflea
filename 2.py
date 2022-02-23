import d3dshot
import cv2
import numpy as np
from numba import njit
from numba.core import types
from numba.typed import Dict


items = [
    ["0.6 liter water bottle", "water.png"],
    ["42nd Signature Blend English Tea", "tea.png"],
    ["5L propane tank", "propane.png"],
    ["AI-2 medkit", "cheese.png"],
    ["Alyonka chocolate bar", "chocolate.png"],
    ["Analgin painkillers", "pk.png"],
    ["Antique teapot", "teapot.png"],
    ["Aseptic bandage", "bandage.png"],
    ["Bolts", "bolts.png"],
    ["Broken GPhone X smartphone", "gpx.png"],
    ["Bronze lion", "lion.png"],
    ["Can of beef stew (Large)", "stewlarge.png"],
    ["Can of condensed milk", "conmilk.png"],
    ["Can of Hot Rod energy drink", "hotrod.png"],
    ["Can of Majaica coffee beans", "coffee.png"],
    ["Car Battery", "carbattery.png"],
    ["Electric drill", "edrill.png"],
    ["Expeditionary fuel tank", "bluefuel.png"],
    ["Freeman crowbar", "crowbar.png"],
    ["Gas analyzer", "gasan.png"],
    ["Golden neck chain", "goldchain.png"],
    ["Gloden rooster", "cock.png"],
    ["Golden Star balm", "goldenstar.png"],
    ["Graphics Card", "gpu.png"],
    ["Grizzly medical kit", "grizzly.png"],
    ["Horse figurine", "horse.png"],
    ["Immobilizing splint", "imsplint.png"],
    ["Insulating tape", "tape.png"],
    ["Morphine injector", "morphine.png"],
    ["Pack of sodium bicarbonate", "bic.png"],
    ["Pack of sugar", "sugar.png"],
    ["Pliers", "pliers.png"],
    ["Printer paper", "paper.png"],
    ["Red Rebel ice pick", "redrebel.png"],
    ["Salewa first aid kit", "salewa.png"],
    ["Screwdriver", "screwdriver.png"],
    ["Spark plug", "splug.png"],
    ["Strike Cigarettes", "strike.png"],
    ["T-Shaped plug", "tplug.png"],
    ["Toilet paper", "tp.png"],
    ["Vaseline balm", "vaseline.png"],
    ["WD-40 (100ml)", "wd40.png"],
    ["Wrench", "wrench.png"],
    ["Xenomorph sealing foam", "xeno.png"],
    ["Zibbo lighter", "zibbo.png"],
    ['"Fierce Hatchling" moonshine', "moonshine.png"],
    ['Gunpowder "Eagle"', "greenpowder.png"],
]


@njit(fastmath=True, parallel=True)
def create_bot_dict():
    items = [
        ["0.6 liter water bottle", "water.png"],
        ["42nd Signature Blend English Tea", "tea.png"],
        ["5L propane tank", "propane.png"],
        ["AI-2 medkit", "cheese.png"],
        ["Alyonka chocolate bar", "chocolate.png"],
        ["Analgin painkillers", "pk.png"],
        ["Antique teapot", "teapot.png"],
        ["Aseptic bandage", "bandage.png"],
        ["Bolts", "bolts.png"],
        ["Broken GPhone X smartphone", "gpx.png"],
        ["Bronze lion", "lion.png"],
        ["Can of beef stew (Large)", "stewlarge.png"],
        ["Can of condensed milk", "conmilk.png"],
        ["Can of Hot Rod energy drink", "hotrod.png"],
        ["Can of Majaica coffee beans", "coffee.png"],
        ["Car Battery", "carbattery.png"],
        ["Electric drill", "edrill.png"],
        ["Expeditionary fuel tank", "bluefuel.png"],
        ["Freeman crowbar", "crowbar.png"],
        ["Gas analyzer", "gasan.png"],
        ["Golden neck chain", "goldchain.png"],
        ["Gloden rooster", "cock.png"],
        ["Golden Star balm", "goldenstar.png"],
        ["Graphics Card", "gpu.png"],
        ["Grizzly medical kit", "grizzly.png"],
        ["Horse figurine", "horse.png"],
        ["Immobilizing splint", "imsplint.png"],
        ["Insulating tape", "tape.png"],
        ["Morphine injector", "morphine.png"],
        ["Pack of sodium bicarbonate", "bic.png"],
        ["Pack of sugar", "sugar.png"],
        ["Pliers", "pliers.png"],
        ["Printer paper", "paper.png"],
        ["Red Rebel ice pick", "redrebel.png"],
        ["Salewa first aid kit", "salewa.png"],
        ["Screwdriver", "screwdriver.png"],
        ["Spark plug", "splug.png"],
        ["Strike Cigarettes", "strike.png"],
        ["T-Shaped plug", "tplug.png"],
        ["Toilet paper", "tp.png"],
        ["Vaseline balm", "vaseline.png"],
        ["WD-40 (100ml)", "wd40.png"],
        ["Wrench", "wrench.png"],
        ["Xenomorph sealing foam", "xeno.png"],
        ["Zibbo lighter", "zibbo.png"],
        ['"Fierce Hatchling" moonshine', "moonshine.png"],
        ['Gunpowder "Eagle"', "greenpowder.png"],
    ]

    return [[key, cv2.imread("./search/sellItems/botItems/%s" % img)] for [key, img] in items]


def main():
    # create d3dshot object singleton
    d = d3dshot.create(capture_output="numpy", frame_buffer_size=5)
    # start d3dshot capture @ 60fps
    d.capture()  # needs d.stop()

    # create ndarray fake dictionary
    botDictionary = create_bot_dict(items)

    # Enter forever loop
    while 1:
        print("1")

    d.stop()


main()
