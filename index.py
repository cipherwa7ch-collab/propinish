import flet as ft
from datetime import datetime
import pyperclip

def main(page: ft.Page):
    # CONFIGURACIÓN VISUAL
    page.title = "Propinish"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 450
    page.scroll = "adaptive"
    page.theme = ft.Theme(color_scheme_seed="indigo") # Cambia "indigo" por "teal" o "blue"
    page.bgcolor = "#f5f5f5" # Fondo gris muy claro

    # Listas de personal
    nombres_full = ["Leonardo", "Maryu", "Ross", "Juan", "Anahis", "Neervison", "Luis", "Liz", "Jessica", "Valentina", "Angelica"]
    nombres_part = ["Annel", "Genesis", "Eliza", "Cony", "Fefi", "Monica", "Pancha"]

    checks_full = {}
    checks_part = {}
    mensaje_final = [""]

    # --- ELEMENTOS DE INTERFAZ ---
    efectivo = ft.TextField(label="Efectivo", prefix_icon=ft.Icons.ATTACH_MONEY_ROUNDED, border_radius=15, bgcolor="white")
    transbank = ft.TextField(label="Transbank", prefix_icon=ft.Icons.CREDIT_CARD_ROUNDED, border_radius=15, bgcolor="white")

    res_cocina = ft.Text(size=18, color="orange-800", weight="bold")
    res_garzones = ft.Text(size=18, color="indigo-800", weight="bold")
    res_individual = ft.Column()

    def calcular(e):
        try:
            m_efectivo = float(efectivo.value) if efectivo.value else 0
            m_tbk = float(transbank.value) if transbank.value else 0
            total_general = m_efectivo + m_tbk
            monto_cocina = total_general * 0.20
            monto_garzones = total_general * 0.80

            seleccionados_full = [n for n, c in checks_full.items() if c.value]
            seleccionados_part = [n for n, c in checks_part.items() if c.value]
            puntos = (len(seleccionados_full) * 1.0) + (len(seleccionados_part) * 0.5)

            res_individual.controls.clear()
            if puntos > 0:
                valor_p = monto_garzones / puntos
                res_cocina.value = f"🍳 Cocina (20%): ${monto_cocina:,.0f}"
                res_garzones.value = f"🍷 Garzones (80%): ${monto_garzones:,.0f}"
                
                res_individual.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Full Time: ${valor_p:,.0f}", size=20, weight="bold", color="green-700"),
                            ft.Text(f"Part Time: ${(valor_p * 0.5):,.0f}", size=20, weight="bold", color="green-600"),
                        ]),
                        bgcolor="green-50", padding=15, border_radius=10
                    )
                )
                
                fecha = datetime.now().strftime("%d/%m/%Y")
                mensaje_final[0] = (f"*PROPINAS {fecha}*\n\n💰 Total: ${total_general:,.0f}\n🍳 Cocina: ${monto_cocina:,.0f}\n🍷 Garzones: ${monto_garzones:,.0f}\n---\n✅ Full: ${valor_p:,.0f}\n✅ Part: ${(valor_p * 0.5):,.0f}")
                btn_copiar.visible = True
            else:
                btn_copiar.visible = False
        except:
            pass
        page.update()

    def copiar_texto(e):
        pyperclip.copy(mensaje_final[0])
        page.snack_bar = ft.SnackBar(ft.Text("¡Copiado para WhatsApp!"), bgcolor="green-700")
        page.snack_bar.open = True
        page.update()

    btn_copiar = ft.ElevatedButton("COPIAR RESUMEN", icon=ft.Icons.SEND_ROUNDED, on_click=copiar_texto, visible=False, style=ft.ButtonStyle(color="white", bgcolor="green-600"))

    # Estructura de Listas con Checkboxes
    def crear_lista(nombres, diccionario):
        return ft.Column([diccionario.setdefault(n, ft.Checkbox(label=n, scale=0.9)) for n in nombres], spacing=0)

    # --- DISEÑO DE LA PÁGINA ---
    page.add(
        ft.Container(
            content=ft.Column([
                # CABECERA (Logo y Título)
                ft.Row([
                    ft.Icon(ft.Icons.RESTAURANT_MENU_ROUNDED, size=40, color="indigo"),
                    ft.Text("Propinish", size=32, weight="bold", color="indigo"),
                ], alignment="center"),
                
                # SECCIÓN DINERO
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text("Ingresos del Turno", weight="bold"),
                            efectivo, transbank
                        ])
                    )
                ),

                # SECCIÓN GARZONES
                ft.Text("Personal en Turno", weight="bold", size=16),
                ft.Row([
                    ft.Column([ft.Text("FULL", size=11, weight="bold"), crear_lista(nombres_full, checks_full)], expand=True),
                    ft.Column([ft.Text("PART", size=11, weight="bold"), crear_lista(nombres_part, checks_part)], expand=True),
                ], vertical_alignment="start"),

                ft.ElevatedButton("CALCULAR AHORA", on_click=calcular, height=50, width=500, style=ft.ButtonStyle(bgcolor="indigo", color="white")),
                
                # RESULTADOS
                res_cocina,
                res_garzones,
                res_individual,
                btn_copiar,
                ft.Text("v1.5 - Hecho por Pancha", size=10, italic=True, text_align="center", width=500)
            ], horizontal_alignment="center"),
            padding=10
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
