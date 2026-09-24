# 🎨 Guia de Padrão Visual e Tokens para Slides (Kiro Design System)

Este documento define os parâmetros visuais, regras de layout, tokens de design e formatos estruturais para a criação automatizada de apresentações de alto impacto pelo **Kiro**.

---

## 1. Visão Geral e Diretrizes Estéticas

- **Estilo Predominante**: Minimalista Premium / Tech Moderno.
- **Princípios de Design**:
  - **Clareza em Primeiro Lugar**: Menos texto por slide, maior hierarquia.
  - **Espaço Branco Ativo**: O respiro visual é tão importante quanto o conteúdo.
  - **Alto Contraste**: Garantia de legibilidade perfeita em qualquer tela ou projetor.
  - **Consistência Modular**: Blocos de conteúdo alinhados rigorosamente à grade.

---

## 2. Tokens de Design (Design Tokens)

### 2.1. Paleta de Cores

#### Tema Escuro (Padrão - Premium Tech)
- `color.bg.primary`: `#0D0F12` (Preto Slate Profundo)
- `color.bg.secondary`: `#16191E` (Cinza Escuro de Contraste / Cards)
- `color.bg.tertiary`: `#22272E` (Bordas e Elementos Desativados)
- `color.text.primary`: `#F0F6FC` (Branco Suave)
- `color.text.secondary`: `#8B949E` (Cinza Médio de Leitura)
- `color.accent.primary`: `#6366F1` (Roxo elétrico / Indigo)
- `color.accent.secondary`: `#06B6D4` (Ciano de Destaque)
- `color.accent.highlight`: `#F59E0B` (Âmbar para Alertas/KPIs)

#### Tema Claro (Opção Alternativa - Executive Clean)
- `color.bg.primary`: `#F8FAFC` (Off-white Limpo)
- `color.bg.secondary`: `#FFFFFF` (Branco Puro / Cards)
- `color.bg.tertiary`: `#E2E8F0` (Bordas e Divisores)
- `color.text.primary`: `#0F172A` (Azul Escuro Quase Preto)
- `color.text.secondary`: `#475569` (Cinza Grafite)
- `color.accent.primary`: `#2563EB` (Azul Corporativo Vibrante)
- `color.accent.secondary`: `#0D9488` (Verde Teal)
- `color.accent.highlight`: `#D97706` (Laranja Quente)

---

### 2.2. Tipografia

- **Fonte de Títulos (Headings)**: `Inter`, `Plus Jakarta Sans` ou `Outfit` (Sans-Serif, Peso 700/800, tracking levemente fechado `-0.02em`).
- **Fonte de Corpo (Body/Captions)**: `Inter` ou `Roboto` (Sans-Serif, Peso 400/500, line-height `1.5`).
- **Fonte Mono (Código/Métricas)**: `JetBrains Mono` ou `Fira Code`.

#### Escala Tipográfica (Tamanhos Relativos baseados em Widescreen 1920x1080)
- `font.size.display`: `72px` (Títulos Principais de Capa)
- `font.size.h1`: `48px` (Títulos de Slides)
- `font.size.h2`: `32px` (Subtítulos / Destaques)
- `font.size.body`: `20px` (Texto de Leitura Principal)
- `font.size.caption`: `14px` (Notas de Rodapé e Metadados)
- `font.size.kpi`: `96px` (Números de Big Data / Métricas)

---

### 2.3. Espaçamentos e Grid

- **Margens de Borda (Safe Zone)**:
  - `margin.horizontal`: `80px`
  - `margin.vertical`: `60px`
- **Grid de Colunas**: Sistema flexível de 12 colunas com `gutter` de `24px`.
- **Raio de Borda (Border Radius)**:
  - `radius.card`: `16px`
  - `radius.button`: `8px`
  - `radius.badge`: `999px` (Pill format)

---

## 3. Formatos de Proporção de Slide (Aspect Ratios)

O Kiro deve ajustar layouts e escalas conforme o formato especificado no prompt:

### 3.1. Proporção 16:9 (Apresentação Padrão Widescreen)
- **Dimensão Base**: `1920px x 1080px`
- **Uso**: Apresentações executivas, palestras, pitching, reuniões Zoom/Meet.
- **Diretriz**: Foco no fluxo horizontal. Disposição de 2 a 4 colunas lógicas.

### 3.2. Proporção 9:16 (Vertical / Stories / Mobile)
- **Dimensão Base**: `1080px x 1920px`
- **Uso**: Consumo no celular, Reels, TikTok, PDFs verticais.
- **Diretriz**: Fluxo estritamente vertical. Empilhamento simples (Single Column Stack). Margens superiores e inferiores ampliadas para evitar botões de UI de redes sociais.

### 3.3. Proporção 1:1 (Quadrado / Carrossel)
- **Dimensão Base**: `1080px x 1080px`
- **Uso**: LinkedIn, Instagram Carousel.
- **Diretriz**: Conteúdo ultra-sintético. Títulos grandes, poucas linhas de texto por slide, foco em 1 ideia central por tela.

### 3.4. Proporção 4:3 (Impresso / Relatórios Tradicionais)
- **Dimensão Base**: `1440px x 1080px`
- **Uso**: Relatórios para impressão e leitura direta em PDF.
- **Diretriz**: Densidade de texto ligeiramente maior, similar a uma folha A4 horizontal.

---

## 4. Biblioteca de Layouts e Templates

O Kiro deve escolher um destes modelos conforme o objetivo do slide:

### Layout 1: Capa (Title Slide)
- **Elementos**: Badge de Categoria (opcional) + Título Principal (Display) + Subtítulo + Autor/Data.
- **Alinhamento**: Esquerda ou Centralizado com foco em grande espaço negativo.

### Layout 2: Seção / Transição (Divider Slide)
- **Elementos**: Número do Capítulo (`01`, `02`, `03`) em tamanho KPI gigantesco (opacidade 20%) + Título da Seção.
- **Uso**: Mudança de assunto na apresentação.

### Layout 3: Conteúdo em Colunas (2 ou 3 Colunas)
- **Elementos**: Título no topo + 2 ou 3 Cards contendo Ícone/Número, Subtítulo e Descrição.
- **Uso**: Comparações, pilares, etapas não sequenciais.

### Layout 4: Métrica / KPI em Destaque (Big Stat)
- **Elementos**: Número de Grande Impacto (ex: `+240%`, `$1.2M`) + Rótulo Explicativo + Pequeno parágrafo contextual.
- **Uso**: Mostrar resultados, dados financeiros e métricas de crescimento.

### Layout 5: Citação ou Depoimento (Quote Slide)
- **Elementos**: Aspas estilizadas em cor de destaque + Texto em itálico/destaque (`32px`) + Nome do Autor e Cargo.

### Layout 6: Imagem + Texto (Split Screen 50/50)
- **Elementos**: Lado Esquerdo (Texto, título e bullet points) | Lado Direito (Imagem com bordas arredondadas ou mockups).

### Layout 7: Timeline / Processo (Step-by-Step)
- **Elementos**: Linha horizontal ou vertical conectando 3 a 5 pontos numerados de progresso.

---

## 5. Regras Globais para Geração pelo Kiro (Instruções para o Modelo)

Ao gerar qualquer slide usando esta especificação, o Kiro **deve cumprir rigorosamente**:

1. **Regra dos 3 PONTOS**: Nunca inclua mais de 3 a 4 blocos de informação principal por slide. Se houver mais dados, subdivida em um novo slide.
2. **Contraste Mínimo**: Garanta que a cor do texto e do fundo cumpram o padrão WCAG AA de acessibilidade.
3. **Hierarquia Visual**:
   - Nível 1: Título do Slide (Capta a atenção imediata).
   - Nível 2: Destaques/Subtítulos/Números.
   - Nível 3: Descrição e rodapé (Apenas para apoio).
4. **Respiro**: O conteúdo nunca deve encostar nos limites da tela. Mantenha as margens de segurança ativas.
5. **Estilo de Ícones**: Usar ícones estilo "Feather Icons" ou "Lucide Icons", sempre com traço fino (lineart) e na cor de destaque (`color.accent.primary`).