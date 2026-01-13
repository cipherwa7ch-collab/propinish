import flet as ft

def main(page: ft.Page):
    page.title = "Propinish"
    page.scroll = "adaptive"
    
    # Listas de garzones
    nombres_full = ["Leonardo", "Maryu", "Ross", "Juan", "Anahis", "Neervison", "Luis", "Liz", "Jessica", "Valentina", "Angelica"]
    nombres_part = ["Annel", "Genesis", "Eliza", "Cony", "Fefi", "Monica", "Pancha"]

    checks_full = {}
    checks_part = {}

    efectivo = ft.TextField(label="Efectivo", keyboard_type=ft.KeyboardType.NUMBER)
    transbank = ft.TextField(label="Transbank", keyboard_type=ft.KeyboardType.NUMBER)
    res_cocina = ft.Text(size=18, color="orange", weight="bold")
    res_individual = ft.Column()

    def calcular(e):
        try:
            total = (float(efectivo.value or 0) + float(transbank.value or 0)) * 0.80
            cocina = (float(efectivo.value or 0) + float(transbank.value or 0)) * 0.20
            
            puntos = sum(1 for c in checks_full.values() if c.value) + sum(0.5 for c in checks_part.values() if c.value)

            res_individual.controls.clear()
            if puntos > 0:
                v_punto = total / puntos
                res_cocina.value = f"Cocina: ${cocina:,.0f}"
                res_individual.controls.append(ft.Text(f"Full: ${v_punto:,.0f}", size=20, weight="bold"))
                res_individual.controls.append(ft.Text(f"Part: ${(v_punto*0.5):,.0f}", size=20, weight="bold"))
            page.update()
        except:
            pass

    page.add(
        ft.Text("Propinish", size=30, weight="bold"),
        efectivo, transbank,
        ft.Text("Garzones Full", weight="bold"),
        ft.Column([checks_full.setdefault(n, ft.Checkbox(label=n)) for n in nombres_full]),
        ft.Text("Garzones Part", weight="bold"),
        ft.Column([checks_part.setdefault(n, ft.Checkbox(label=n)) for n in nombres_part]),
        ft.ElevatedButton("Calcular", on_click=calcular),
        res_cocina,
        res_individual
    )
app = ft.app(target=main, export_asgi=True) # ESTA LINEA ES CLAVE PARA VERCEL

