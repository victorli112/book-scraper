# ~2,600 books
NOVELA_CONTEMP = {
    "output_file": "novela_contemporanea.xlsx",
    "start_urls": ["https://www.planetadelibros.com.ar/libros/novelas/00038/p/1?q=30"],
}

# ~3,100 books
NOVELA_LITERARIA = {
    "output_file": "novela_literaria.xlsx",
    "start_urls": ["https://www.planetadelibros.com.ar/libros/novela-literaria/00012/p/1?q=30",
                  "https://www.planetadelibros.com.ar/libros/teatro/00052/p/1?q=30"],
}

# ~833 books + ~77 Books
NOVELA_NEGRA_AND_TEATRO = {
    "output_file": "novela_negra.xlsx",
    "start_urls": ["https://www.planetadelibros.com.ar/libros/novela-negra/00015/p/1?q=30"],
}

# ~1,755 books
NOVELAS_ROMANTICAS = {
    "output_file": "novelas_romanticas.xlsx",
    "start_urls": ["https://www.planetadelibros.com.ar/libros/novelas-romanticas/00014/p/1?q=30"],
}

# ~417 + ~586 books
POESIA_AND_HISTORICA = {
    "output_file": "poesia_historica.xlsx",
    "start_urls": ["https://www.planetadelibros.com.ar/libros/poesia/00051/p/1?q=30", 
                   "https://www.planetadelibros.com.ar/libros/novela-historica/00013/p/1?q=30"],
}

## ONLY MODIFY THIS VARIABLE ##
# NOVELA_CONTEMP | NOVELA_LITERARIA | NOVELA_NEGRA_AND_TEATRO | NOVELAS_ROMANTICAS | POESIA_AND_HISTORICA
CURRENT_BATCH = POESIA_AND_HISTORICA
