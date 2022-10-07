import re
from pathlib import Path

HERE = Path(__file__).parent.resolve()

page = HERE.parent.joinpath("data/page.txt").read_text()
new_page = page

singular = "urubu-rei"
plural = "urubus-rei"


species_tuples = [
    ("abutres-rei", plural),
    # ("oliveiras", plural),
    ("abutre-rei", singular),
    # ("potoo", singular)
    # ("oliveira ridley", singular),
    # ("oliveira", singular),
    # ("tartarugas marinhas verdes", plural),
]


regex_and_replacements = [
    ("{{Cvt\|(.{,6}?)\|km2\|sqmi}}", r"\1 quilômetros quadrados"),
    ("{{Cvt\|(.{,6}?)\|-\|(.{,6}?)\|cm\|ftin\|0}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|-\|(.{,6}?)\|cm\|in}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|cm\|in}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|to\(-\)\|(.{,6}?)\|cm\|in}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|to\(-\)\|(.{,6}?)\|cm\|in\|0}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|in\|cm}}", r"\1 a \2 polegadas"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|cm\|ftin\|0}}", r"\1 a \2 centímetros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|m\|ft}}", r"\1 a \2 metros"),
    ("{{Cvt\|(.{,6}?)\|to\(-\)\|(.{,6}?)\|m\|ft\|0}}", r"\1 a \2 metros"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|kg\|lb}}", r"\1 a \2 quilos"),
    ("{{Cvt\|(.{,6}?)\|to\(-\)\|(.{,6}?)\|kg\|lb\|0}}", r"\1 a \2 quilos"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|m\|ftin\|0}}", r"\1 a \2 metro"),
    ("{{Cvt\|(.{,6}?)\|and\|(.{,6}?)\|m\|ft}}", r"\1 e \2 metros"),
    ("{{Cvt\|(.{,6}?)\|and\|(.{,6}?)\|g\|oz}}", r"\1 e \2 gramas"),
    ("{{Cvt\|(.{,6}?)\|to\|(.{,6}?)\|mm\|in}}", r"\1 a \2 milímetros"),
    ("{{Cvt\|(.{,6}?)\|x\|(.{,6}?)\|mm\|in}}", r"\1 por \2 milímetros"),
    ("{{Cvt\|(.{,6}?)\|-\|(.{,6}?)\|km/h}}", r"\1 a \2 km/h"),
    ("{{Cvt\|(.{,6}?)\|m\|ft}}", r"\1 metros"),
    ("{{Cvt\|(.{,6}?)\|m\|ft\|0}}", r"\1 metros"),
    ("{{Cvt\|(.{,6}?)\|ha\|acres}}", r"\1 hectares"),
    ("{{Cvt\|(.{,6}?)\|kg\|lb}}", r"\1 quilos"),
    ("{{Cvt\|(.{,6}?)\|km\|mi}}", r"\1 quilômetros"),
    ("{{Cvt\|(.{,6}?)\|m\|ftin\|0}}", r"\1 metro"),
    ("{{Cvt\|(.{,6}?)\|mm\|in}}", r"\1 milímetros"),
    ("{{Cvt\|(.{,6}?)\|cm\|in}}", r"\1 centímetros"),
    ("{{Cvt\|(.{,6}?)\|cm\|in\|0}}", r"\1 centímetros"),
    ("{{Cvt\|(.{,6}?)\|g\|oz}}", r"\1 gramas"),
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


results = re.findall(f'<ref name="(.*?)">', new_page)
print(results)

import collections

repeated_refs = [
    item for item, count in collections.Counter(results).items() if count > 1
]
print(repeated_refs)


repeated_refs.extend(["Mayumba", "NSLTWG", "WWFEcology"])
for ref_name in repeated_refs:
    new_page = clean_ref(ref_name, new_page)
HERE.parent.joinpath("results/new_page.txt").write_text(new_page)
