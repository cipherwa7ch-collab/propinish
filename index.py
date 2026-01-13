import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Propinish"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.theme = ft.Theme(color_scheme_seed="indigo")
    
    # Listas de personal
    nombres_full = ["Leonardo", "Maryu", "Ross", "Juan", "Anahis", "Neervison", "Luis", "Liz", "Jessica", "Valentina", "Angelica"]
    nombres_part = ["Annel", "Genesis", "Eliza", "Cony", "Fefi", "Monica", "Pancha"]

    checks_full = {}
    checks_part = {}
    mensaje_final = ft.Text("") # Usamos un control de Flet para guardar el texto

    # --- ELEMENTOS DE INTERFAZ ---
    efectivo = ft.TextField(label="Efectivo", prefix_icon=ft.Icons.ATTACH_MONEY_ROUNDED, border_radius=15)
    transbank = ft.TextField(label="Transbank", prefix_icon=ft.Icons.CREDIT_CARD_ROUNDED, border_radius=15)
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
                mensaje_final.value = (f"*PROPINAS {fecha}*\n\n💰 Total: ${total_general:,.0f}\n🍳 Cocina: ${monto_cocina:,.0f}\n🍷 Garzones: ${monto_garzones:,.0f}\n---\n✅ Full: ${valor_p:,.0f}\n✅ Part: ${(valor_p * 0.5):,.0f}")
                btn_copiar.visible = True
            else:
                btn_copiar.visible = False
        except:
            res_cocina.value = "Error en montos"
        page.update()

    def copiar_texto(e):
        # ESTA ES LA FORMA CORRECTA PARA WEB
        page.set_clipboard(mensaje_final.value)
        page.snack_bar = ft.SnackBar(ft.Text("¡Copiado! Pégalo en WhatsApp"))
        page.snack_bar.open = True
        page.update()

    btn_copiar = ft.ElevatedButton("COPIAR RESUMEN", icon=ft.Icons.COPY, on_click=copiar_texto, visible=False)

    def crear_lista(nombres, diccionario):
        return ft.Column([diccionario.setdefault(n, ft.Checkbox(label=n)) for n in nombres], spacing=0)

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.RESTAURANT), ft.Text("Propinish", size=30, weight="bold")], alignment="center"),
                efectivo, transbank,
                ft.Row([
                    ft.Column([ft.Text("FULL", weight="bold"), crear_lista(nombres_full, checks_full)], expand=True),
                    ft.Column([ft.Text("PART", weight="bold"), crear_lista(nombres_part, checks_part)], expand=True),
                ], vertical_alignment="start"),
                ft.ElevatedButton("CALCULAR", on_click=calcular, height=50, width=400),
                res_cocina, res_garzones, res_individual, btn_copiar
            ], horizontal_alignment="center"),
            padding=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
