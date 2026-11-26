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
