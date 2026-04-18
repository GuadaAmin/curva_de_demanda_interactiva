import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Curva de Demanda - Herramienta Didáctica", layout="centered")
st.title("📉 Construcción de Curvas de Demanda")
st.markdown("Define una curva de demanda mediante **dos puntos** o **un punto y la pendiente económica**. Guarda múltiples curvas y comparalas.")
st.markdown("Por: Abregú Candela, Amin Guadalupe, y Luciana Pasteris.")
st.markdown("Economía 2026")

# Inicialización de variables de estado
if "curvas_guardadas" not in st.session_state:
    st.session_state.curvas_guardadas = []  # Lista de dicts con {'a': , 'b': , 'nombre': }
if "curva_actual" not in st.session_state:
    st.session_state.curva_actual = {'a': 100.0, 'b': 2.0}  # Q = a - bP

# Funciones de conversión entre formas matemática y económica
def demanda_economica_a_matematica(a, b):
    """
    a: cantidad demandada cuando P=0 (intercepto con eje Q) --> Punto de saciedad
    b: pendiente económica (ΔQ/ΔP, valor positivo)
    Forma económica: Q = a - b·P
    Forma matemática: P = (a/b) - (1/b)·Q
    Retorna (intercepto_P, pendiente_P) para graficar P en función de Q
    """
    intercepto_P = a / b  # Precio máximo
    pendiente_P = -1 / b   # Pendiente negativa para graficar
    return intercepto_P, pendiente_P

def actualizar_curva_desde_puntos(P1, Q1, P2, Q2):
    """
    Dados dos puntos (P, Q) en la curva de demanda,
    calcula los parámetros económicos a y b (Q = a - bP)
    """
    b = (Q1 - Q2) / (P2 - P1) if (P2 - P1) != 0 else 0.001
    b = abs(b)  # Pendiente positiva por convención
    a = Q1 + b * P1
    return a, b

def actualizar_curva_desde_punto_pendiente(P1, Q1, pendiente_economica):
    """
    Dados un punto (P, Q) y la pendiente económica b,
    calcula a (Q = a - bP)
    """
    b = abs(pendiente_economica)
    a = Q1 + b * P1
    return a, b

# Función para graficar
def graficar_todas_las_curvas(a_actual, b_actual, curvas_guardadas, punto=None):
    """
    Grafica la curva actual y todas las curvas guardadas.
    Los límites de los ejes se ajustan automáticamente al mayor valor.
    punto: tupla (Q, P) opcional para resaltar un punto sobre la curva actual
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Colores para las curvas guardadas
    colores_gris = ['#888888', '#AAAAAA', '#CCCCCC', '#DDDDDD', '#EEEEEE']
    
    # Variables para calcular límites máximos
    max_Q = 0
    max_P = 0
    
    # Graficar curvas guardadas y actualizar máximos
    for idx, curva in enumerate(curvas_guardadas):
        a_g = curva['a']
        b_g = curva['b']
        inter_p, pend_p = demanda_economica_a_matematica(a_g, b_g)
        
        # El intercepto P es el precio máximo de esta curva
        max_P = max(max_P, inter_p)
        # La cantidad máxima es a_g
        max_Q = max(max_Q, a_g)
        
        Q_vals = np.linspace(0, a_g + 20, 200)  # Graficar hasta a_g + margen
        P_vals = inter_p + pend_p * Q_vals
        P_vals = np.maximum(P_vals, 0)
        color = colores_gris[idx % len(colores_gris)]
        ax.plot(Q_vals, P_vals, color=color, linewidth=1.5, linestyle='--',
                label=f"Guardada: Q = {a_g:.1f} - {b_g:.2f}·P")
    
    # Graficar curva actual
    inter_p_act, pend_p_act = demanda_economica_a_matematica(a_actual, b_actual)
    max_P = max(max_P, inter_p_act)
    max_Q = max(max_Q, a_actual)
    
    Q_vals = np.linspace(0, a_actual + 20, 200)
    P_vals = inter_p_act + pend_p_act * Q_vals
    P_vals = np.maximum(P_vals, 0)
    ax.plot(Q_vals, P_vals, 'b-', linewidth=3, label=f"Actual: Q = {a_actual:.1f} - {b_actual:.2f}·P")
    
    # Marcar el punto si se proporciona
    if punto:
        q_punto, p_punto = punto
        ax.plot(q_punto, p_punto, 'ro', markersize=10, zorder=5)
        ax.annotate(f'  ({q_punto:.1f}, {p_punto:.1f})', 
                   (q_punto, p_punto), 
                   xytext=(10, -10),
                   textcoords='offset points',
                   fontsize=10,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Configurar ejes con límites AUTOMÁTICOS (más un margen del 10%)
    ax.set_xlim(0, max_Q * 1.1)
    ax.set_ylim(0, max_P * 1.1)
    ax.set_xlabel("Cantidad demandada (Q)")
    ax.set_ylabel("Precio (P)")
    ax.set_title("Curva(s) de Demanda - Forma económica: Q = a - b·P")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', fontsize=8)
    
    return fig


# INTERFAZ PRINCIPAL

# Sección 1: Definición de la curva original por el usuario
st.header("1. Definir la curva original")

metodo = st.radio("¿Cómo deseas definir la curva?", 
                  ["Dos puntos (P, Q)", "Un punto + pendiente económica"])

col1, col2 = st.columns(2)

if metodo == "Dos puntos (P, Q)":
    with col1:
        st.subheader("Punto A")
        P_A = st.number_input("Precio A (P)", min_value=0.0, max_value=200.0, value=50.0, step=1.0, key="PA")
        Q_A = st.number_input("Cantidad A (Q)", min_value=0.0, max_value=200.0, value=50.0, step=1.0, key="QA")
    with col2:
        st.subheader("Punto B")
        P_B = st.number_input("Precio B (P)", min_value=0.0, max_value=200.0, value=20.0, step=1.0, key="PB")
        Q_B = st.number_input("Cantidad B (Q)", min_value=0.0, max_value=200.0, value=80.0, step=1.0, key="QB")
    
    if st.button("Calcular curva"):
        try:
            a, b = actualizar_curva_desde_puntos(P_A, Q_A, P_B, Q_B)
            st.session_state.curva_actual = {'a': a, 'b': b}
            # FORZAR ACTUALIZACIÓN DE LOS SLIDERS
            st.session_state.a_slider = a
            st.session_state.b_slider = b
            st.success(f"Curva calculada: Q = {a:.2f} - {b:.2f}·P")
            st.rerun()  # Forzar recarga para que los sliders muestren el nuevo valor
        except Exception as e:
            st.error(f"Error al calcular: {e}")
else:
    with col1:
        P_punto = st.number_input("Precio del punto (P)", min_value=0.0, max_value=200.0, value=50.0, step=1.0, key="Ppunto")
        Q_punto = st.number_input("Cantidad del punto (Q)", min_value=0.0, max_value=200.0, value=50.0, step=1.0, key="Qpunto")
    with col2:
        pendiente_econ = st.number_input("Pendiente económica (b = ΔQ/ΔP)", min_value=0.01, max_value=10.0, value=2.0, step=0.1, key="pend_econ")
    
    if st.button("Calcular curva"):
        a, b = actualizar_curva_desde_punto_pendiente(P_punto, Q_punto, pendiente_econ)
        st.session_state.curva_actual = {'a': a, 'b': b}
        # FORZAR ACTUALIZACIÓN DE LOS SLIDERS
        st.session_state.a_slider = a
        st.session_state.b_slider = b
        st.success(f"Curva calculada: Q = {a:.2f} - {b:.2f}·P")
        st.rerun()

# Sección 2: Sliders para modificar la curva actual y desplazarse
st.header("2. Modificar la curva actual en tiempo real")

col_s1, col_s2 = st.columns(2)
with col_s1:
    a_slider = st.slider("Parámetro a, cambio de precio máximo que pagarían clientes y punto de saciedad", 
                          min_value=0.0, max_value=300.0, 
                          value=st.session_state.curva_actual['a'], step=5.0, key="a_slider")
with col_s2:
    b_slider = st.slider("Pendiente económica b (ΔQ/ΔP, sensibilidad de la demanda al cambio de precio)", 
                          min_value=0.1, max_value=10.0, 
                          value=st.session_state.curva_actual['b'], step=0.1, key="b_slider")
    
# ACTUALIZAR la curva actual con los valores de los sliders
st.session_state.curva_actual['a'] = a_slider
st.session_state.curva_actual['b'] = b_slider

# Desplazamiento a lo largo de la curva

# Obtener valores actualizados
a_act = st.session_state.curva_actual['a']
b_act = st.session_state.curva_actual['b']

# Calcular rango posible (desde 0 hasta a)
Q_max_desp = max(0.1, a_act)  # Evitar que sea cero

# Inicializar el valor del slider de desplazamiento en session_state si no existe
if "cantidad_deslizante" not in st.session_state:
    st.session_state.cantidad_deslizante = Q_max_desp / 2

# Ajustar el valor si supera el nuevo máximo
if st.session_state.cantidad_deslizante > Q_max_desp:
    st.session_state.cantidad_deslizante = Q_max_desp / 2

cantidad_deslizante = st.slider(
    "Selecciona la cantidad (Q) para moverte a lo largo de la curva",
    min_value=0.0,
    max_value=float(Q_max_desp),
    value=float(st.session_state.cantidad_deslizante),
    step=1.0,
    key="deslizamiento_curva"
)

# Guardar el valor actual en session_state para la próxima iteración
st.session_state.cantidad_deslizante = cantidad_deslizante

# Calcular el precio correspondiente
if b_act > 0:
    precio_correspondiente = (a_act - cantidad_deslizante) / b_act
    precio_correspondiente = max(0, precio_correspondiente)
else:
    precio_correspondiente = 0

punto_actual = (cantidad_deslizante, precio_correspondiente)

fig = graficar_todas_las_curvas(
    st.session_state.curva_actual['a'],
    st.session_state.curva_actual['b'],
    st.session_state.curvas_guardadas,
    punto=punto_actual if 'punto_actual' in locals() else None
)
st.pyplot(fig)

st.caption("Los ejes se ajustan automáticamente para mostrar todas las curvas completas.")

# Guardar curva
st.header("Guardar curva para comparar")

nombre_curva = st.text_input("Nombre de la curva a guardar", value=f"Curva {len(st.session_state.curvas_guardadas)+1}")
col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("💾 Guardar curva actual"):
        st.session_state.curvas_guardadas.append({
            'a': st.session_state.curva_actual['a'],
            'b': st.session_state.curva_actual['b'],
            'nombre': nombre_curva
        })
        st.success(f"Curva guardada: {nombre_curva}")
with col_b2:
    if st.button("🗑️ Limpiar curvas guardadas") and len(st.session_state.curvas_guardadas) > 0:
        st.session_state.curvas_guardadas = []
        st.warning("Se eliminaron todas las curvas guardadas")

# Mostrar curvas guardadas
if st.session_state.curvas_guardadas:
    st.write("**Curvas guardadas:**")
    for i, c in enumerate(st.session_state.curvas_guardadas):
        st.write(f"{i+1}. {c['nombre']}: Q = {c['a']:.1f} - {c['b']:.2f}·P")

# Explicaciones 
st.header("📖 Fundamentos económicos")
st.markdown("""
- **Forma económica de la demanda lineal:** Q = a - b·P
  - **a:** Cantidad demandada cuando el precio es cero (intercepto con el eje Q). Punto de saciedad.
  - **b:** Pendiente económica (ΔQ/ΔP). Indica cuánto varía la cantidad demandada ante un cambio unitario en el precio.
- **Forma matemática (para graficar):** P = (a/b) - (1/b)·Q
  - El precio máximo que los compradores están dispuestos a pagar (ordenada al origen) es a/b.
  - La pendiente de la recta en el gráfico es -1/b.
- **Desplazamiento a lo largo de la curva:** Un movimiento a lo largo de la curva de demanda se origina exclusivamente por una variación en el precio del bien, manteniéndose constantes los demás factores (ingresos, gustos, precios de sustitutos). Conforme la ley de la demanda establece, un aumento del precio reduce la cantidad demandada, y una disminución la incrementa, desplazando el punto de equilibrio sobre la misma curva.
- **Cambio del intercepto:** La curva de demanda se desplaza horizontalmente cuando varían factores distintos al precio del bien, tales como el ingreso de los consumidores (diferenciando bienes normales de inferiores), los precios de bienes sustitutos o complementarios, los gustos, las expectativas futuras o el número de compradores. Un desplazamiento hacia la derecha refleja un aumento de la demanda; hacia la izquierda, una disminución.
- **Cambio de la pendiente económica:** La pendiente de la demanda refleja la sensibilidad de la cantidad demandada ante variaciones en el precio. Una pendiente más inclinada indica menor capacidad de sustitución o un horizonte temporal corto. Por el contrario, una pendiente más plana surge cuando existen sustitutos cercanos.
""")

st.caption("Herramienta didáctica - Construye, modifica y compara múltiples curvas de demanda.")