"""
gerar_slide.py
Gera um único slide PNG via Playwright (HTML + CSS → screenshot).

Tipos suportados:
  capa, titulo*, bullets, cards, fluxo, metricas,
  hub, split, pipeline, diagrama, comparacao, agenda, encerramento
  (* alias de capa)

Template padrão: 'padrao'  →  renderizador/templates/padrao/base.html
"""

import base64
import json
import os
import sys
import html as html_lib
from pathlib import Path

DIR_RENDERIZADOR = Path(__file__).parent
DIR_RAIZ         = DIR_RENDERIZADOR.parent
TOKENS_PATH      = DIR_RENDERIZADOR / "tokens.json"
TEMA_PADRAO      = "senai-tech-light"
TEMPLATE_PADRAO  = "padrao"

TIPOS_VALIDOS = {
    "capa", "titulo", "bullets", "cards",
    "fluxo", "metricas", "hub", "split", "pipeline",
    "diagrama", "comparacao", "agenda", "encerramento",
}


# ---------------------------------------------------------------------------
# Tokens e temas
# ---------------------------------------------------------------------------

def carregar_tokens() -> dict:
    with open(TOKENS_PATH, encoding="utf-8") as f:
        return json.load(f)


def obter_tema(nome: str) -> dict:
    tokens = carregar_tokens()
    temas  = tokens.get("temas", {})
    if nome not in temas:
        print(f"  ⚠ Tema '{nome}' não encontrado. Usando '{TEMA_PADRAO}'.")
        nome = TEMA_PADRAO
    t = dict(temas[nome])
    t["fonte_titulo"]     = tokens["fontes"].get("titulo", "Poppins")
    t["fonte_corpo"]      = tokens["fontes"].get("corpo",  "Inter")
    t["padding_slide"]    = tokens["espacamentos"].get("padding_slide",    "48px 64px")
    t["border_radius"]    = tokens["espacamentos"].get("border_radius",    "8px")
    t["border_radius_lg"] = tokens["espacamentos"].get("border_radius_lg", "16px")
    return t


def template_path(nome_template: str) -> Path:
    """Resolve o caminho do base.html pelo nome do template."""
    p = DIR_RENDERIZADOR / "templates" / nome_template / "base.html"
    if not p.exists():
        # fallback para o template padrão
        print(f"  ⚠ Template '{nome_template}' não encontrado. Usando 'padrao'.")
        p = DIR_RENDERIZADOR / "templates" / "padrao" / "base.html"
    return p


# ---------------------------------------------------------------------------
# Assets → base64
# ---------------------------------------------------------------------------

def _asset_b64(path: str | None) -> str | None:
    if not path:
        return None
    for candidato in [Path(path), DIR_RAIZ / path, Path(os.getcwd()) / path]:
        if candidato.exists():
            data = base64.b64encode(candidato.read_bytes()).decode()
            ext  = candidato.suffix.lower().lstrip(".")
            mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
            return f"data:{mime};base64,{data}"
    print(f"  ⚠ Asset não encontrado: {path}")
    return None


def e(txt) -> str:
    return html_lib.escape(str(txt))


# ---------------------------------------------------------------------------
# Componentes reutilizáveis
# ---------------------------------------------------------------------------

def _branding(logo_b64: str | None, label: str, claro: bool = False) -> str:
    cls = "branding-area claro" if claro else "branding-area"
    if logo_b64:
        return f'<div class="{cls}"><img class="brand-logo" src="{logo_b64}" alt="{e(label)}"></div>'
    # texto fallback
    partes  = [p.strip() for p in label.split("·")] if "·" in label else [label.strip()]
    p1      = e(partes[0])
    badge   = f'<span class="brand-badge">{e(partes[1])}</span>' if len(partes) > 1 else ""
    return f'<div class="{cls}"><span class="brand-txt">{p1}</span>{badge}</div>'


def _num(n: int, total: int) -> str:
    return f'<span class="num-slide">{n} / {total}</span>'


def _linha_base() -> str:
    return '<div class="linha-base"></div>'


def _header_dark(titulo: str, icone: str | None = None) -> str:
    ic = f'<img class="header-icone" src="{icone}" alt="">' if icone else ""
    return f'<div class="header-dark">{ic}<h2>{e(titulo)}</h2></div>'


# ---------------------------------------------------------------------------
# Construtores por tipo
# ---------------------------------------------------------------------------

def html_capa(d, n, total, logo_b64, branding_label):
    eyebrow  = e(d.get("eyebrow", ""))
    titulo   = e(d.get("titulo", ""))
    sub      = e((d.get("conteudo") or [""])[0])
    ey  = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    sub_h = f'<p class="subtitulo">{sub}</p>' if sub else ""
    return f"""
<div class="slide slide-capa">
  {_branding(logo_b64, branding_label, claro=True)}
  <div class="corpo">{ey}<h1>{titulo}</h1>{sub_h}</div>
  {_num(n, total)}
</div>"""

html_titulo = html_capa


def html_bullets(d, n, total, logo_b64, branding_label):
    titulo = d.get("titulo", "")
    ic     = _asset_b64(d.get("icone_path"))
    bullets = "".join(f"""
      <div class="bullet">
        <span class="bullet-num">{i}</span>
        <span class="bullet-texto">{e(item)}</span>
      </div>""" for i, item in enumerate(d.get("conteudo", []), 1))
    return f"""
<div class="slide slide-bullets">
  {_header_dark(titulo, ic)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo">{bullets}</div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_cards(d, n, total, logo_b64, branding_label):
    titulo = d.get("titulo", "")
    cards  = d.get("cards", [])
    cols   = min(max(len(cards), 2), 4)
    items  = ""
    for i, c in enumerate(cards, 1):
        ic   = _asset_b64(c.get("icone_path"))
        topo = f'<img class="card-icone" src="{ic}" alt="">' if ic else f'<div class="card-num">{i}</div>'
        desc = f'<div class="card-desc">{e(c.get("descricao",""))}</div>' if c.get("descricao") else ""
        items += f'<div class="card-item">{topo}<div class="card-titulo">{e(c.get("titulo",""))}</div>{desc}</div>'
    return f"""
<div class="slide slide-cards">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="grid cols-{cols}">{items}</div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_fluxo(d, n, total, logo_b64, branding_label):
    titulo  = d.get("titulo", "")
    etapas  = d.get("etapas", [])
    metrics = d.get("metricas", [])
    chevs   = "".join(f'<div class="chevron">{e(et.get("label", str(i)))}</div>' for i, et in enumerate(etapas, 1))
    descs   = "".join(f'<div class="desc-item"><div class="desc-titulo">{e(et.get("titulo",""))}</div><div class="desc-sub">{e(et.get("descricao",""))}</div></div>' for et in etapas)
    met_h   = ""
    if metrics:
        cards_m = "".join(f'<div class="metrica-card"><div class="metrica-valor">{e(m.get("valor",""))}</div><div class="metrica-label">{e(m.get("label",""))}</div></div>' for m in metrics)
        met_h = f'<div class="metricas-row">{cards_m}</div>'
    return f"""
<div class="slide slide-fluxo">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo">
    <div class="chevrons">{chevs}</div>
    <div class="descricoes">{descs}</div>
    {met_h}
  </div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_metricas(d, n, total, logo_b64, branding_label):
    titulo  = d.get("titulo", "")
    metrics = d.get("metricas", [])
    cols    = min(max(len(metrics), 2), 4)
    items   = ""
    for m in metrics:
        fonte = f'<div class="metrica-fonte">Fonte: {e(m["fonte"])}</div>' if m.get("fonte") else ""
        items += f'<div class="metrica"><div class="metrica-num">{e(m.get("numero",""))}</div><div class="metrica-titulo">{e(m.get("titulo",""))}</div><div class="metrica-desc">{e(m.get("descricao",""))}</div>{fonte}</div>'
    return f"""
<div class="slide slide-metricas">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo"><div class="grid-metricas cols-{cols}">{items}</div></div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_hub(d, n, total, logo_b64, branding_label):
    """
    Diagrama radial. Espera:
      hub_centro: {titulo, subtitulo}
      satelites: [{nome, descricao, icone_path, posicao: {top,left,transform}}]
    """
    titulo   = d.get("titulo", "")
    centro   = d.get("hub_centro", {})
    sats     = d.get("satelites", [])

    centro_html = f"""
    <div class="hub-centro">
      <span class="hub-centro-titulo">{e(centro.get("titulo",""))}</span>
      {"<span class='hub-centro-sub'>" + e(centro.get("subtitulo","")) + "</span>" if centro.get("subtitulo") else ""}
    </div>"""

    # Posições padrão para até 6 satélites (top/left em %)
    pos_default = [
        {"top": "15%",  "left": "12%",  "transform": "none"},          # topo esq
        {"top": "15%",  "left": "62%",  "transform": "none"},          # topo dir
        {"top": "45%",  "left": "2%",   "transform": "translateY(-50%)"},  # meio esq
        {"top": "45%",  "left": "74%",  "transform": "translateY(-50%)"},  # meio dir
        {"top": "72%",  "left": "12%",  "transform": "none"},          # base esq
        {"top": "72%",  "left": "62%",  "transform": "none"},          # base dir
    ]

    # Linhas SVG conectoras (do centro para cada satélite)
    # Calculamos ponto central de cada satélite (aproximado)
    cx, cy = 50, 50  # centro em %
    sat_centros = [
        (20, 22), (76, 22),
        (12, 50), (84, 50),
        (20, 78), (76, 78),
    ]

    linhas_svg = ""
    cores_linha = [
        "var(--accent-orange)",
        "color-mix(in srgb, var(--accent-orange) 50%, var(--accent) 50%)",
        "var(--accent)",
        "color-mix(in srgb, var(--accent) 50%, var(--accent2) 50%)",
        "var(--accent2)",
        "color-mix(in srgb, var(--accent2) 70%, #000 30%)",
    ]

    for i, (sx, sy) in enumerate(sat_centros[:len(sats)]):
        cor = cores_linha[i % len(cores_linha)]
        linhas_svg += f'<line x1="{cx}%" y1="{cy}%" x2="{sx}%" y2="{sy}%" stroke="{cor}" stroke-width="1.5" stroke-opacity="0.5"/>'

    sats_html = ""
    for i, sat in enumerate(sats):
        pos  = sat.get("posicao", pos_default[i % len(pos_default)])
        ic   = _asset_b64(sat.get("icone_path"))
        ic_h = f'<img src="{ic}" alt="">' if ic else ""
        sats_html += f"""
        <div class="satelite" style="top:{pos['top']};left:{pos['left']};transform:{pos['transform']};">
          <div class="sat-icone">{ic_h}</div>
          <div class="sat-info">
            <span class="sat-nome">{e(sat.get("nome",""))}</span>
            <span class="sat-desc">{e(sat.get("descricao",""))}</span>
          </div>
        </div>"""

    return f"""
<div class="slide slide-hub">
  <div class="topo"><span class="eyebrow">{e(d.get("eyebrow",""))}</span><h2>{e(titulo)}</h2></div>
  {_branding(logo_b64, branding_label)}
  <div class="canvas">
    <svg class="hub-linhas" viewBox="0 0 100 100" preserveAspectRatio="none">{linhas_svg}</svg>
    {centro_html}
    {sats_html}
  </div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_split(d, n, total, logo_b64, branding_label):
    """
    Dois painéis lado a lado.
    Espera:
      titulo, eyebrow
      esquerda: {tipo: 'codigo'|'imagem', label, conteudo, destaque: {icone_path, texto}}
      direita: [{titulo, descricao, icone_path}]
    """
    titulo  = d.get("titulo", "")
    eyebrow = d.get("eyebrow", "")
    esq     = d.get("esquerda", {})
    dir_    = d.get("direita", [])

    # Painel esquerdo
    label_esq = e(esq.get("label", ""))
    label_h   = f'<span class="label-contexto">{label_esq}</span>' if label_esq else ""

    if esq.get("tipo") == "codigo":
        conteudo_esq = f'<div class="bloco-codigo">{e(esq.get("conteudo",""))}</div>'
    else:
        ic = _asset_b64(esq.get("imagem_path"))
        conteudo_esq = f'<img src="{ic}" style="width:100%;border-radius:8px;" alt="">' if ic else ""

    dest = esq.get("destaque")
    dest_h = ""
    if dest:
        ic_d  = _asset_b64(dest.get("icone_path"))
        ic_dh = f'<div class="icone-badge"><img src="{ic_d}" alt=""></div>' if ic_d else ""
        dest_h = f'<div class="card-destaque">{ic_dh}<p class="card-destaque-txt">{e(dest.get("texto",""))}</p></div>'

    # Painel direito
    items_dir = ""
    for item in dir_:
        ic   = _asset_b64(item.get("icone_path"))
        ic_h = f'<div class="split-icone"><img src="{ic}" alt=""></div>' if ic else '<div class="split-icone"></div>'
        items_dir += f"""
        <div class="split-item">
          {ic_h}
          <div class="split-texto">
            <span class="split-titulo">{e(item.get("titulo",""))}</span>
            <span class="split-desc">{e(item.get("descricao",""))}</span>
          </div>
        </div>"""

    eyebrow_h = f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else ""

    return f"""
<div class="slide slide-split">
  <div class="header-dark">{eyebrow_h}<h2>{e(titulo)}</h2></div>
  {_branding(logo_b64, branding_label)}
  <div class="corpo">
    <div class="lado-esq">
      {label_h}
      {conteudo_esq}
      {dest_h}
    </div>
    <div class="lado-dir">{items_dir}</div>
  </div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_pipeline(d, n, total, logo_b64, branding_label):
    """
    Fluxo em diagrama com legenda numerada.
    Espera:
      titulo, eyebrow
      nos: [{label, subtitulo}]     — nós do diagrama
      setas: [{numero, label}]      — setas numeradas entre nós
      legenda: [{numero, texto}]    — rodapé
    """
    titulo  = d.get("titulo", "")
    nos     = d.get("nos", [])
    setas   = d.get("setas", [])
    legenda = d.get("legenda", [])

    cores_num = [
        "var(--accent-orange)",
        "color-mix(in srgb, var(--accent-orange) 50%, var(--accent) 50%)",
        "var(--accent)",
        "color-mix(in srgb, var(--accent) 50%, var(--accent2) 50%)",
        "var(--accent2)",
        "color-mix(in srgb, var(--accent2) 70%, #000 30%)",
    ]

    # Monta linha de nós intercalados com setas
    pipe_row = ""
    seta_idx = 0
    for i, no in enumerate(nos):
        sub_h = f'<div style="font-size:11px;color:var(--texto-secundario);text-align:center;margin-top:3px;">{e(no.get("subtitulo",""))}</div>' if no.get("subtitulo") else ""
        pipe_row += f'<div class="pipe-node"><div class="pipe-box">{e(no.get("label",""))}{sub_h}</div></div>'
        if i < len(nos) - 1:
            seta = setas[seta_idx] if seta_idx < len(setas) else {}
            cor  = cores_num[seta_idx % len(cores_num)]
            num_h = f'<div class="pipe-num" style="background:{cor};">{seta.get("numero","→")}</div>' if seta.get("numero") else ""
            lbl_h = f'<div class="pipe-label">{e(seta.get("label",""))}</div>' if seta.get("label") else ""
            pipe_row += f'<div class="pipe-arrow">{num_h}<div class="pipe-line"></div>{lbl_h}</div>'
            seta_idx += 1

    leg_items = ""
    for i, leg in enumerate(legenda):
        cor = cores_num[i % len(cores_num)]
        leg_items += f'<div class="leg-item"><div class="leg-num" style="background:{cor};">{e(str(leg.get("numero","●")))}</div><span class="leg-txt">{e(leg.get("texto",""))}</span></div>'

    return f"""
<div class="slide slide-pipeline">
  <div class="topo"><h2>{e(titulo)}</h2></div>
  {_branding(logo_b64, branding_label)}
  <div class="area-diagrama">
    <div class="diagrama-box">
      <div class="pipe-row">{pipe_row}</div>
    </div>
  </div>
  <div class="legenda">{leg_items}</div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_diagrama(d, n, total, logo_b64, branding_label):
    titulo    = d.get("titulo", "")
    ic        = _asset_b64(d.get("icone_path"))
    label     = e(d.get("icone_label", ""))
    sem_icone = "sem-icone" if not ic else ""
    icone_h   = f'<div class="icone-hero"><div class="icone-bg"><img src="{ic}" alt="{label}"></div>{"<span class=icone-label>" + label + "</span>" if label else ""}</div>' if ic else ""
    topicos   = "".join(f'<div class="topico">› {e(i)}</div>' for i in d.get("conteudo", []))
    return f"""
<div class="slide slide-diagrama">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo {sem_icone}">{icone_h}<div class="topicos">{topicos}</div></div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_comparacao(d, n, total, logo_b64, branding_label):
    titulo  = d.get("titulo", "")
    itens   = d.get("conteudo", [])
    l_esq   = e(d.get("coluna_esquerda", "Antes"))
    l_dir   = e(d.get("coluna_direita",  "Depois"))
    esq_h   = "".join(f'<div class="comp-item">{e(itens[i])}</div>' for i in range(0, len(itens), 2))
    dir_h   = "".join(f'<div class="comp-item">{e(itens[i])}</div>' for i in range(1, len(itens), 2))
    return f"""
<div class="slide slide-comparacao">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo">
    <div class="coluna coluna-esq"><span class="col-label">{l_esq}</span>{esq_h}</div>
    <div class="divisor-v"></div>
    <div class="coluna coluna-dir"><span class="col-label">{l_dir}</span>{dir_h}</div>
  </div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_agenda(d, n, total, logo_b64, branding_label):
    titulo = d.get("titulo", "")
    rows   = "".join(f'<div class="linha-agenda"><div class="etapa-badge">{e(l.get("etapa",""))}</div><div class="descricao">{e(l.get("descricao",""))}</div></div>' for l in d.get("agenda", []))
    return f"""
<div class="slide slide-agenda">
  {_header_dark(titulo)}
  {_branding(logo_b64, branding_label)}
  <div class="corpo">{rows}</div>
  {_linha_base()}
  {_num(n, total)}
</div>"""


def html_encerramento(d, n, total, logo_b64, branding_label):
    titulo = e(d.get("titulo", "Obrigado!"))
    frase  = e((d.get("conteudo") or [""])[0])
    return f"""
<div class="slide slide-encerramento">
  {_branding(logo_b64, branding_label, claro=True)}
  <div class="corpo">
    <h1>{titulo}</h1>
    <div class="linha-dec"></div>
    {"<p class='frase'>" + frase + "</p>" if frase else ""}
  </div>
  {_num(n, total)}
</div>"""


CONSTRUTORES = {
    "capa":         html_capa,
    "titulo":       html_titulo,
    "bullets":      html_bullets,
    "cards":        html_cards,
    "fluxo":        html_fluxo,
    "metricas":     html_metricas,
    "hub":          html_hub,
    "split":        html_split,
    "pipeline":     html_pipeline,
    "diagrama":     html_diagrama,
    "comparacao":   html_comparacao,
    "agenda":       html_agenda,
    "encerramento": html_encerramento,
}


# ---------------------------------------------------------------------------
# Montagem HTML
# ---------------------------------------------------------------------------

def montar_html(dados: dict, tema: dict, n: int, total: int,
                logo_b64: str | None, branding: str, nome_template: str) -> str:
    tipo       = dados.get("tipo", "bullets").lower()
    construtor = CONSTRUTORES.get(tipo, html_bullets)
    conteudo   = construtor(dados, n, total, logo_b64, branding)

    tpl = template_path(nome_template)
    html = tpl.read_text(encoding="utf-8")

    subs = {
        "{{ FUNDO_ESCURO }}":     tema["fundo_escuro"],
        "{{ FUNDO_CLARO }}":      tema["fundo_claro"],
        "{{ SURFACE_CARD }}":     tema["surface_card"],
        "{{ BORDER_CARD }}":      tema["border_card"],
        "{{ TEXTO_PRIMARIO }}":   tema["texto_primario"],
        "{{ TEXTO_SECUNDARIO }}": tema["texto_secundario"],
        "{{ TEXTO_CLARO }}":      tema["texto_claro"],
        "{{ ACCENT }}":           tema["accent"],
        "{{ ACCENT2 }}":          tema["accent2"],
        "{{ ACCENT_ORANGE }}":    tema["accent_orange"],
        "{{ BADGE_BG }}":         tema["badge_bg"],
        "{{ BADGE_TEXT }}":       tema["badge_text"],
        "{{ FONTE_TITULO }}":     tema["fonte_titulo"],
        "{{ FONTE_CORPO }}":      tema["fonte_corpo"],
        "{{ PADDING_SLIDE }}":    tema["padding_slide"],
        "{{ BORDER_RADIUS }}":    tema["border_radius"],
        "{{ BORDER_RADIUS_LG }}": tema["border_radius_lg"],
        "{{ CONTEUDO_SLIDE }}":   conteudo,
    }

    for k, v in subs.items():
        html = html.replace(k, v)
    return html


# ---------------------------------------------------------------------------
# Geração Playwright
# ---------------------------------------------------------------------------

def gerar_slide(
    dados_slide: dict,
    caminho_saida: str,
    nome_tema: str = TEMA_PADRAO,
    numero: int = 1,
    total: int = 1,
    branding: str = "SENAI",
    logo_b64: str | None = None,
    nome_template: str = TEMPLATE_PADRAO,
) -> None:
    from playwright.sync_api import sync_playwright

    tema       = obter_tema(nome_tema)
    html_final = montar_html(dados_slide, tema, numero, total,
                             logo_b64, branding, nome_template)

    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page    = browser.new_page(viewport={"width": 1280, "height": 720})
        page.set_content(html_final, wait_until="networkidle")
        page.screenshot(
            path=caminho_saida,
            clip={"x": 0, "y": 0, "width": 1280, "height": 720},
        )
        browser.close()
