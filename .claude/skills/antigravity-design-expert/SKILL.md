---
name: antigravity-design-expert
description: Direção visual "Antigravity" (glassmorphism, profundidade espacial, elementos flutuantes, animações suaves com GSAP/CSS 3D) para interfaces interativas. Use quando o usuário pedir para deixar o dashboard mais moderno/imersivo, com efeito de vidro, cards flutuantes, animações de entrada ou visual 3D — inclusive no dashboard Streamlit deste projeto.
---

# Antigravity UI & Motion Design Expert

Você é um engenheiro de UI/UX especializado em "Antigravity Design": interfaces espaciais, leves e interativas, com grids isométricos, elementos flutuantes, glassmorphism e animações suaves.

## Quando usar
- Pedidos de interface com profundidade espacial, vidro (glassmorphism) e muito movimento.
- Dashboards, landing pages ou superfícies imersivas, em vez de uma UI plana convencional.
- Não use para mudanças de dados/métricas (isso vai em `src/data.py`) nem quando o usuário pedir um visual simples.

## Stack neste projeto (Streamlit)
O projeto é **Python + Streamlit + Plotly**, não React. Adapte a direção visual assim:

- **CSS global:** injete um bloco `<style>` via `st.markdown(css, unsafe_allow_html=True)`. Prefira guardar o CSS em um arquivo (ex.: `assets/antigravity.css`) e lê-lo no `app.py`, em vez de strings gigantes inline.
- **Tema base:** cores, fonte e fundo em `.streamlit/config.toml` (`[theme]`); o CSS refina por cima.
- **Componentes animados (GSAP, 3D CSS):** use `streamlit.components.v1.html(...)`, que roda num iframe isolado. Carregue GSAP de um CDN com versão fixa (ex.: `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`). Scripts injetados via `st.markdown` **não executam**.
- **KPIs como cards de vidro:** estilize `[data-testid="stMetric"]` (ou renderize cards em HTML) com translucidez e blur.
- **Gráficos Plotly:** `paper_bgcolor`/`plot_bgcolor` transparentes (`rgba(0,0,0,0)`) para que o vidro do container apareça; animações via `transition` do Plotly.
- Seletores `data-testid` do Streamlit podem mudar entre versões — verifique no browser pane (configuração `dashboard` em `.claude/launch.json`) antes de confiar neles.
- Fora deste projeto (React/Next.js), o padrão original vale: Tailwind + CSS 3D, GSAP + ScrollTrigger, React Three Fiber.

## Paleta Vingadores
Cores originais inspiradas no tema (sem logos, marcas ou artes oficiais). Fundo escuro profundo, acentos em vermelho, dourado e azul.

| Token | Valor | Uso |
|---|---|---|
| `--av-bg` | `#0B0F1A` | Fundo da página (espaço profundo) |
| `--av-bg-2` | `#131A2B` | Sidebar, fundo secundário |
| `--av-red` | `#E23D3D` | Acento principal, série 1, destaques e alertas (mortes) |
| `--av-gold` | `#F2B33D` | Valores de KPI, série 2, hover e foco |
| `--av-blue` | `#3D8BFF` | Série 3, links e estado ativo |
| `--av-teal` | `#2EC4B6` | Série 4, retornos e sinais positivos |
| `--av-violet` | `#9B6BFF` | Série 5, categorias extras |
| `--av-glass` | `rgba(255,255,255,0.06)` | Fundo de cards de vidro |
| `--av-glass-strong` | `rgba(255,255,255,0.10)` | Card em hover ou destaque |
| `--av-border` | `rgba(255,255,255,0.14)` | Bordas dos cards e divisores |
| `--av-grid` | `rgba(255,255,255,0.08)` | Grade dos gráficos |
| `--av-text` | `#F3F5FA` | Texto principal e números |
| `--av-text-muted` | `#A9B2C7` | Rótulos, eixos e legendas |

**Contraste** (sobre `--av-bg`): `--av-text` ≈ 17:1, `--av-text-muted` ≈ 9:1, `--av-gold` ≈ 10:1, `--av-blue` ≈ 5.8:1, `--av-teal` ≈ 8.8:1, `--av-red` ≈ 4.5:1 (limite AA). Use o vermelho em barras, ícones e textos grandes, não em textos pequenos. Números de KPI ficam em `--av-text` ou `--av-gold`. Sobre o vidro, o contraste cai pouco porque o vidro é quase transparente; não use vidro com opacidade acima de `0.15` atrás de texto escuro.

**`.streamlit/config.toml`** (mescle com o que já existe, sem apagar a telemetria desligada):
```toml
[theme]
base = "dark"
primaryColor = "#E23D3D"
backgroundColor = "#0B0F1A"
secondaryBackgroundColor = "#131A2B"
textColor = "#F3F5FA"
```

**Variáveis CSS** (no topo de `assets/antigravity.css`):
```css
:root {
  --av-bg: #0B0F1A;  --av-bg-2: #131A2B;
  --av-red: #E23D3D; --av-gold: #F2B33D; --av-blue: #3D8BFF;
  --av-teal: #2EC4B6; --av-violet: #9B6BFF;
  --av-glass: rgba(255,255,255,0.06); --av-glass-strong: rgba(255,255,255,0.10);
  --av-border: rgba(255,255,255,0.14); --av-grid: rgba(255,255,255,0.08);
  --av-text: #F3F5FA; --av-text-muted: #A9B2C7;
}
[data-testid="stMetric"] {
  background: var(--av-glass); border: 1px solid var(--av-border);
  backdrop-filter: blur(12px); border-radius: 16px;
}
[data-testid="stMetricValue"] { color: var(--av-gold); }
[data-testid="stMetricLabel"] { color: var(--av-text-muted); }
```

**Plotly** (um template único, registrado uma vez no app):
```python
import plotly.graph_objects as go
import plotly.io as pio

AV_COLORWAY = ["#E23D3D", "#F2B33D", "#3D8BFF", "#2EC4B6", "#9B6BFF", "#A9B2C7"]
pio.templates["vingadores"] = go.layout.Template(layout=dict(
    colorway=AV_COLORWAY,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F3F5FA"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#A9B2C7")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#A9B2C7")),
))
pio.templates.default = "plotly_dark+vingadores"
```
Para categorias fixas, mantenha a mesma cor em todos os gráficos (ex.: ativo = `--av-teal`, inativo = `--av-text-muted`; mortes = `--av-red`, retornos = `--av-teal`).

## Princípios de design
- **Leveza:** elementos parecem flutuar; sombras suaves e difusas em camadas (ex.: `box-shadow: 0 20px 40px rgba(0,0,0,0.05)`).
- **Profundidade espacial:** camadas no eixo Z; fundo profundo, primeiro plano saltando com `perspective`.
- **Glassmorphism:** translucidez sutil, `backdrop-filter: blur(12px)` e bordas semitransparentes.
- **Isometria (com moderação):** em grids de cards, inclinações 3D (ex.: `transform: rotateX(60deg) rotateZ(-45deg)`) — só em elementos decorativos; dados e tabelas precisam continuar legíveis.

## Regras de movimento
- **Nada muda de forma brusca:** hover/focus/active com transição de no mínimo `0.3s ease-out`.
- **Entradas escalonadas:** cards de uma grade entram em sequência, com `0.1s` de atraso entre eles (CSS `animation-delay` ou `gsap.from(..., {stagger: 0.1})`).
- **Scroll e parallax:** ScrollTrigger/parallax só funcionam dentro de um `components.html` com altura própria; a página Streamlit em si re-renderiza a cada interação, então não dependa de scroll hijacking nela.

## Restrições de execução
- Código modular e reutilizável (ex.: uma função `inject_styles()` e helpers para cards).
- Desligue todas as animações com `@media (prefers-reduced-motion: reduce)`.
- Performance: `will-change: transform` em elementos animados; não anime continuamente `box-shadow` nem `filter`.
- Mantenha contraste e legibilidade dos números (KPIs, eixos, tabela) acima do efeito visual.

## Limitações
- Valide no browser pane depois de mudar o visual; isto não substitui testes nem revisão.
- Se faltarem requisitos (paleta, nível de animação, o que pode mudar), pergunte antes.
