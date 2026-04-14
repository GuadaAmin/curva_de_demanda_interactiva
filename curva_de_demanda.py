import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Curva de Demanda", layout="centered")
st.title("Curva de Demanda Interactiva")
st.markdown("Herramienta de exploración sobre los conceptos de **movimiento a lo largo de la curva**, **desplazamientos** y **cambios en la sensibilidad al precio**.")
st.markdown("Por: Abregú Candela, Amin Guadalupe, y Luciana Pasteris.")
st.markdown("Economía 2026")

# Función auxiliar para graficar la curva de demanda (forma estándar)
def graficar_demanda(intercepto, pendiente, Q_max=700, punto=None, titulo="", referencia=None):
    """
    referencia: tupla (intercepto_ref, pendiente_ref) para mostrar curva original como referencia
    """
    Q = np.linspace(0, Q_max, 200)
    P = intercepto - pendiente * Q
    P = np.maximum(P, 0)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Curva actual (sólida)
    ax.plot(Q, P, 'b-', linewidth=2, label='Curva actual')
    
    # Curva de referencia (discontinua) si se proporciona
    if referencia:
        inter_ref, pend_ref = referencia
        P_ref = inter_ref - pend_ref * Q
        P_ref = np.maximum(P_ref, 0)
        ax.plot(Q, P_ref, 'r--', linewidth=1.5, alpha=0.7, label='Curva original (referencia)')
    
    if punto:
        q, p = punto
        ax.plot(q, p, 'ro', markersize=8)
        ax.annotate(f'({q:.1f}, {p:.1f})', (q, p), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)
    
    ax.set_xlim(0, 700)   # escala fija
    ax.set_ylim(0, 35)   # escala fija
    ax.set_xlabel("Cantidad demandada (Q)")
    ax.set_ylabel("Precio (P)")
    ax.set_title(titulo)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    return fig

# PESTAÑA 1: Movimiento a lo largo de la misma curva D1 (con deslizador)
tab1, tab2, tab3= st.tabs(["📌 Movimiento sobre D1", "↔️ Cambio en ordenada al origen", "📐 Cambio en pendiente"])

with tab1:
    st.header("Movimiento a lo largo de una misma curva de demanda")
    st.markdown("**Desliza el punto sobre la curva** para ver cómo varía la cantidad demandada al cambiar el precio.")
    
    intercepto_fijo = 30.0
    pendiente_fija = 0.05
    Q_max = 700
    
    cantidad_punto = st.slider("Cantidad demandada (punto móvil)", min_value=0.0, max_value=600.0, value=300.0, step=0.5, key="punto_movil")
    precio_punto = intercepto_fijo - pendiente_fija * cantidad_punto
    precio_punto = max(precio_punto, 0)
    
    fig1 = graficar_demanda(intercepto_fijo, pendiente_fija, Q_max=Q_max,
                            punto=(cantidad_punto, precio_punto),
                            titulo=f"Punto sobre D₁: Q = {cantidad_punto:.1f}, P = {precio_punto:.1f}")
    st.pyplot(fig1)
    
    st.markdown("**Fundamento económico:** Un movimiento a lo largo de la curva de demanda se origina exclusivamente por una variación en el precio del bien, manteniéndose constantes los demás factores (ingresos, gustos, precios de sustitutos). Conforme la ley de la demanda establece, un aumento del precio reduce la cantidad demandada, y una disminución la incrementa, desplazando el punto de equilibrio sobre la misma curva.")

# PESTAÑA 2: Cambio continuo en la ordenada al origen (intercepto) 
with tab2:
    st.header("Impacto de cambios en la ordenada al origen (intercepto)")
    st.markdown("Ajusta el **precio máximo** que los consumidores estarían dispuestos a pagar por la primera unidad.")
    
    intercepto = st.slider("Intercepto (Precio máximo)", min_value=0.0, max_value=60.0, value=30.0, step=1.0, key="intercepto_slider")
    pendiente_const = 0.05
    Q_max2 = 700
    
    fig2 = graficar_demanda(intercepto, pendiente_const,
                            titulo=f"Demanda: P = {intercepto:.1f} - {pendiente_const}·Q", referencia=(30.0, 0.05))
    st.pyplot(fig2)
    
    st.markdown("**Fundamento económico:** La curva de demanda se desplaza cuando varían factores distintos al precio del bien, tales como el ingreso de los consumidores (diferenciando bienes normales de inferiores), los precios de bienes sustitutos o complementarios, los gustos, las expectativas futuras o el número de compradores. Un desplazamiento hacia la derecha refleja un aumento de la demanda; hacia la izquierda, una disminución.")

# PESTAÑA 3: Cambio continuo en la pendiente
with tab3:
    st.header("Impacto de cambios en la pendiente (sensibilidad al precio)")
    st.markdown("Modifica la **inclinación** de la curva: pendiente alta → poco sensible; pendiente baja → muy sensible.")
    
    pendiente = st.slider("Pendiente (valor absoluto)", min_value=0.01, max_value=0.1, value=0.05, step=0.01, key="pendiente_slider")
    intercepto_const = 30.0
    Q_max3 = 700
    
    fig3 = graficar_demanda(intercepto_const, pendiente,
                            titulo=f"Demanda: P = {intercepto_const} - {pendiente:.2f}·Q", referencia=(30.0, 0.05))
    st.pyplot(fig3)
    
    st.markdown("**Fundamento económico:** La pendiente de la demanda refleja la sensibilidad de la cantidad demandada ante variaciones en el precio. Una pendiente más inclinada indica menor capacidad de sustitución o un horizonte temporal corto. Por el contrario, una pendiente más plana surge cuando existen sustitutos cercanos.")

# Pie de página
st.markdown("---")
st.caption("Herramienta didáctica basada en la ley de demanda | Interactúa con los sliders para visualizar los conceptos económicos | Realizada por Guadalupe Amin, Candela Abregú, y Luciana Pasteris, 2026.")