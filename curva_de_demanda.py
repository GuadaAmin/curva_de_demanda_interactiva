import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Configuración de la página
# ------------------------------------------------------------
st.set_page_config(page_title="Curva de Demanda - Herramienta Didáctica", layout="centered")
st.title("📉 Construcción de Curvas de Demanda")
st.markdown("Define una curva de demanda mediante **dos puntos** o **un punto y la pendiente económica**. Guarda múltiples curvas y comparalas.")
st.markdown("Por: Abregú Candela, Amin Guadalupe, y Luciana Pasteris.")
st.markdown("Economía 2026")

# ------------------------------------------------------------
# Inicialización de variables de estado
# ------------------------------------------------------------
if "curvas_guardadas" not in st.session_state:
    st.session_state.curvas_guardadas = []  # Lista de dicts con {'a': , 'b': , 'nombre': }
if "curva_actual" not in st.session_state:
    st.session_state.curva_actual = {'a': 100.0, 'b': 2.0}  # Q = a - bP
if "limites_fijos" not in st.session_state:
    st.session_state.limites_fijos = None  # Se asignará cuando se calcule la primera curva

# ------------------------------------------------------------
# Funciones de conversión entre formas matemática y económica
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Función para graficar
# ------------------------------------------------------------
def graficar_todas_las_curvas(a_actual, b_actual, curvas_guardadas, Q_max_fijo, P_max_fijo):
    """
    Grafica la curva actual y todas las curvas guardadas.
    Q_max_fijo: límite superior del eje Q (fijo)
    P_max_fijo: límite superior del eje P (fijo)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Colores para las curvas guardadas
    colores_gris = ['#888888', '#AAAAAA', '#CCCCCC', '#DDDDDD', '#EEEEEE']
    
    # Graficar curvas guardadas
    for idx, curva in enumerate(curvas_guardadas):
        a_g = curva['a']
        b_g = curva['b']
        inter_p, pend_p = demanda_economica_a_matematica(a_g, b_g)
        Q_vals = np.linspace(0, Q_max_fijo, 200)
        P_vals = inter_p + pend_p * Q_vals
        P_vals = np.maximum(P_vals, 0)
        color = colores_gris[idx % len(colores_gris)]
        ax.plot(Q_vals, P_vals, color=color, linewidth=1.5, linestyle='--',
                label=f"Guardada: Q = {a_g:.1f} - {b_g:.2f}·P")
    
    # Graficar curva actual
    inter_p_act, pend_p_act = demanda_economica_a_matematica(a_actual, b_actual)
    Q_vals = np.linspace(0, Q_max_fijo, 200)
    P_vals = inter_p_act + pend_p_act * Q_vals
    P_vals = np.maximum(P_vals, 0)
    ax.plot(Q_vals, P_vals, 'b-', linewidth=3, label=f"Actual: Q = {a_actual:.1f} - {b_actual:.2f}·P")
    
    # Configurar ejes con límites FIJOS
    ax.set_xlim(0, Q_max_fijo)
    ax.set_ylim(0, P_max_fijo)
    ax.set_xlabel("Cantidad demandada (Q)")
    ax.set_ylabel("Precio (P)")
    ax.set_title("Curva(s) de Demanda - Forma económica: Q = a - b·P")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', fontsize=8)
    
    return fig

# ------------------------------------------------------------
# INTERFAZ PRINCIPAL
# ------------------------------------------------------------

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
            a, b = actualizar_curva_desde_puntos(P_A, Q_A, P_B, Q_B)  # o desde punto+pendiente
            st.session_state.curva_actual = {'a': a, 'b': b}
            
            # Fijar los límites de los ejes SOLO UNA VEZ (si aún no están fijos)
            if st.session_state.limites_fijos is None:
                inter_p, _ = demanda_economica_a_matematica(a, b)
                P_max_fijo = inter_p * 1.1  # 10% más que el precio máximo de la primera curva
                Q_max_fijo = a + 50  # Cantidad máxima: a + un margen
                st.session_state.limites_fijos = {'P_max': P_max_fijo, 'Q_max': Q_max_fijo}
            
            st.success(f"Curva calculada: Q = {a:.2f} - {b:.2f}·P")
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
        st.success(f"Curva calculada: Q = {a:.2f} - {b:.2f}·P")

# ------------------------------------------------------------
# Sección 2: Sliders para modificar la curva actual
# ------------------------------------------------------------
st.header("2. Modificar la curva actual en tiempo real")

col_s1, col_s2 = st.columns(2)
with col_s1:
    a_slider = st.slider("Parámetro a (cantidad demandada cuando P=0)", 
                          min_value=0.0, max_value=300.0, 
                          value=st.session_state.curva_actual['a'], step=5.0, key="a_slider")
with col_s2:
    b_slider = st.slider("Pendiente económica b (ΔQ/ΔP, sensibilidad al precio)", 
                          min_value=0.1, max_value=10.0, 
                          value=st.session_state.curva_actual['b'], step=0.1, key="b_slider")

# Actualizar la curva actual con los sliders
st.session_state.curva_actual['a'] = a_slider
st.session_state.curva_actual['b'] = b_slider

# Obtener límites fijos (si no existen, usar valores por defecto)
if st.session_state.limites_fijos is None:
    # Si aún no se ha definido ninguna curva, usar valores por defecto
    Q_max_fijo = 200
    P_max_fijo = 150
else:
    Q_max_fijo = st.session_state.limites_fijos['Q_max']
    P_max_fijo = st.session_state.limites_fijos['P_max']

fig = graficar_todas_las_curvas(
    st.session_state.curva_actual['a'],
    st.session_state.curva_actual['b'],
    st.session_state.curvas_guardadas,
    Q_max_fijo,
    P_max_fijo
)
st.pyplot(fig)

st.caption(f"Ejes fijos: P hasta {P_max_fijo:.1f} | Q hasta {Q_max_fijo:.1f} (definidos con la primera curva)")
# Mostrar información de los ejes
st.caption(f"Eje P fijo hasta {y_max:.1f} | Eje Q fijo hasta {Q_max_fijo}")

# ------------------------------------------------------------
# Guardar curva
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Explicaciones didácticas
# ------------------------------------------------------------
st.header("📖 Fundamentos económicos")
st.markdown("""
- **Forma económica de la demanda lineal:** Q = a - b·P
  - **a:** Cantidad demandada cuando el precio es cero (intercepto con el eje Q).
  - **b:** Pendiente económica (ΔQ/ΔP). Indica cuánto varía la cantidad demandada ante un cambio unitario en el precio. Siempre positiva por la ley de la demanda.
- **Forma matemática (para graficar):** P = (a/b) - (1/b)·Q
  - El precio máximo (ordenada al origen) es a/b.
  - La pendiente de la recta en el gráfico es -1/b.
- **Movimiento a lo largo de la curva:** Cambia solo el precio.
- **Desplazamiento de la curva:** Cambia el parámetro a (ingresos, gustos, etc.) o b (sustitutos, horizonte temporal).
""")

st.caption("Herramienta didáctica - Construye, modifica y compara múltiples curvas de demanda.")