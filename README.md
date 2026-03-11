iambic.py is a python program that write bad poetry in iambic pentameter.
It comes with several options, none of which are an option to write good poetry.

```
usage: iambic_pentameter.py [-h] [--theme {night,nature,time,love,sea}] [--stanzas STANZAS] [--lines LINES]
                            [--rhyme RHYME] [--scansion] [--seed SEED] [--count COUNT]

Generate poems in iambic pentameter

options:
  -h, --help            show this help message and exit
  --theme {night,nature,time,love,sea}
                        Poem theme (default: night)
  --stanzas STANZAS     Number of stanzas (default: 3)
  --lines LINES         Lines per stanza (default: 4)
  --rhyme RHYME         Rhyme scheme: abab, aabb, abba, none (default: abab)
  --scansion            Show scansion marks below each stanza
  --seed SEED           Random seed for reproducibility
  --count COUNT         Number of poems to generate

Examples:
  python3 iambic.py                           # Default: 3 stanzas, night theme
  python3 iambic.py --theme love --rhyme aabb # Love poem, couplet rhymes
  python3 iambic.py --theme sea --stanzas 4 --scansion  # With scansion marks
  python3 iambic.py --theme nature --lines 2 --rhyme aa  # Short couplet stanzas
  python3 iambic.py --theme love --rhyme aabb --scansion
  python3 iambic.py --theme sea --stanzas 4 --lines 6 --rhyme ababcc    
```