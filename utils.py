from datetime import date, timedelta


mesesDic = {
    1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
    5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto', 9:'Septiembre',
    10:'Octubre', 11:'Noviembre', 12:'Diciembre'
}

normal_colors = {
    'Pinar del Río': "#00553d",
    'Artemisa': "#fe0002",
    'La Habana': "#020085",
    'Mayabeque': "#940000",
    'Matanzas': "#e36d70",
    'Cienfuegos': "#00a261",
    'Villa Clara': "#ff7a13",
    'Sancti Spíritus': "#fe6515",
    'Ciego de Ávila': "#008dd0",
    'Camagüey': "#003060",
    'Las Tunas': "#009c55",
    'Holguín': "#007fc6",
    'Granma': "#0b4ca0",
    'Santiago de Cuba': "#ef242a",
    'Guantánamo': "#515a57",
    'Isla de la Juventud': "#38b396"
}

def date_range(date_init, date_end, idays=1):
        dater = []
        date_current = date.fromisoformat(date_init)
        date_end = date.fromisoformat(date_end)
        oneDay = timedelta(days=+idays)
        while date_current <= date_end:
            dater.append(date_current.isoformat())
            date_current += oneDay
        if date_end.isoformat() not in dater:
            dater.append(date_end.isoformat())
        return dater
