from flask import Flask, render_template, request
import random

app = Flask(__name__)

def reiniciar_juego():
    global zonas_acertar, disparos_acertados, disparos_fallados, oportunidades_restantes
    zonas_acertar = set()
    while len(zonas_acertar) < 10:
        zonas_acertar.add((random.randint(0, 9), random.randint(0, 9)))
    disparos_acertados = set()
    disparos_fallados = set()
    oportunidades_restantes = 50

reiniciar_juego()

@app.route('/', methods=['GET', 'POST'])
def index():
    global zonas_acertar, disparos_acertados, disparos_fallados, oportunidades_restantes

    message = ''
    acertados = len(disparos_acertados)
    fallados = len(disparos_fallados)

    if request.method == 'POST':
        if 'reset' in request.form:
            reiniciar_juego()
        else:
            if oportunidades_restantes > 0:
                x = request.form.get('x')
                y = request.form.get('y')

                if x is not None and y is not None:
                    try:
                        x = int(x)
                        y = int(y)

                        if (x, y) in zonas_acertar:
                            disparos_acertados.add((x, y))
                            message = '¡Acertaste!'
                        else:
                            disparos_fallados.add((x, y))
                            message = 'Error, intenta de nuevo.'
                    except ValueError:
                        pass

                oportunidades_restantes -= 1

            if oportunidades_restantes == 0:
                message = '¡Has alcanzado el límite máximo de elecciones! Perdiste.'
                reiniciar_juego()

            if len(disparos_acertados) == 10:
                message = '¡Felicidades! ¡Has encontrado todas las casillas ocultas!'
                reiniciar_juego()

    return render_template('index.html', message=message, acertados=acertados, fallados=fallados, oportunidades_restantes=oportunidades_restantes, disparos_acertados=disparos_acertados)

if __name__ == '__main__':
    app.run(debug=True)
