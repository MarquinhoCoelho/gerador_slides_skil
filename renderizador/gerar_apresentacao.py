"""
gerar_apresentacao.py
Orquestrador: lê um roteiro.json e gera todos os slides PNG com Playwright.

Uso:
    python renderizador/gerar_apresentacao.py saida/slides/<tema>/roteiro.json

Campos globais do roteiro.json:
  tema        — slug identificador
  template    — nome do template visual (padrão: 'padrao')
  tema_visual — nome do tema de cores em tokens.json (padrão: 'senai-tech-light')
  branding    — texto no canto superior direito
  logo_path   — caminho relativo para PNG/SVG da logo (opcional)
"""

import json
import os
import sys
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gerar_slide import gerar_slide, TEMA_PADRAO, TEMPLATE_PADRAO, _asset_b64

TIPOS_VALIDOS = {
    "capa", "titulo", "bullets", "cards",
    "fluxo", "metricas", "hub", "split", "pipeline",
    "diagrama", "comparacao", "agenda", "encerramento",
}


def validar_roteiro(roteiro: dict) -> list[str]:
    erros = []
    if "tema" not in roteiro:
        erros.append("Campo 'tema' ausente.")
    slides = roteiro.get("slides")
    if not isinstance(slides, list) or len(slides) == 0:
        erros.append("Campo 'slides' ausente, não é lista ou está vazio.")
        return erros
    for i, s in enumerate(slides, 1):
        tipo = s.get("tipo", "")
        if not tipo:
            erros.append(f"Slide {i}: 'tipo' ausente.")
        elif tipo.lower() not in TIPOS_VALIDOS:
            erros.append(f"Slide {i}: tipo '{tipo}' inválido. Use: {', '.join(sorted(TIPOS_VALIDOS))}")
        if "titulo" not in s:
            erros.append(f"Slide {i}: 'titulo' ausente.")
    return erros


def gerar_apresentacao(caminho_roteiro: str) -> None:
    caminho_roteiro = Path(caminho_roteiro)
    if not caminho_roteiro.exists():
        print(f"❌ Arquivo não encontrado: {caminho_roteiro}")
        sys.exit(1)

    try:
        roteiro = json.loads(caminho_roteiro.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        print(f"❌ JSON inválido: {ex}")
        sys.exit(1)

    erros = validar_roteiro(roteiro)
    if erros:
        print("❌ Roteiro inválido:")
        for er in erros:
            print(f"   • {er}")
        sys.exit(1)

    # Config global
    tema_visual    = roteiro.get("tema_visual", roteiro.get("template", TEMA_PADRAO))
    nome_template  = roteiro.get("nome_template", TEMPLATE_PADRAO)
    branding       = roteiro.get("branding", "SENAI")
    logo_path      = roteiro.get("logo_path")
    pasta_saida    = caminho_roteiro.parent
    slides         = roteiro["slides"]
    total          = len(slides)

    # Resolve logo uma vez para todos os slides
    logo_b64 = _asset_b64(logo_path) if logo_path else None
    if logo_path and not logo_b64:
        print(f"  ⚠ Logo não encontrada: {logo_path} — usando texto")

    print(f"\n[SLIDES] Gerando apresentacao: {roteiro['tema']}")
    print(f"   Template  : {nome_template}")
    print(f"   Cores     : {tema_visual}")
    print(f"   Branding  : {branding}")
    print(f"   Logo      : {'OK' if logo_b64 else 'sem logo (usando texto)'}")
    print(f"   Slides    : {total}")
    print(f"   Destino   : {pasta_saida}\n")

    os.makedirs(pasta_saida, exist_ok=True)
    gerados, falhas = 0, []

    for slide in slides:
        numero       = slide.get("numero", gerados + 1)
        nome_arquivo = f"slide-{numero:02d}.png"
        caminho_png  = str(pasta_saida / nome_arquivo)

        tema_slide    = slide.get("tema_visual",   tema_visual)
        template_slide= slide.get("nome_template", nome_template)

        dados = {
            "tipo":            slide.get("tipo", "bullets"),
            "eyebrow":         slide.get("eyebrow", ""),
            "titulo":          slide.get("titulo", ""),
            "conteudo":        slide.get("conteudo", []),
            "cards":           slide.get("cards", []),
            "agenda":          slide.get("agenda", []),
            "etapas":          slide.get("etapas", []),
            "metricas":        slide.get("metricas", []),
            "hub_centro":      slide.get("hub_centro", {}),
            "satelites":       slide.get("satelites", []),
            "esquerda":        slide.get("esquerda", {}),
            "direita":         slide.get("direita", []),
            "nos":             slide.get("nos", []),
            "setas":           slide.get("setas", []),
            "legenda":         slide.get("legenda", []),
            "icone_path":      slide.get("icone_path"),
            "icone_label":     slide.get("icone_label", ""),
            "coluna_esquerda": slide.get("coluna_esquerda", "Antes"),
            "coluna_direita":  slide.get("coluna_direita", "Depois"),
        }

        try:
            gerar_slide(
                dados, caminho_png,
                nome_tema=tema_slide,
                numero=numero, total=total,
                branding=branding,
                logo_b64=logo_b64,
                nome_template=template_slide,
            )
            titulo_d = dados["titulo"][:48] + "…" if len(dados["titulo"]) > 48 else dados["titulo"]
            print(f"  [{numero:02d}/{total:02d}] OK {nome_arquivo}  -  {titulo_d}")
            gerados += 1
        except Exception as ex:
            msg = f"  [{numero:02d}/{total:02d}] ✗ {nome_arquivo}  —  ERRO: {ex}"
            print(msg)
            falhas.append(msg)

    print(f"\n{'='*62}")
    if falhas:
        print(f"AVISOS: {gerados}/{total} slides gerados com erros:")
        for f in falhas:
            print(f"   {f}")
    else:
        print(f"CONCLUIDO: {gerados} slides em:")
        print(f"   {pasta_saida}")
    print(f"{'='*62}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python renderizador/gerar_apresentacao.py <roteiro.json>")
        sys.exit(1)
    gerar_apresentacao(sys.argv[1])
