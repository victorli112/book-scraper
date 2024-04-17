# ~94 books + ~242 books + ~167 books
AVENTURAS_AND_FANTASIA_AND_CLASICOS = {
    "output_file": "aventuras_and_fantasia_and_grandes_clasicos.xlsx",
    "start_urls": ["https://www.penguinlibros.com/ar/40915-aventuras",
                   "https://www.penguinlibros.com/ar/40919-fantasia",
                   "https://www.penguinlibros.com/ar/40923-grandes-clasicos"],
}

# ~2,347/2 books
LITERATURA_CONTEMP_1 = {
    "output_file": "literatura_contemp_1.xlsx",
    "start_urls": ["https://www.penguinlibros.com/ar/40925-literatura-contemporanea"],
    "end_page": 50,
}

# ~2,347/2 books
LITERATURA_CONTEMP_2 = {
    "output_file": "literatura_contemp_2.xlsx",
    "start_urls": ["https://www.penguinlibros.com/ar/40925-literatura-contemporanea?pageno=50"],
}

# 728 books + 143 books + 76 books
NOVELA_NEGRA_AND_CIENCIA_AND_POESIA = {
    "output_file": "novela_negra_and_ciencia_and_poesia.xlsx",
    "start_urls": ["https://www.penguinlibros.com/ar/40929-novela-negra-misterio-y-thriller",
                   "https://www.penguinlibros.com/ar/40917-ciencia-ficcion",
                   "https://www.penguinlibros.com/ar/40933-poesia"],
}

# 650 books + 469 books
NOVELA_ROMANTICA_AND_HISTORICA = {
    "output_file": "novela_romantica_and_historica.xlsx",
    "start_urls": ["https://www.penguinlibros.com/ar/40931-novela-romantica",
                   "https://www.penguinlibros.com/ar/40927-novela-historica"],
}

## ONLY MODIFY THIS VARIABLE ##
# AVENTURAS_AND_FANTASIA_AND_CLASICOS | LITERATURA_CONTEMP_1 | LITERATURA_CONTEMP_2 | NOVELA_NEGRA_AND_CIENCIA_AND_POESIA | NOVELA_ROMANTICA_AND_HISTORICA
CURRENT_BATCH = NOVELA_ROMANTICA_AND_HISTORICA
