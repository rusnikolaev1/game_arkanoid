# подключаем графическую библиотеку
from tkinter import *
# подключаем модули, которые отвечают за время и случайные числа
import time
import random
from typing import List

# создаём новый объект — окно с игровым полем. В нашем случае переменная окна называется tk, и мы его сделали из класса Tk() — он есть в графической библиотеке 
tk = Tk()
# делаем заголовок окна — Games с помощью свойства объекта title
tk.title('Game')
# запрещаем менять размеры окна, для этого используем свойство resizable 
tk.resizable(0, 0)
# помещаем наше игровое окно выше остальных окон на компьютере, чтобы другие окна не могли его заслонить
tk.wm_attributes('-topmost', 1)
# создаём новый холст — 400 на 500 пикселей, где и будем рисовать игру
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
# говорим холсту, что у каждого видимого элемента будут свои отдельные координаты 
canvas.pack()
# обновляем окно с холстом
tk.update()


#создаем класс Ball
class Ball():
    """
    Этот класс описывает поведение объекта шар
    """
    Y_VEL = 6
    X_VEL = 6
    def __init__(self, canvas: Canvas, paddle: 'Paddle', score: int, color: str) -> None:
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.colot = color
        #дополнительные свойства объекта, которые появляются после создания объекта
        #cоздаем шарик радиусом 15 пикселей
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        #перемещаем шарик в точку с координатами 245, 100 - середина окна
        self.canvas.move(self.id, 245, 100)
        #задаем список возможных направлений для стартового движения
        starts: List = [-self.X_VEL, -self.X_VEL/2, self.X_VEL/2, self.X_VEL]
        random.shuffle(starts)
        #Выбираем первое значение - оно будет вектором движения шарика
        self.x = starts[0]
        # в самом начале он всегда падает вниз, поэтому уменьшаем значение по оси y
        random.shuffle(starts)
        self.y = starts[0]
        # шарик узнаёт свою высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # свойство, которое отвечает за то, достиг шарик дна или нет. Пока не достиг, значение будет False
        self.hit_bottom = False
    
    # обрабатываем касание платформы, для этого получаем 4 координаты шарика в переменной pos (левая верхняя и правая нижняя точки)
    def hit_paddle(self, pos: list):
        #получаем координаты платформы
        paddle_pos: List = self.canvas.coords(self.paddle.id)
        # если шар касается платформы
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                # увеличиваем счёт (обработчик этого события будет описан ниже)
                self.score.hit()
                # возвращаем метку о том, что мы успешно коснулись
                return True
        # возвращаем False — касания не было
        return False
    
    # обрабатываем отрисовку шарика
    def draw(self):
        time.sleep(0.0001)
        # передвигаем шарик на заданные координаты x и y
        self.canvas.move(self.id, self.x, self.y)
        # запоминаем новые координаты шарика
        pos = self.canvas.coords(self.id)
        # если шарик падает сверху  
        if pos[1] <= 0:
            # задаём падение на следующем шаге = 2
            self.y = self.Y_VEL
        # если шарик правым нижним углом коснулся дна
        if pos[3] >= self.canvas_height:
            # помечаем это в отдельной переменной
            self.hit_bottom = True
            # выводим сообщение и количество очков
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red')
        # если было касание платформы
        if self.hit_paddle(pos) == True:
            # отправляем шарик наверх
            self.y = -self.Y_VEL
        # если коснулись левой стенки
        if pos[0] <= 0:
            # движемся вправо
            self.x = self.X_VEL
        # если коснулись правой стенки
        if pos[2] >= self.canvas_width:
            # движемся влево
            self.x = -self.X_VEL

# Класс платформы Paddle
class Paddle:
    # конструктор
    PAD_VEL = 100
    def __init__(self, canvas, color):
        # canvas означает, что платформа будет нарисована на нашем изначальном холсте
        self.canvas = canvas
        # создаём прямоугольную платформу 10 на 100 пикселей, закрашиваем выбранным цветом и получаем её внутреннее имя 
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # задаём список возможных стартовых положений платформы
        starts_pad = [40, 60, 90, 120, 150, 180, 200]
        #перемешиваем
        random.shuffle(starts_pad)
        #первое значение будет равно положению платформы
        self.starting_point_x = starts_pad[0]
        # перемещаем платформу в стартовое положение
        self.canvas.move(self.id, self.starting_point_x, 300)
        # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.x = 0
        # платформа узнаёт свою ширину
        self.canvas_width = self.canvas.winfo_width()
        # задаём обработчик нажатий
        # если нажата стрелка вправо — выполняется метод turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # если стрелка влево — turn_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        # пока игра не началась, поэтому ждём
        self.started = False
        # как только игрок нажмёт Enter — всё стартует
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
        # движемся вправо 
        self.pad_right = False
        self.pad_left = False
    def turn_right(self, event):
        # будем смещаться правее на 2 пикселя по оси х
        self.pad_right = True
        self.pad_left = False
    # движемся влево
    def turn_left(self, event):
        # будем смещаться левее на 2 пикселя по оси х
        self.pad_left = True
        self.pad_right = False
    # игра начинается
    def start_game(self, event):
        # меняем значение переменной, которая отвечает за старт
        self.started = True
    def draw(self):
        self.x = 0
        #time.sleep(0.000001)
        if self.pad_right == True:
            self.x = self.PAD_VEL
        elif self.pad_left == True:
            self.x = -self.PAD_VEL
        # сдвигаем нашу платформу на заданное количество пикселей
        self.canvas.move(self.id, self.x, 0)

        self.pad_left = False
        self.pad_right = False

        # получаем координаты холста
        pos = self.canvas.coords(self.id)
        # если мы упёрлись в левую границу 
        if pos[0] <= 0:
            # останавливаемся
            self.canvas.move(self.id,0 - pos[0], 0)
        # если упёрлись в правую границу 
        elif pos[2] >= self.canvas_width:
            # останавливаемся
            self.canvas.move(self.id, self.canvas_width - pos[2], 0)

#  Описываем класс Score, который отвечает за отображение счетов
class Score:
    # конструктор
    def __init__(self, canvas, color):
        # в самом начале счёт равен нулю
        self.score = 0
        # будем использовать наш холст
        self.canvas = canvas
        # создаём надпись, которая показывает текущий счёт, делаем его нужно цвета и запоминаем внутреннее имя этой надписи
        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color)
    # обрабатываем касание платформы
    def hit(self):
        # увеличиваем счёт на единицу
        self.score += 1
        # пишем новое значение счёта 
        self.canvas.itemconfig(self.id, text=self.score)

if __name__ == "__main__":
    # создаём объект — зелёный счёт 
    score = Score(canvas, 'green')
    # создаём объект — белую платформу
    paddle = Paddle(canvas, 'White')
    # создаём объект — красный шарик 
    ball = Ball(canvas, paddle, score, 'red')
    # пока шарик не коснулся дна 
    while not ball.hit_bottom:
        # если игра началась и платформа может двигаться
        if paddle.started == True:
            # двигаем шарик
            ball.draw()
            # двигаем платформу
            paddle.draw()
        # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
        tk.update_idletasks()
        # обновляем игровое поле, и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
        tk.update()
        # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
        time.sleep(0.01)
    # если программа дошла досюда, значит, шарик коснулся дна. Ждём 3 секунды, пока игрок прочитает финальную надпись, и завершаем игру
    time.sleep(3)
