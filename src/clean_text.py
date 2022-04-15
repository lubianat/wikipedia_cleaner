import re
from pathlib import Path

HERE = Path(__file__).parent.resolve()


page = HERE.parent.joinpath("data/page.txt").read_text()

regex = "{{Cvt\|(.*?)\|to\|(.*?)\|(.*?)\|.*}}"

replacement = r"\1 a \2 \3"
new_page = re.sub(pattern=regex, repl=replacement, string=page)

regex = "{{Cvt\|(.*?)\|(.*?)\|.*}}"
replacement = r"\1 \2"
new_page = re.sub(pattern=regex, repl=replacement, string=new_page)

new_page = re.sub(pattern=" \.", repl=".", string=new_page)

HERE.parent.joinpath("results/new_page.txt").write_text(new_page)
