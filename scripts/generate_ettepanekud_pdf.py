#!/usr/bin/env python3
"""Generate PDF: Kaitseliidu relvaseaduse ettepanekud."""

from pathlib import Path

from fpdf import FPDF

OUTPUT = Path("/workspace/Kaitseliidu-relvaseaduse-ettepanekud.pdf")
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


class EstonianPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Lehekülg {self.page_no()}/{{nb}}", align="C")


def setup_fonts(pdf: FPDF) -> None:
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))


def title_page(pdf: FPDF) -> None:
    pdf.add_page()
    pdf.set_font("DejaVu", "B", 20)
    pdf.ln(40)
    pdf.multi_cell(0, 12, "Kaitseliidu relvaseaduse ja\nsellega seotud regulatsioonide\nmuutmise ettepanekud", align="C")
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(
        0,
        8,
        "Analüüs kehtivatest regulatsioonidest, kitsaskohtadest\n"
        "ja ettepanekutest bürokraatia vähendamiseks\n"
        "ning valmisoleku suurendamiseks",
        align="C",
    )
    pdf.ln(20)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 8, "Koostatud: juuni 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Saatmiseks: raivo.tamm@kaitseliit.ee (tähtaeg 23. juuni)", align="C")


def section(pdf: FPDF, heading: str, level: int = 1) -> None:
    sizes = {1: 14, 2: 12, 3: 11}
    pdf.ln(4 if level > 1 else 6)
    pdf.set_font("DejaVu", "B", sizes.get(level, 11))
    pdf.set_text_color(20, 60, 100) if level == 1 else pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, heading)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def body(pdf: FPDF, text: str) -> None:
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(1)


def bullet(pdf: FPDF, text: str) -> None:
    pdf.set_font("DejaVu", "", 10)
    x = pdf.get_x()
    pdf.cell(6, 5.5, "•")
    pdf.multi_cell(0, 5.5, text)
    pdf.set_x(x)


def table_row(pdf: FPDF, cols: list[str], widths: list[int], bold: bool = False) -> None:
    style = "B" if bold else ""
    pdf.set_font("DejaVu", style, 9)
    h = 6
    for col, w in zip(cols, widths):
        pdf.cell(w, h, col, border=1)
    pdf.ln(h)


def build_pdf() -> None:
    pdf = EstonianPDF()
    pdf.alias_nb_pages()
    setup_fonts(pdf)
    pdf.set_auto_page_break(auto=True, margin=20)

    title_page(pdf)

    # 1. Kokkuvõte
    pdf.add_page()
    section(pdf, "1. Kokkuvõte", 1)
    body(
        pdf,
        "Kaitseliidu Keskkogu on kutsunud koguma ettepanekuid relvaseaduse ja sellega "
        "seotud regulatsioonide muutmiseks. Eesmärk on leida kohti, kus kehtiv regulatsioon "
        "ei vasta enam tegelikele vajadustele või takistab põhjendamatult väljaõpet, "
        "relvaomanike tegevust ning Kaitseliidu ülesannete täitmist.",
    )
    body(
        pdf,
        "See dokument koondab analüüsi kehtivast õigusest, avalikust tagasisidest, "
        "tegevliikme teekonna stenaariumidest ning konkreetsetest ettepanekutest. "
        "Peamine siht: säästa aega ja raha, vähendada bürokraatiat ning suurendada "
        "tegelikku riigikaitsevalmisolekut.",
    )

    # 2. Metoodika
    section(pdf, "2. Allikad ja metoodika", 1)
    bullet(pdf, "Relvaseadus, Kaitseliidu seadus, kaitseministri määrused (Riigi Teataja)")
    bullet(pdf, "Malevkondade ametlikud juhendid (nt Nõmme malevkond, Lääne malevkond)")
    bullet(pdf, "Eesti Relvaomanike Liit, Eesti Laskurliit — ettepanekud ja pöördumised")
    bullet(pdf, "ERR, Uued Uudised, Forte/Delfi — avalik arutelu")
    bullet(pdf, "Stenaariumianalüüs: tegevliikme teekond relvani")

    # 3. Tegevliikme teekond
    section(pdf, "3. Tegevliikme teekond — stenaarium ja kitsaskohad", 1)
    section(pdf, "3.1 Uus liige soovib relva kodusele hoiule", 2)

    widths = [42, 48, 35, 55]
    table_row(pdf, ["Etapp", "Tegevus", "Aeg", "Kitsaskoht"], widths, bold=True)
    rows = [
        ["Liitumine", "Astumine, taustakontroll", "1–3 kuud", "Malevkonna koormus"],
        ["Ootamine", "1 aasta + 48 h KL tegevust", "12+ kuud", "Blokeerib motiveeritud liikmeid"],
        ["Relvakapp", "Statsionaarne kapp", "200–800 €", "Defitsiit malevates"],
        ["Relvaeksam", "Teooria + TEST 1 + laskekatse", "Kvartalis 1×", "Pudelikael, 2 kuu tähtaeg"],
        ["PPA luba", "Isikliku relva korral", "+2 kuud", "Topelteksam"],
        ["Hoiuõigus", "Taotlus + kodukontroll", "Kuni 90 päeva", "Eraldi menetlus"],
        ["Väljastus", "Relvur / pealik", "Muutuv", "Mitmeastmeline ahel"],
    ]
    pdf.set_font("DejaVu", "", 8)
    for row in rows:
        y0 = pdf.get_y()
        x0 = pdf.get_x()
        heights = []
        for col, w in zip(row, widths):
            pdf.set_xy(x0 + sum(widths[: row.index(col)]), y0)
            pdf.multi_cell(w, 5, col, border=1)
            heights.append(pdf.get_y() - y0)
        pdf.set_y(y0 + max(heights))

    body(
        pdf,
        "Kokku: motiveeritud uus liige jõuab kodusele relvale realistlikult 18–24 kuu "
        "pärast astumist. Sõjaaja kontekstis on see ebaproportsionaalne.",
    )

    section(pdf, "3.2 Puhkus, komandeering, väljasõit", 2)
    body(
        pdf,
        "Kaitseministri määruse nr 7 § 8 järgi: kui tegevliige ei viibi elukohas järjest "
        "üle 14 päeva, peab ta väljaspool relvakappi hoitava relva ja moona viima "
        "Kaitseliitu hoiule. Kui puudumine ületab 6 kuud, tuleb kõik relvad koju hoiule KL-i.",
    )
    body(
        pdf,
        "Praktikas sunnib see reisivat liiget pidevalt halduskoormuse alla: transport, "
        "logistika, relvuri aeg, dokumentatsioon.",
    )

    # 4. Avalik tagasiside
    section(pdf, "4. Avalik tagasiside ja kaebused", 1)
    section(pdf, "4.1 PPA menetlus (mõjutab ka KL liikmeid isiklike relvadega)", 2)
    bullet(pdf, "Põhjendamiskohustus, mida seaduses pole (nt „miks kolmandat relva vaja?\")")
    bullet(pdf, "Keeldumine mõistlike põhjustega; sotsiaalmeedia skaneerimine")
    bullet(pdf, "Puudub „laskeharrastuse\" otstarve — harrastaja peab kasutama „enese ja vara kaitse\"")
    bullet(pdf, "Eesti Relvaomanike Liit pöördus 2024 õiguskantsleri poole")

    section(pdf, "4.2 Relvaseadus tervikuna", 2)
    bullet(pdf, "Seadus on 60+ korral parandatud, killustunud ja raskesti rakendatav")
    bullet(pdf, "200 padrunit turvalisuse otstarbeks — üks treeningkord tiirus kustutab varu")
    bullet(pdf, "Automaatne loa kehtetuks tunnistamine väikeste rikkumiste korral — puudub kaalutlusõigus")

    section(pdf, "4.3 Kaitseliidu-spetsiifiline tagasiside", 2)
    bullet(pdf, "SA-struktuuri välisel liikmel piiratud ligipääs relvadele")
    bullet(pdf, "Relvaeksam üks kord kvartalis — logistiline pudelikael")
    bullet(pdf, "Relvakapi defitsiit; paberimajandus; mitme rolli segadus (KL + PPA)")

    # 5. Kitsaskohad
    section(pdf, "5. Kitsaskohad kategooriate kaupa", 1)
    section(pdf, "Kriitilised", 2)
    bullet(pdf, "1 aasta + 48 h nõue enne KL relvaluba")
    bullet(pdf, "Topeltsüsteem: KL luba + PPA luba + hoiuõigus + soetamisluba")
    bullet(pdf, "14-päevane puudumise reegel")
    bullet(pdf, "Eksamite haruldus ja 2 kuu tähtaeg")
    bullet(pdf, "90-päevane hoiuõiguse menetlus + füüsiline kodukontroll")

    section(pdf, "Olulised (raha ja aeg)", 2)
    bullet(pdf, "Relvakapi kohustus ja defitsiit; laskemoona eraldi sektsioon")
    bullet(pdf, "Soetamisluba iga ostu kohta; riigikaitse märge eraldi PPA-s")
    bullet(pdf, "Riigilõivud: relvaeksam 90 €, pikendamine 75 €")

    # 6. Juba parandatav
    section(pdf, "6. Plaanitud ja jõustunud muudatused (2024–2026)", 1)
    bullet(pdf, "Laskemoona kodus 5000/10000 padrunit (jõustunud 2024)")
    bullet(pdf, "Jahirelva kasutus teenistuses; tervisetõendi lihtsustamine")
    bullet(pdf, "Plaan 2026: soetamis-/võõrandamisloa kaotamine (PPA), laskeharrastuse otstarve")
    bullet(pdf, "NB: KL tegevliikme relv jääb eraldi süsteemi — topeltsüsteem säilib")

    # 7. PEAMINE ETTEPANEK - staaž
    pdf.add_page()
    section(pdf, "7. PRIORITEETNE ETTEPANEK: Staažinõude täielik kaotamine", 1)

    section(pdf, "7.1 Probleem", 2)
    body(
        pdf,
        "Praegu ei saa tegevliige taotleda Kaitseliidu relvaluba ega relva kodusele "
        "hoiule võtmist enne, kui ta on olnud tegevliige vähemalt 1 aasta ja osalenud "
        "vähemalt 48 tundi Kaitseliidu tegevuses. See tuleneb Kaitseliidu seaduse § 43-st.",
    )
    body(
        pdf,
        "Inimene, kes on läbinud relvaõppe, sooritanud relvaeksami ja täitnud hoiutingimused, "
        "peab siiski ootama kuude või üle aasta ainult seetõttu, et seaduses on kirjas "
        "ajaline miinimum. See ei suurenda turvalisust ega valmisolekut.",
    )

    section(pdf, "7.2 Miks staažinõue on mõttetu pärast relvaõpet ja eksamit", 2)
    body(
        pdf,
        "Tüüpiline uue tegevliikme tee: astumine → relvaõpe (sageli esimene väljaõpe) → "
        "esmaabikoolitus → relvaeksam → seejärel ootamine kuni kalendriline staaž täitub.",
    )
    body(
        pdf,
        "Staažinõue ei kontrolli midagi, mida eksam ja tingimused juba ei kontrolliks. "
        "Kui inimene on läbinud relvaõppe, sooritanud relvaeksami, omab relvakappi "
        "ja läbib taustakontrolli, on ta valmis relva kodusele hoiule võtma.",
    )

    section(pdf, "7.3 Ettepanek", 2)
    body(pdf, "Asendada ajapõhine staažinõue tingimuspõhise lähenemisega.")
    body(pdf, "Kaitseliidu relvaluba ja kodune hoiuõigus antakse tegevliikmele, kes:")
    bullet(pdf, "on tasunud liikmemaksu")
    bullet(pdf, "vastab § 43 lg 2 ja lg 3 nõuetele (taust, tervis, välistavad asjaolud puuduvad)")
    bullet(pdf, "on läbinud nõutava relvaõppe ja sooritanud relvaeksami")
    bullet(pdf, "on täitnud relva ja laskemoona koduse hoidmise tingimused (sh relvakapp)")
    bullet(pdf, "on läbinud esmaabikoolituse")
    body(
        pdf,
        "Staažinõuet (1 aasta ja 48 tundi) ei kohaldata relvaloa ja koduse hoiuõiguse "
        "esmase saamise korral. Lähenemine: kui täidad tingimused, saad relva kodusele hoiule.",
    )

    section(pdf, "7.4 Muudetavad aktid", 2)
    bullet(pdf, "Kaitseliidu seadus § 43")
    bullet(pdf, "Kaitseministri määrus nr 14 „Kaitseliidu relvaloa andmise ja väljastamise kord\"")
    bullet(pdf, "Kaitseministri määrus nr 7 koduse hoiuõiguse osas (vajadusel)")

    section(pdf, "7.5 Oodatav tulemus", 2)
    widths2 = [55, 55, 70]
    table_row(pdf, ["Näitaja", "Praegu", "Pärast muudatust"], widths2, bold=True)
    for row in [
        ["Aeg relvani", "12–24 kuud", "2–4 kuud"],
        ["Motivatsioon", "Kõrge kadu ooteajal", "Paraneb"],
        ["Halduskoormus", "Taotlused „ootel staaži\"", "Ainult sisulised menetlused"],
    ]:
        table_row(pdf, row, widths2)

    # 8. Muud ettepanekud
    section(pdf, "8. Täiendavad ettepanekud", 1)

    section(pdf, "8.1 Seadusandlikud", 2)
    proposals = [
        ("A2", "Ühendada KL relvaluba ja hoiuõigus üheks menetluseks"),
        ("A3", "Kaotada/asendada 14-päevane hoiuleviimise kohustus riskipõhise reegliga"),
        ("A4", "Liita tegevliikme relva soetamine digitaalse taotlusega mõlemasse registrisse"),
        ("A5", "Riigikaitse märge automaatselt aktiivsetele tegevliikmetele"),
        ("A6", "Tunnistada KL relvaeksam ja PPA eksam vastastikku võrdseks"),
        ("A7", "Laskeharrastuse otstarve ka KL B-kategooria jaoks ilma võistlusnõudeta"),
    ]
    for code, text in proposals:
        bullet(pdf, f"{code}: {text}")

    section(pdf, "8.2 Määruste / menetluse muudatused", 2)
    for code, text in [
        ("B1", "Relvaeksam iga kuu või malevkonna tiirus — mitte ainult kvartalis"),
        ("B2", "Digitaalne taotluste süsteem (sarnane relvataotlus.politsei.ee)"),
        ("B3", "Eelkontroll fotode/videokõnega, kui kapp juba sertifitseeritud"),
        ("B4", "Standardne relvakapp maleva laenutusena"),
        ("B5", "Ühtlustada ja uuendada eksamimaterjalid"),
    ]:
        bullet(pdf, f"{code}: {text}")

    section(pdf, "8.3 Kaitseliidu sisekord (kohe rakendatav)", 2)
    for code, text in [
        ("C1", "Ühtne „teekonna kaart\" iga malevkonna kodulehel"),
        ("C2", "Relvuri koormuse jälgimine — teavitamine kui menetlus >60 päeva"),
        ("C3", "Selge tee mitte-SA liikmetele maleva relva kodusele hoiule"),
        ("C4", "Eksamile registreerimine iseteeninduses"),
    ]:
        bullet(pdf, f"{code}: {text}")

    # 9. Prioriteedid
    section(pdf, "9. Prioriteetide järjekord", 1)
    priorities = [
        "1. Staažinõude täielik kaotamine — tingimuspõhine mudel",
        "2. Topeltmenetluse kaotamine (relvaluba + hoiuõigus üheks)",
        "3. 14-päevase puudumise reegli paindlustamine",
        "4. Eksami kättesaadavuse parandamine",
        "5. Digitaalne menetlus",
    ]
    for p in priorities:
        bullet(pdf, p)

    # 10. Valmis tekst
    pdf.add_page()
    section(pdf, "10. Valmis ettepaneku tekst e-kirja jaoks", 1)
    pdf.set_font("DejaVu", "", 9)
    email_text = (
        "Ettepanek: Kaitseliidu tegevliikme relvaloa ja koduse hoiuõiguse saamise "
        "staažinõude (1 aasta + 48 tundi) täielik kaotamine\n\n"
        "Praegune regulatsioon nõuab, et tegevliige oleks enne relvaloa ja koduse "
        "hoiuõiguse saamist Kaitseliidu liige vähemalt üks aasta ning osalenud vähemalt "
        "48 tundi organisatsiooni tegevuses, kuigi sama perioodi jooksul läbib ta relvaõppe "
        "ja relvaeksami.\n\n"
        "Ettepanek: asendada ajapõhine staažinõue tingimuspõhise lähenemisega. Kui "
        "tegevliige on tasunud liikmemaksu, läbinud taustakontrolli, esmaabikoolituse ja "
        "relvaõppe, sooritanud relvaeksami ning täidab relva ja laskemoona koduse hoidmise "
        "nõuded (sh relvakapp), antakse talle relvaluba ja kodune hoiuõigus ilma "
        "kalendrilise ooteajata.\n\n"
        "Põhjendus: relvaõpe on uue liikme esimene ja põhiline väljaõpe; eksam kontrollib "
        "pädevust, mida staažinõue formaalselt ei mõõda. Kalendrilise ooteaja taga puudub "
        "sisuline turvalisuse või valmisoleku argument. Tingimuste täitmisel peaks liige "
        "saama relva kodusele hoiule — see on kooskõlas Kaitseliidu eesmärgiga suurendada "
        "riigikaitsevalmisolekut ja vähendada bürokraatiat.\n\n"
        "Muudetavad aktid: Kaitseliidu seadus § 43, kaitseministri määrus nr 14, "
        "vajadusel määrus nr 7."
    )
    pdf.set_fill_color(245, 245, 245)
    pdf.multi_cell(0, 5, email_text, fill=True)

    section(pdf, "Kontakt", 2)
    body(pdf, "Saatmine: raivo.tamm@kaitseliit.ee")
    body(pdf, "Tähtaeg: 23. juuni 2026 (MHK 23JUN)")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    print(f"PDF loodud: {OUTPUT} ({OUTPUT.stat().st_size} baiti)")


if __name__ == "__main__":
    build_pdf()
