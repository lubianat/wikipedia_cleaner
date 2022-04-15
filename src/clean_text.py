import re
from pathlib import Path

HERE = Path(__file__).parent.resolve()

page = HERE.parent.joinpath("data/page.txt").read_text()
new_page = page

species_tuples = [
    ("gavião-preto", "gavião-pega-macaco"),
    ("as espécies ornamentadas", "os gaviões-de-penacho"),
    ("gaviões ornamentados", "gaviões-de-penacho"),
    ("gavião ornamentado", "gavião-de-penacho"),
    ("as águias-de-falcão ornamentadas", "os gaviões-de-penacho"),
    ("águia-falcão", "ave"),
]


regex_and_replacements = [
    ("{{Cvt\|(.{,6}?)\|m\|ft}}", r"\1 metros"),
    ("{{Cvt\|(.{,6}?)\|m\|ftin\|0}}", r"\1 metro"),
    ("{{Cvt\|(.{,6}?)\|mm\|in}}", r"\1 milímetros"),
    ("{{Cvt\|(.{,6}?)\|cm\|in}}", r"\1 centímetros"),
    ("{{Cvt\|(.{,6}?)\|g\|oz}}", r"\1 gramas"),
    ("{{Cvt\|(.{,6}?)\|km2\|sqmi}}", r"\1 quilômetros quadrados"),
    ("{{Cvt\|(.{,6}?)\|to\|(.*?)\|m\|ft}}", r"\1 a \2 metros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.*?)\|m\|ftin\|0}}", r"\1 a \2 metro"),
    ("{{Cvt\|(.{,6}?)\|and\|(.*?)\|m\|ft}}", r"\1 e \2 metros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.*?)\|mm\|in}}", r"\1 a \2 milímetros"),
    ("{{Cvt\|(.{,6}?)\|x\|(.*?)\|mm\|in}}", r"\1 por \2 milímetros"),
    (" \.", "."),
    ("\( ", "("),
    (" \)", ")"),
]
regex_and_replacements.extend(species_tuples)

for tuple in regex_and_replacements:
    print(tuple)
    regex = tuple[0]
    replacement = tuple[1]
    new_page = re.sub(pattern=regex, repl=replacement, string=new_page)


def clean_ref(ref_name, new_page):
    parts = new_page.partition(f'"{ref_name}"')  # returns a tuple
    new_page = (
        parts[0]
        + parts[1]
        + re.sub(
            f'<ref name="{ref_name}">.*?</ref>',
            f'<ref name="{ref_name}"/>',
            parts[2],
        )
    )
    return new_page


refs_to_clean = ["Ferguson-Lees", "Uplist"]

for ref_name in refs_to_clean:
    new_page = clean_ref(ref_name, new_page)
HERE.parent.joinpath("results/new_page.txt").write_text(new_page)
